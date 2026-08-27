import os
import re

# Fix PaddlePaddle + oneDNN/PIR issue on Windows
os.environ["FLAGS_enable_pir_api"] = "0"

from paddleocr import PaddleOCR
import cv2


# ==========================================
# OCR INITIALIZATION
# ==========================================

ocr = PaddleOCR(
    lang="en",
    enable_mkldnn=False
)


# ==========================================
# READ IMAGE
# ==========================================

image_path = "plate_test.png"

image = cv2.imread(image_path)

if image is None:
    print("ERROR: Could not read plate_test.png")
    exit()


# ==========================================
# OCR
# ==========================================

print("Running OCR...")

result = ocr.predict(image)


# ==========================================
# EXTRACT TEXT
# ==========================================

for res in result:

    texts = res.get("rec_texts", [])
    scores = res.get("rec_scores", [])

    print("\nDETECTED TEXT")
    print("=" * 40)

    for text, score in zip(texts, scores):

        print(
            f"{text}  "
            f"(confidence: {score:.2f})"
        )


    # ======================================
    # COMBINE TEXT
    # ======================================

    combined_text = ""

    for text in texts:

        # Remove spaces/special characters
        cleaned = re.sub(
            r"[^A-Z0-9]",
            "",
            text.upper()
        )

        # Ignore IND
        if cleaned == "IND":
            continue

        combined_text += cleaned


    print("\nNORMALIZED PLATE")
    print("=" * 40)

    print(combined_text)