import os
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import whisper
from google import genai
import numpy as np


def m4a_to_text(audio_path, progress_var=None, progress_bar=None):
    try:
        model = whisper.load_model("medium.en")
        audio = whisper.load_audio(audio_path)
        audio_length = len(audio) / whisper.audio.SAMPLE_RATE

        segment_duration = 30
        num_segments = int(np.ceil(audio_length / segment_duration))

        full_text = ""
        for i in range(num_segments):
            start_sample = int(i * segment_duration * whisper.audio.SAMPLE_RATE)
            end_sample = int(min((i + 1) * segment_duration * whisper.audio.SAMPLE_RATE, len(audio)))
            segment = audio[start_sample:end_sample]
            segment = whisper.pad_or_trim(segment)
            mel = whisper.log_mel_spectrogram(segment).to(model.device)
            options = whisper.DecodingOptions(language="en")
            result = whisper.decode(model, mel, options)
            full_text += result.text + "\n"
            print(f"Processed {i + 1}/{num_segments} segments")

            # 음성 인식 진행률 (0~50%)
            if progress_var and progress_bar:
                progress = int(((i + 1) / num_segments) * 50)
                progress_var.set(progress)
                progress_bar.update()

        with open("transcription.txt", "w", encoding="utf-8") as f:
            f.write(full_text)

        return "transcription.txt"
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None


def translate_file(api_key, input_file, output_file, progress_var=None, progress_bar=None):
    try:
        client = genai.Client(api_key=api_key)
        with open(input_file, 'r', encoding='utf-8') as a, open(output_file, 'w', encoding='utf-8') as b:
            lines = a.readlines()
            total = len(lines)
            for idx, line in enumerate(lines):
                if line.strip():
                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents="뒤 문장들 한국어로 번역해줘 " + line
                    )
                    b.write(response.text + "\n\n")
                    #time.sleep(5)

                # 번역 진행률 (50~100%)
                if progress_var and progress_bar:
                    progress = 50 + int(((idx + 1) / total) * 50)
                    progress_var.set(progress)
                    progress_bar.update()

        messagebox.showinfo("Success", "Translation completed!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def start_translation():
    api_key = entry_api_key.get()
    audio_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.m4a")])
    if not audio_path:
        return

    button_translate.config(state="disabled", text="Processing...")
    progress_var.set(0)
    progress_bar.update()

    transcription_path = m4a_to_text(audio_path, progress_var, progress_bar)
    if transcription_path:
        translate_file(api_key, transcription_path, "final.txt", progress_var, progress_bar)

    button_translate.config(state="normal", text="Translate M4A")
    progress_var.set(0)


def start_translation_thread():
    threading.Thread(target=start_translation, daemon=True).start()


root = tk.Tk()
root.title("Whisper-Gemini Translator")
root.geometry("400x200")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True)

label_api_key = tk.Label(frame, text="Enter Gemini API Key:")
label_api_key.pack(pady=(0, 5))

entry_api_key = tk.Entry(frame, width=50)
entry_api_key.pack(pady=(0, 10))

button_translate = tk.Button(frame, text="Translate M4A", command=start_translation_thread)
button_translate.pack(pady=(0, 10))

progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(frame, variable=progress_var, maximum=100)
progress_bar.pack(pady=5, fill=tk.X)

root.mainloop()
