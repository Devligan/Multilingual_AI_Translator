import gradio as gr
from transformers import pipeline
from langdetect import detect
from langcodes import Language
from gtts import gTTS
import tempfile
import speech_recognition as sr

# Initialize translation pipeline
tranPipe = pipeline("translation", model="facebook/nllb-200-distilled-600M")

# Complete list of languages supported by gTTS with their codes
GTTS_LANGUAGES = {
    'Afrikaans': 'af',
    'Arabic': 'ar',
    'Bulgarian': 'bg',
    'Bengali': 'bn',
    'Bosnian': 'bs',
    'Catalan': 'ca',
    'Czech': 'cs',
    'Welsh': 'cy',
    'Danish': 'da',
    'German': 'de',
    'Greek': 'el',
    'English': 'en',
    'Spanish': 'es',
    'Estonian': 'et',
    'Finnish': 'fi',
    'French': 'fr',
    'Gujarati': 'gu',
    'Hindi': 'hi',
    'Croatian': 'hr',
    'Hungarian': 'hu',
    'Indonesian': 'id',
    'Icelandic': 'is',
    'Italian': 'it',
    'Hebrew': 'iw',
    'Japanese': 'ja',
    'Javanese': 'jw',
    'Khmer': 'km',
    'Kannada': 'kn',
    'Korean': 'ko',
    'Latin': 'la',
    'Latvian': 'lv',
    'Malayalam': 'ml',
    'Marathi': 'mr',
    'Malay': 'ms',
    'Burmese': 'my',
    'Nepali': 'ne',
    'Dutch': 'nl',
    'Norwegian': 'no',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Sinhala': 'si',
    'Slovak': 'sk',
    'Albanian': 'sq',
    'Serbian': 'sr',
    'Sundanese': 'su',
    'Swedish': 'sv',
    'Swahili': 'sw',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Thai': 'th',
    'Filipino': 'tl',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Vietnamese': 'vi',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Mandarin/Taiwan)': 'zh-TW',
    'Chinese (Mandarin)': 'zh'
}

# Mapping from gTTS languages to NLLB language codes
GTTS_TO_NLLB = {
    'Afrikaans': 'afr_Latn',
    'Arabic': 'arb_Arab',
    'Bulgarian': 'bul_Cyrl',
    'Bengali': 'ben_Beng',
    'Bosnian': 'bos_Latn',
    'Catalan': 'cat_Latn',
    'Czech': 'ces_Latn',
    'Welsh': 'cym_Latn',
    'Danish': 'dan_Latn',
    'German': 'deu_Latn',
    'Greek': 'ell_Grek',
    'English': 'eng_Latn',
    'Spanish': 'spa_Latn',
    'Estonian': 'est_Latn',
    'Finnish': 'fin_Latn',
    'French': 'fra_Latn',
    'Gujarati': 'guj_Gujr',
    'Hindi': 'hin_Deva',
    'Croatian': 'hrv_Latn',
    'Hungarian': 'hun_Latn',
    'Indonesian': 'ind_Latn',
    'Icelandic': 'isl_Latn',
    'Italian': 'ita_Latn',
    'Hebrew': 'heb_Hebr',
    'Japanese': 'jpn_Jpan',
    'Javanese': 'jav_Latn',
    'Khmer': 'khm_Khmr',
    'Kannada': 'kan_Knda',
    'Korean': 'kor_Hang',
    'Latin': 'lat_Latn',
    'Latvian': 'lvs_Latn',
    'Malayalam': 'mal_Mlym',
    'Marathi': 'mar_Deva',
    'Malay': 'zsm_Latn',
    'Burmese': 'mya_Mymr',
    'Nepali': 'npi_Deva',
    'Dutch': 'nld_Latn',
    'Norwegian': 'nno_Latn',
    'Polish': 'pol_Latn',
    'Portuguese': 'por_Latn',
    'Romanian': 'ron_Latn',
    'Russian': 'rus_Cyrl',
    'Sinhala': 'sin_Sinh',
    'Slovak': 'slk_Latn',
    'Albanian': 'sqi_Latn',
    'Serbian': 'srp_Cyrl',
    'Sundanese': 'sun_Latn',
    'Swedish': 'swe_Latn',
    'Swahili': 'swh_Latn',
    'Tamil': 'tam_Taml',
    'Telugu': 'tel_Telu',
    'Thai': 'tha_Thai',
    'Filipino': 'tgl_Latn',
    'Turkish': 'tur_Latn',
    'Ukrainian': 'ukr_Cyrl',
    'Urdu': 'urd_Arab',
    'Vietnamese': 'vie_Latn',
    'Chinese (Simplified)': 'zho_Hans',
    'Chinese (Mandarin/Taiwan)': 'zho_Hant',
    'Chinese (Mandarin)': 'zho_Hans'
}

