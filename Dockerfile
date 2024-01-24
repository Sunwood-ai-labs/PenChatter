# 基本イメージをCUDA互換のものにする
# FROM python:3.10.13-slim-bookworm
FROM nvcr.io/nvidia/pytorch:23.12-py3

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y python3-pip git

# WhisperとPyannote、Streamlitをインストール
RUN pip3 install git+https://github.com/openai/whisper.git
RUN pip3 install pyannote.audio
RUN pip3 install streamlit
RUN pip3 install yt_dlp
RUN pip install pydub
RUN pip install torchaudio
RUN pip install faster_whisper

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get -y install ffmpeg
# Streamlitのデフォルトポートを開放
EXPOSE 8501

# Streamlitアプリケーションの実行
# CMD ["streamlit", "run", "app.py"]