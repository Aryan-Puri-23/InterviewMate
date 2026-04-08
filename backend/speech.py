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
    clip.close()  # 🔥 ADD THIS

    # 🎯 speech to text
    result = model.transcribe(audio_path)

    # text = result["text"].lower()
    # words = text.split()

    # if word_count == 0 and len(text.strip()) > 0:
    #     word_count = len(text.strip().split())

    # word_count = len(words)

    text = result["text"].lower()
    words = text.split()

    word_count = len(words)   # 🔥 define first

    if word_count == 0 and len(text.strip()) > 0:
        word_count = len(text.strip().split())

    # duration = result["segments"][-1]["end"] if result["segments"] else 1
    duration = result["segments"][-1]["end"] if result["segments"] else 1

    if duration <= 0:
        duration = 1

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


# import whisper
# from moviepy.editor import VideoFileClip

# model = whisper.load_model("tiny")

# FILLER_WORDS = ["um", "uh", "like", "you know", "basically", "actually"]

# def analyze_speech(video_path):

#     # 🎯 extract audio
#     # audio_path = video_path.replace(".mp4", ".wav")
#     audio_path = video_path.split(".")[0] + ".wav"

#     clip = VideoFileClip(video_path)
#     clip.audio.write_audiofile(audio_path, logger=None)
#     clip.close()   # 🔥 ADD THIS

#     # 🎯 speech to text
#     result = model.transcribe(audio_path)
#     text = result["text"].lower()

#     words = text.split()
#     word_count = len(words)

#     duration = result["segments"][-1]["end"] if result["segments"] else 1

#     # 🎯 REAL speech rate
#     speech_rate = int((word_count / duration) * 60)

#     # 🎯 REAL filler detection
#     filler_count = sum(text.count(f) for f in FILLER_WORDS)

#     # 🎯 clarity (simple but meaningful)
#     clarity = max(0, 100 - filler_count * 2)

#     return {
#         "word_count": word_count,
#         "speech_rate": speech_rate,
#         "filler_count": filler_count,
#         "clarity": clarity
#     }