'''
    Purpose: Detects the language of a given text
    Paramaters:
        {text}: The statement that requires translation
    Return:
        {code}: Language Code for NLLB translation
        {lang.display_name()}: Standard name for language
        OR
        NLLB as English
        Display Name as "Unknown"
'''
def lang_code(text):
    try:
        detected = detect(text)
        lang = Language.get(detected)
        script = lang.script or "Latn"  # Default to Latin script if not specified
        code = f"{lang.language}_{script}"
        return code, lang.display_name()
    except:
        return "eng_Latn", "Unknown"

'''
    Purpose: Converts speech from an audio file to text using Google's speech recognition API
    Parameters:
        {audio}: Path to an audio file (WAV/AIFF/FLAC format) containing speech
    Return:
        {text}: Transcribed text if successful
        OR
        {error_message}: If audio is unintelligible ("Could not understand audio") 
                        or API request fails ("Could not request results")
'''
def speech_to_text(audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Could not request results (check internet)"

'''
    Purpose: Translates text to a target language and generates speech output
    Parameters:
        {text}: Input text to be translated (str)
        {tgt_lang}: User-selected target language name (e.g., "French") (str)
    Returns:
        {lang_name}: Detected source language name (str)
        {translated_text}: Translated text content (str)
        {audio_path}: Path to generated speech file (None if generation fails) (str/None)
        OR
        {"Error"}: Error indicator (str)
        {error_msg}: Description of failure (str)
        {None}: Placeholder for failed audio
'''
def translate(text, tgt_lang):
    if not text.strip():
        return "Error", "No text provided", None

    src_lang, lang_name = lang_code(text)
    try:
        # Get NLLB target language code
        tgt_lang_code = GTTS_TO_NLLB.get(tgt_lang, "eng_Latn")

        # Perform translation
        result = tranPipe(text, src_lang=src_lang, tgt_lang=tgt_lang_code)
        translated_text = result[0]['translation_text']

        # Generate speech using gTTS
        audio_path = None
        if tgt_lang in GTTS_LANGUAGES:
            try:
                tts = gTTS(text=translated_text, lang=GTTS_LANGUAGES[tgt_lang])
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(temp_file.name)
                audio_path = temp_file.name
            except Exception as e:
                print(f"Could not generate speech: {str(e)}")

        return lang_name, translated_text, audio_path
    except Exception as e:
        return "Error", f"Could not translate: {str(e)}", None

#Setup for GUI
with gr.Blocks() as app:
    gr.Markdown("# 🎤 Language Translator 🎧")
    gr.Markdown("Supports all gTTS languages with NLLB translation")

    with gr.Tab("Text Input"):
        with gr.Row():
            text_input = gr.Textbox(lines=2, placeholder="Type here...", label="Input Text")
            tgt_lang_text = gr.Dropdown(choices=list(GTTS_LANGUAGES.keys()), label="Target Language", value="English")
        translate_btn_text = gr.Button("Translate (Text)")

        with gr.Row():
            detected_lang_text = gr.Label(label="Detected Language")
            translated_text_text = gr.Textbox(label="Translation")
            audio_output_text = gr.Audio(label="Speech Output", autoplay=False)

    with gr.Tab("Voice Input"):
        with gr.Row():
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Speak Now")
            tgt_lang_voice = gr.Dropdown(choices=list(GTTS_LANGUAGES.keys()), label="Target Language", value="English")
        translate_btn_voice = gr.Button("Translate (Voice)")

        with gr.Row():
            detected_lang_voice = gr.Label(label="Detected Language")
            translated_text_voice = gr.Textbox(label="Translation")
            audio_output_voice = gr.Audio(label="Speech Output", autoplay=False)

    # Text translation
    translate_btn_text.click(
        fn=translate,
        inputs=[text_input, tgt_lang_text],
        outputs=[detected_lang_text, translated_text_text, audio_output_text]
    )

    # Voice translation
    translate_btn_voice.click(
        fn=lambda audio, lang: translate(speech_to_text(audio), lang),
        inputs=[audio_input, tgt_lang_voice],
        outputs=[detected_lang_voice, translated_text_voice, audio_output_voice]
    )

app.launch()