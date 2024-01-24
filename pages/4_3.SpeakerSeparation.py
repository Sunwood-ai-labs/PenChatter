import streamlit as st
import os
import re
from pathlib import Path
from pyannote.audio import Pipeline
from pydub import AudioSegment
import json
import torch
import pathlib
import torchaudio
from pyannote.audio.pipelines.utils.hook import ProgressHook

def millisec(timeStr):
    spl = timeStr.split(":")
    s = int((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2])) * 1000)
    return s

def extract_speaker_name(segment):
    # 話者名を抽出する正規表現
    match = re.search(r'SPEAKER_[0-9]+', segment)
    if match:
        return match.group()
    return "Unknown"

# 環境変数からHF_AUTH_TOKENを取得
HF_AUTH_TOKEN = os.getenv('HF_AUTH_TOKEN')
os.environ['HUGGINGFACE_HUB_CACHE'] = str(pathlib.Path("./Assets").absolute())


# UIの設定
st.title("PyannoteとWhisperによる話者分離と音声認識")

# 入出力フォルダの設定
input_folder = st.text_input("Input Folder Path", "./outputs/")
output_folder = st.text_input("Output Folder Path", "./outputs/speaker/")
input_file_name = st.text_input("Input File Name", "input_prep.wav")
diarization_file_name = st.text_input("Diarization Output File Name", "diarization.txt")

input_file_path = Path(input_folder) / input_file_name
diarization_file_path = Path(output_folder) / diarization_file_name

os.makedirs(output_folder, exist_ok=True)

# 話者分離の実行ボタン
if st.button("話者分離を実行"):


    # PyannoteのPipelineを初期化
    # pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token=HF_AUTH_TOKEN)
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=HF_AUTH_TOKEN)
    # pipeline = Pipeline.from_pretrained("./Assets/config.yaml", use_auth_token=HF_AUTH_TOKEN)
    # st.write(pipeline)
    # send pipeline to GPU (when available)
    pipeline.to(torch.device("cuda"))

    waveform, sample_rate = torchaudio.load(str(input_file_path))
    
    with ProgressHook() as hook:
        dz = pipeline({"waveform": waveform, "sample_rate": sample_rate}, hook=hook, min_speakers=2)
        st.write(dz)

    # 結果をテキストファイルに保存
    with open(diarization_file_path, "w") as text_file:
        text_file.write(str(dz))

    # 結果を画面に表示
    diarization_result = list(dz.itertracks(yield_label=True))[:10]
    for track in diarization_result:
        st.write(track)

    with open("result_rttm.txt", "wt") as f:
        # diarization.write_lab(f)
        dz.write_rttm(f)


# 話者のグルーピングと音声ファイルの分割
if st.button("音声ファイルを分割"):
    diarization_file_path = Path(output_folder) / diarization_file_name
    if not diarization_file_path.is_file():
        st.error("Diarizationファイルが見つかりません。")
    else:
        # 話者のグルーピング
        dzs = open(diarization_file_path).read().splitlines()
        groups = []
        g = []
        lastend = 0

        for d in dzs:
            if g and (g[0].split()[-1] != d.split()[-1]):  # same speaker
                groups.append(g)
                g = []

            g.append(d)

            end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=d)[1]
            end = millisec(end)
            if lastend > end:  # segment engulfed by a previous segment
                groups.append(g)
                g = []
            else:
                lastend = end
        if g:
            groups.append(g)

        # 音声ファイルの分割と保存
        audio = AudioSegment.from_wav(str(input_file_path))
        progress_bar = st.progress(0)
        for i, group in enumerate(groups):
            # 各セグメントの開始と終了時間を計算
            st.write(f"segment : {i}")
            st.write(group)
            speaker_name = extract_speaker_name(group[0])
            segment_start = millisec(re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=group[0])[0])
            segment_end = millisec(re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=group[-1])[1])
            segment = audio[segment_start:segment_end]
            segment_file_path = Path(output_folder) / f"{i:03d}_{speaker_name}.wav"
            segment.export(segment_file_path, format='wav')
            progress_bar.progress((i + 1) / len(groups))

        st.success("音声ファイルの分割が完了しました。")