# 🎤 Language Translator 🎧

This Gradio app lets you **translate text or speech into another language** and **hear it spoken aloud** using:

- 🌍 **NLLB-200** (No Language Left Behind) for multilingual translation
- 🗣️ **gTTS (Google Text-to-Speech)** for speech synthesis
- 🧠 **LangDetect** and **SpeechRecognition** for language and voice input

---

## 🚀 Features

- 🔤 **Text Translation**: Type in any sentence and get a translation with audio output.
- 🎙️ **Voice Input**: Speak into your mic and get your speech transcribed, translated, and read back.
- 🧠 **Automatic Language Detection** for source text.
- 🌐 Supports **60+ Languages** (based on gTTS support + NLLB).

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| 🤗 `transformers` | Translation using `facebook/nllb-200-distilled-600M` |
| 🗣️ `gTTS` | Text-to-speech synthesis |
| 🎧 `speech_recognition` | Converts audio input into text |
| 🌍 `langdetect` + `langcodes` | Detects source language |
| 🎛️ `gradio` | Web UI framework for the app |

---

## 🌈 How to Use

1. Select the **Text Input** or **Voice Input** tab.
2. Enter text or speak into the mic.
3. Choose the target language.
4. Click **Translate**.
5. View the **detected language**, **translated text**, and play the **audio output**.

---

## 📦 Model Details

- 🔄 Translation: `facebook/nllb-200-distilled-600M`
  - Optimized for performance (smaller than full NLLB-200).
  - Accepts `src_lang` and `tgt_lang` codes like `eng_Latn`, `fra_Latn`, etc.

- 🎤 Text-to-Speech: `gTTS`
  - Converts translated text to speech for supported languages.

---

## ⚠️ Limitations

- **Performance may be slow** on Hugging Face free-tier CPUs. For better speed:
  - Run locally.
  - Use shorter text/audio.
- `gTTS` requires internet and may fail if rate-limited or offline.
- Not all NLLB languages are supported in `gTTS`.

---

## 📚 Credits

- Translation Model: [Meta AI - NLLB-200](https://huggingface.co/facebook/nllb-200-distilled-600M)
- TTS: [gTTS](https://pypi.org/project/gTTS/)
- Voice to Text: [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- UI: [Gradio](https://gradio.app)

---

## 🧪 Try It Out

Click the [here](https://huggingface.co/spaces/Devligan/Multilingual_AI_Translator) and give it a try!


Check out the configuration reference [here](https://huggingface.co/docs/hub/spaces-config-reference)
