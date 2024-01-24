import streamlit as st
from pathlib import Path
from faster_whisper import WhisperModel
import re

def extract_speaker_id(filename):
    match = re.search(r"SPEAKER_\d+", filename)
    return match.group() if match else "Unknown"

# StreamlitのUI要素を設定
st.title("Whisperによる音声認識")

# ユーザー入力を受け取る
input_folder = st.text_input("Input Folder Path", "./outputs/speaker/")

# 音声認識を実行するボタン
if st.button("音声認識を実行"):
    model = WhisperModel("large-v3", device="cpu", compute_type="int8")

    # 指定されたフォルダから.wavファイルを読み込み、ソート
    wav_files = sorted(Path(input_folder).glob("*.wav"))
    
    # プログレスバーの設定
    progress_bar = st.progress(0)
    total_files = len(wav_files)

    for i, file_path in enumerate(wav_files):
        speaker_id = extract_speaker_id(file_path.name)
        segments, info = model.transcribe(str(file_path), language="ja")

        # 音声認識結果の表示
        st.write(f"---")
        st.write(f"**File: {file_path.name} (Speaker ID: {speaker_id}):**")
        for segment in segments:
            st.write(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

        # プログレスバーの更新
        progress_bar.progress((i + 1) / total_files)

    st.success("音声認識が完了しました。")
