import streamlit as st
from yt_dlp import YoutubeDL
from pathlib import Path
import os

# StreamlitのUI要素を設定
st.title("YouTube動画のダウンロードと音声変換")

# ユーザー入力を受け取る
video_url = st.text_input("YouTube Video URL", "https://www.youtube.com/watch?v=ZhoE5d41ofM")
output_path = st.text_input("Output Path", "./outputs/")
output_file_name = st.text_input("Output File Name", "input.wav")

# ダウンロードボタン
if st.button("Download and Convert Video"):
    output_path = str(Path(output_path))
    output_file = Path(output_path) / output_file_name
    Path(output_path).mkdir(parents=True, exist_ok=True)

    # 既存のファイルがあれば削除
    if output_file.is_file():
        os.remove(output_file)

    # YouTube動画の情報を取得
    with YoutubeDL() as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        video_title = info_dict.get('title', None)
        video_id = info_dict.get('id', None)
        st.write(f"Title: {video_title}")

    # YouTube動画をダウンロードし、音声を指定されたファイル名で保存
    os.system(f"yt-dlp -x --audio-format wav -o '{output_file}' -- {video_url}")

    # 生成された音声ファイルを再生
    if output_file.is_file():
        audio_file = open(output_file, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav')
    else:
        st.error("音声ファイルの生成に失敗しました。")