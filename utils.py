from pydub import AudioSegment

def get_loudness(file_path):
    """指定された音声ファイルの平均音量（dBFS）を取得する。

    Args:
        file_path (str): 音声ファイルのパス

    Returns:
        float: 音声ファイルの平均音量（dBFS）
    """
    audio = AudioSegment.from_file(file_path)
    return audio.dBFS

# 音量を計算
loudness_input = get_loudness("./input.wav")
loudness_mix_headset = get_loudness("./ES2004a.Mix-Headset.wav")

print("input.wavの音量（dBFS）:", loudness_input)
print("ES2004a.Mix-Headset.wavの音量（dBFS）:", loudness_mix_headset)


def adjust_loudness(file_path, target_dBFS=-36):
    """指定された音声ファイルの音量を指定されたdBFSに調整する。

    Args:
        file_path (str): 音声ファイルのパス
        target_dBFS (float): 目標とする音量（dBFS）

    Returns:
        AudioSegment: 音量が調整された音声データ
    """
    audio = AudioSegment.from_file(file_path)
    change_in_dBFS = target_dBFS - audio.dBFS
    return audio.apply_gain(change_in_dBFS)

# 例：音量を-36 dBFSに調整
adjusted_audio = adjust_loudness("./input.wav", -36)

# 調整された音声ファイルを保存
adjusted_audio.export("./input_adjusted.wav", format="wav")