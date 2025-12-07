# Các bước chính:
# 1. Ảnh đầu vào gồm 1 vật thể mình muốn đo và 1 thước chuẩn để làm mốc tính pixel -> mm. Đọc ảnh và tiền xử lý ảnh.
# 2. Đọc cái thước chuẩn
# 3. Calibration để chuẩn hóa về 1 mặt phẳng, đo chính xác hơn
# 4. Phát hiện được vật thể ở đâu trên hình
# 5. Tính diện tích của vật thể sau khi xác định kích thước chuẩn và vật thể
# 6. Chạy main.py, hiển thị kết quả

import cv2
import numpy as np
import gradio as gr


from imgLoad import loadImage, load_image_gradio
from scaleCalibration import show_ruler_and_get_scale, select_point, calc_mm_per_pixel, calc_mm_value
from objectContour import getFilledContourMask
from pixelToMM import get_object_area, get_object_area_gradio

# ======================= PIPELINE Cũ ========================
# # Load và xử lý ảnh đầu vào
# ruler, obj, full = loadImage("./imgs/earphone2.jpg")
# # print("Kich thuoc anh thuoc: ", ruler.size)
# # print("Kich thuoc anh vat the: ", obj.size)
# # print("Kich thuoc anh full", full.size)

# cv2.imshow("Anh vat the", obj)
# cv2.waitKey(0)


# # Tính giá trị mm mỗi pixel
# mmPerPixel = show_ruler_and_get_scale(ruler)


# # Tìm contour
# mask = getFilledContourMask(obj)


# # Tính diện tích vật thể
# objectArea = get_object_area(mask, mmPerPixel)
# print("Dien tich vat the:", objectArea, "mm2")


# contourImg = cv2.resize(mask, (500, 500))
# cv2.imshow("Contour", contourImg)
# cv2.waitKey(0)


# cv2.destroyAllWindows()

#=========================== Giao diện gradio ============================
with gr.Blocks() as demo:
    with gr.Row():
        input_img = gr.Image(label="Upload ảnh", type="pil")

    btn_load = gr.Button("Tách ảnh ruler và object")
    state_object = gr.State()
    state_mm = gr.State()

    with gr.Row():
        output_ruler = gr.Image(label="Ruler", type="numpy")
        output_object = gr.Image(label="Object", type="numpy")

    # Bước tính mm mỗi pixel
    gr.Markdown("Chọn đúng 2 điểm trên thước để tính mm mỗi pixel")
    real_mm = gr.Number(label="Nhập chiều dài thật (mm)")
    btn_calc = gr.Button("Tính mm/pixel")
    output = gr.Textbox(label="Kết quả")

    # Debug state
    # gr.Markdown("### DEBUG STATE")
    # debug_btn = gr.Button("Xem dữ liệu state")
    # debug_object = gr.Textbox(label="State Object (info)")
    # debug_mm = gr.Textbox(label="State mm_per_pixel")

    # Tính diện tích
    btn_area = gr.Button("Tính diện tích")
    gr.Markdown("Diện tích vật thể")
    objectArea = gr.Textbox(label="Diện tích vật thể (mm2)")

    # =========================== Hàm bọc và EVENTS =====================
    def load_wrapper(img):
        ruler, obj = load_image_gradio(img)
        return ruler, obj, obj
    
    def calc_mm_wrapper(real_mm):
        text_info = calc_mm_per_pixel(real_mm)
        mm_value = calc_mm_value(real_mm)
        return text_info, mm_value
    
    # def debug_state(obj, mm):
    #     obj_info = "None"
    #     mm_info = "None"

    #     if obj is not None and isinstance(obj, np.ndarray):
    #         obj_info = f"Type: numpy.ndarray\nShape: {obj.shape}\nDtype: {obj.dtype}"
        
    #     if mm is not None:
    #         mm_info = f"{mm}"

    #     return obj_info, mm_info

    # Các events
    btn_load.click(
        load_wrapper, 
        inputs=input_img, 
        outputs=[output_ruler, output_object, state_object]
    )
    
    output_ruler.select(select_point)
    
    btn_calc.click(
        calc_mm_wrapper, 
        inputs=real_mm, 
        outputs=[output, state_mm]
    )

    # # Ấn debug để xem state đang chứa gì
    # debug_btn.click(
    #     debug_state,
    #     inputs=[state_object, state_mm],
    #     outputs=[debug_object, debug_mm]
    # )

    # Tính diện tích sau khi nhấn "Tính mm/pixel"
    btn_area.click(
        get_object_area_gradio,
        inputs=[state_object, state_mm],
        outputs=objectArea
    )

demo.launch(share=True)
