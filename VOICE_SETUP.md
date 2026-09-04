# Voice control setup

The program listens locally for the Chinese command `答题`. Once recognized, it
runs the same screenshot, OCR, AI answer, and clipboard workflow as the hotkey.

## One-time setup

1. Install Python 3.11 or 3.12. The existing `.venv` cannot be used because
   its Python 3.13 interpreter is no longer present on this computer.
2. In PowerShell, from this folder, create a new environment and install the
   project dependencies:

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   pip install sounddevice==0.5.5 vosk==0.3.45
   ```

3. Download `vosk-model-small-cn-0.22` from the Vosk models page and extract
   the folder directly under this project folder. Its final location must be:

   ```text
   D:\answer_bot\vosk-model-small-cn-0.22
   ```

4. Run `python answer_bot.py`, allow microphone access if Windows asks, then
   say `答题` clearly. The recognition and command trigger are offline.

The program ignores repeated triggers while a previous answer is being made.
Press `Esc` to exit; `Ctrl+Shift+Q` remains available as a backup.
