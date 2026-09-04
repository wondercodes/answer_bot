import json
import queue
import threading
from pathlib import Path

import keyboard
import pyperclip
import sounddevice as sd
from vosk import KaldiRecognizer, Model

from ocr import recognize_text
from models import LLMModel
from screenshot import capture_screen


class AnswerBot:
    def __init__(self):
        self.model = LLMModel()
        self.is_processing = threading.Lock()
        print(f"Current model: {self.model.provider}")

    def process(self):
        """Capture the primary screen, answer its question, and copy the result."""
        if not self.is_processing.acquire(blocking=False):
            print("Answering is already in progress; command ignored.")
            return

        try:
            image = capture_screen()
            #question = recognize_text(image)
            print(f"\nAnswering with {self.model.provider}...")
            #answer = self.model.answer(question)
            answer = self.model.image_to_answer(image)
            print("\n========== AI Answer ==========")
            print(answer)
            print("===============================")
            pyperclip.copy(answer)
            print("\nAnswer copied to the Windows clipboard.")
        except Exception as error:
            print(f"\n[ERROR] {error}")
        finally:
            self.is_processing.release()


class VoiceCommandListener:
    """Offline microphone listener that triggers a callback when it hears '答题'."""

    def __init__(self, command_callback, model_path=None):
        self.command_callback = command_callback
        self.model_path = model_path or Path(__file__).with_name("vosk-model-small-cn-0.22")
        self.audio_queue = queue.Queue()

    def _on_audio(self, indata, frames, time, status):
        if status:
            print(f"Microphone status: {status}")
        self.audio_queue.put(bytes(indata))

    def listen_forever(self):
        try:
            model = Model(str(self.model_path))
        except Exception as error:
            print(
                "Voice model not found. Download the Chinese Vosk model and extract it "
                "next to this script as 'vosk-model-small-cn-0.22'."
            )
            print(f"Voice listener disabled: {error}")
            return

        device_info = sd.query_devices(kind="input")
        sample_rate = int(device_info["default_samplerate"])
        recognizer = KaldiRecognizer(model, sample_rate)
        print("Voice control is ready. Say '答题' to capture the screen and answer.")

        with sd.RawInputStream(
            samplerate=sample_rate,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self._on_audio,
        ):
            while True:
                audio_data = self.audio_queue.get()
                if not recognizer.AcceptWaveform(audio_data):
                    continue
                text = json.loads(recognizer.Result()).get("text", "")
                if "答题" in text.replace(" ", ""):
                    print("Voice command received: 答题")
                    threading.Thread(target=self.command_callback, daemon=True).start()


def main():
    print("======================================")
    print("       Windows AI Answer Bot")
    print("======================================")

    bot = AnswerBot()
    print("Ctrl + Shift + Q : capture screen and answer")
    print("Say '答题'        : capture screen and answer")
    print("ESC               : exit")

    keyboard.add_hotkey("ctrl+shift+q", bot.process)
    listener = VoiceCommandListener(bot.process)
    threading.Thread(target=listener.listen_forever, daemon=True).start()
    keyboard.wait("esc")


if __name__ == "__main__":
    main()
