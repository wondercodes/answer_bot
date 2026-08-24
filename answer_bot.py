import keyboard
import pyperclip

from screenshot import capture_screen
from ocr import recognize_text
from models import LLMModel


class AnswerBot:

    def __init__(self):

        self.model = LLMModel()

        print(
            f"当前模型：{self.model.provider}"
        )

    def process(self):

        try:

            # ----------------------------------------
            # 1. 截图
            # ----------------------------------------

            image = capture_screen()


            # ----------------------------------------
            # 2. OCR
            # ----------------------------------------

            question = recognize_text(
                image
            )


            # ----------------------------------------
            # 3. 调用大模型
            # ----------------------------------------

            print(
                f"\n正在使用 {self.model.provider} 答题..."
            )

            answer = self.model.answer(
                question
            )


            # ----------------------------------------
            # 4. 输出
            # ----------------------------------------

            print(
                "\n========== AI答案 =========="
            )

            print(answer)

            print(
                "============================"
            )


            # ----------------------------------------
            # 5. 写入剪切板
            # ----------------------------------------

            pyperclip.copy(answer)

            print(
                "\n✓ 答案已经复制到 Windows 剪切板"
            )


        except Exception as e:

            print(
                f"\n[ERROR] {e}"
            )


def main():

    print(
        "======================================"
    )

    print(
        "       Windows AI Answer Bot"
    )

    print(
        "======================================"
    )

    bot = AnswerBot()

    print()
    print(
        "Ctrl + Shift + Q : 截图并答题"
    )

    print(
        "ESC              : 退出"
    )

    print()

    keyboard.add_hotkey(
        "ctrl+shift+q",
        bot.process
    )

    keyboard.wait(
        "esc"
    )


if __name__ == "__main__":
    main()