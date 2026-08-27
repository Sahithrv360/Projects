import os

# Fix PaddlePaddle + oneDNN/PIR issue on Windows
os.environ["FLAGS_enable_pir_api"] = "0"

from paddleocr import PaddleOCR
import cv2


# Initialize OCR
ocr = PaddleOCR(
    lang="en",
    enable_mkldnn=False
)


# Test image
image_path = "plate_test.png"

image = cv2.imread(image_path)

if image is None:
    print("ERROR: Could not read plate_test.jpg")
    exit()


print("Running OCR...")

result = ocr.predict(image)


print("\nOCR RESULT")
print("=" * 50)

for res in result:

    print(res)