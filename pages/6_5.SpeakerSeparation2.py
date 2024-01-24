import streamlit as st
from pathlib import Path
from faster_whisper import WhisperModel
import re

import logging

logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)



def extract_speaker_id(filename):
    match = re.search(r"SPEAKER_\d+", filename)
    return match.group() if match else "Unknown"

# StreamlitのUI要素を設定
st.title("Whisperによる音声認識")

# ユーザー入力を受け取る
input_file = st.text_input("Input File Path", "./outputs/input.wav")
output_file = st.text_input("Output Text File Path", "./outputs/transcription.txt")
output_file_id = st.text_input("Output Text File Path", "./outputs/transcription_id.txt")

# 音声認識を実行するボタン
if st.button("音声認識を実行"):
    # model = WhisperModel("large-v3", device="cpu", compute_type="int8")     
    model = WhisperModel("large-v3", device="cuda", compute_type="float16")
    segments, info = model.transcribe(input_file, language="ja")

    # テキストファイルに結果を書き込み
    with open(output_file_id, "w") as f:
        for i, segment in enumerate(segments):
            f.write(f"[{i}] {segment.text}\n")
    
    # テキストファイルに結果を書き込み
    with open(output_file, "w") as f:
        for i, segment in enumerate(segments):
            f.write(f"{segment.text}\n")

    # 音声認識結果の表示
    for i, segment in enumerate(segments):
        st.write(f"[{i}] {segment.text}")
    
    st.success("音声認識が完了しました。")
    st.download_button("テキストファイルをダウンロード", data=open(output_file, "rb"), file_name=Path(output_file).name, mime="text/plain")
