import streamlit as st
from pydub import AudioSegment
from pathlib import Path

# UIの設定
st.title("音声の前処理")
st.write("音声ファイルをトリミングしてから無音区間を追加")

# ユーザー入力
input_folder = st.text_input("Input Folder Path", "./outputs/")
input_file_name = st.text_input("Input File Name", "input.wav")
audio_length = 0


input_file = Path(input_folder) / input_file_name
if not input_file.is_file():
    st.error("入力ファイルが見つかりません。")
else:
    audio = AudioSegment.from_wav(input_file)
    audio_length = len(audio)
    st.success(f"ファイル読み込み成功: 長さは {audio_length} ミリ秒です。")

# トリミング設定
trim_start = st.number_input("トリミング開始時間（ミリ秒）", min_value=0, value=0, step=100)
trim_end = st.number_input("トリミング終了時間（ミリ秒）", min_value=0, value=audio_length, step=100)
output_folder = st.text_input("Output Folder Path", "./outputs/")
output_file_name = st.text_input("Output File Name", "input_prep.wav")
spacer_milli = st.number_input("無音区間の長さ（ミリ秒）", min_value=0, value=2000, step=100)

# 処理実行ボタン
if st.button("処理実行"):
    output_file = Path(output_folder) / output_file_name
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    input_file = Path(input_folder) / input_file_name
    audio = AudioSegment.from_wav(input_file)
    # トリミング
    audio = audio[trim_start:trim_end]

    # 無音区間を追加
    spacer = AudioSegment.silent(duration=spacer_milli)
    audio_with_spacer = spacer.append(audio, crossfade=0)

    # 結果を出力ファイルに保存
    audio_with_spacer.export(output_file, format='wav')

    # 生成された音声ファイルを再生
    audio_file = open(output_file, "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/wav')
