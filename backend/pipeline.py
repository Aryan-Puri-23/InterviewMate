from speech import analyze_speech
from fuzzy import compute_score
from vision import analyze_video

def run_pipeline(video_path):

    speech_data = analyze_speech(video_path)
    vision_data = analyze_video(video_path)

    # score = compute_score(
    #     speech_data["clarity"],
    #     vision_data["confidence"],
    #     vision_data["eye_contact"]
    # )

    score = int((speech_data["clarity"] + vision_data["confidence"]) / 2)

    return {
        "score": score,
        "communication": speech_data["clarity"],
        "confidence": vision_data["confidence"],
        "emotional": 100 - vision_data["nervous"],

        # 🔥 ADD THESE (for your UI)
        "speech": {
            "word_count": speech_data["word_count"],
            "speech_rate": speech_data["speech_rate"],
            "filler_count": speech_data["filler_count"],
            "clarity": speech_data["clarity"]
        },

        "emotion_timeline": vision_data["timeline"]  # 🔥 IMPORTANT
    }