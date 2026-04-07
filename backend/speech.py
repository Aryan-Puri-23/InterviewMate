import whisper
from moviepy.editor import VideoFileClip

model = whisper.load_model("tiny")

FILLER_WORDS = ["um", "uh", "like", "you know", "basically", "actually"]

def analyze_speech(video_path):

    # 🎯 extract audio
    # audio_path = video_path.replace(".mp4", ".wav")
    audio_path = video_path.split(".")[0] + ".wav"

    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, logger=None)
    clip.close()   # 🔥 ADD THIS

    # 🎯 speech to text
    result = model.transcribe(audio_path)
    text = result["text"].lower()

    words = text.split()
    word_count = len(words)

    duration = result["segments"][-1]["end"] if result["segments"] else 1

    # 🎯 REAL speech rate
    speech_rate = int((word_count / duration) * 60)

    # 🎯 REAL filler detection
    filler_count = sum(text.count(f) for f in FILLER_WORDS)

    # 🎯 clarity (simple but meaningful)
    clarity = max(0, 100 - filler_count * 2)

    return {
        "word_count": word_count,
        "speech_rate": speech_rate,
        "filler_count": filler_count,
        "clarity": clarity
    }