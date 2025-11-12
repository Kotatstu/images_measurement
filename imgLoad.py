# Load và tiền xử lý ảnh
# Mục tiêu là giảm nhiễu, xác định contour chính xác hơn

# Resize ảnh.
# Chuyển sang grayscale
# Gaussian blur
# Làm tăng tương phản nếu cần: CLAHE (cv2.createCLAHE()).
# Edge detection: Canny (cv2.Canny(blurred, 50, 150)), hoặc threshold (adaptive).