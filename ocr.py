import pytesseract


def recognize_text(image):

    print("正在 OCR 识别题目...")

    text = pytesseract.image_to_string(
        image,
        lang="chi_sim+eng"
    )

    text = text.strip()

    if not text:
        raise RuntimeError(
            "OCR没有识别到文字"
        )

    print("\n========== 识别结果 ==========")
    print(text)
    print("==============================")

    return text