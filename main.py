import cv2
import numpy as np
import gradio as gr

# Import các hàm từ các file của bạn
from imgLoad import load_image_gradio
from scaleCalibration import select_point, calc_mm_per_pixel, calc_mm_value
from objectContour import getFilledContourMask
from pixelToMM import get_object_area_gradio

style_css = """
<style>
    .main-header {
        text-align: center; 
        padding: 25px; 
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        border-radius: 12px; 
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: white !important; 
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .section-card {
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 10px;
    }
</style>
"""

# Bỏ tham số css=... ở đây để tránh lỗi TypeError
with gr.Blocks() as demo:
    # 1. Chèn CSS thủ công qua HTML
    gr.HTML(style_css)
    
    # 2. Tiêu đề ứng dụng
    gr.HTML("""
        <div class='main-header'>
            <h1>📏 HỆ THỐNG ĐO DIỆN TÍCH VẬT THỂ</h1>
        </div>
    """)

    state_object = gr.State()
    state_mm = gr.State()

    with gr.Row():
        # CỘT TRÁI: Cấu hình và Thước
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown("### 📥 Bước 1: Nhập ảnh")
                input_img = gr.Image(label="Upload ảnh (Vật thể + Thước)", type="pil")
                btn_load = gr.Button("🚀 Tách ảnh Ruler & Object", variant="primary")
            
            with gr.Group():
                gr.Markdown("### 📏 Bước 2: Calibration")
                output_ruler = gr.Image(label="Ảnh thước (Click 2 điểm)", type="numpy", interactive=True)
                real_mm = gr.Number(label="Nhập chiều dài thực (mm)", value=10)
                btn_calc = gr.Button("✅ Tính mm/pixel")
                output = gr.Textbox(label="Kết quả thông số", interactive=False)

        # CỘT PHẢI: Vật thể và Kết quả
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown("### 🔍 Bước 3: Nhận diện")
                output_object = gr.Image(label="Ảnh vật thể", type="numpy")
                
            with gr.Group():
                gr.Markdown("### 📊 Bước 4: Diện tích thực tế")
                btn_area = gr.Button("✨ TÍNH DIỆN TÍCH", variant="primary")
                objectArea = gr.Textbox(
                    label="Kết quả (mm²)", 
                    placeholder="Diện tích sẽ hiển thị tại đây...",
                    text_align="center"
                )

    # =========================== Logic xử lý =====================
    def load_wrapper(img):
        if img is None: return None, None, None
        ruler, obj = load_image_gradio(img)
        # Gửi ruler cho output_ruler, obj cho output_object và state_object
        return ruler, obj, obj
    
    def calc_mm_wrapper(real_mm_val):
        text_info = calc_mm_per_pixel(real_mm_val)
        mm_value = calc_mm_value(real_mm_val)
        return text_info, mm_value

    # Đăng ký các sự kiện (Events)
    btn_load.click(
        load_wrapper, 
        inputs=input_img, 
        outputs=[output_ruler, output_object, state_object]
    )
    
    # Sự kiện click trên ảnh thước
    output_ruler.select(select_point)
    
    # Sự kiện tính tỷ lệ
    btn_calc.click(
        calc_mm_wrapper, 
        inputs=real_mm, 
        outputs=[output, state_mm]
    )

    # Sự kiện tính diện tích cuối cùng
    btn_area.click(
        get_object_area_gradio,
        inputs=[state_object, state_mm],
        outputs=objectArea
    )

if __name__ == "__main__":
    demo.launch(share=True)