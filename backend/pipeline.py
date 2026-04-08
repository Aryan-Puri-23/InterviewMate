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

    # score = int((speech_data["clarity"] + vision_data["confidence"]) / 2)

    # if speech_data["word_count"] == 0:
    #     score = 0

    filler_score = max(0, 100 - speech_data["filler_count"] * 3)

    if speech_data["word_count"] == 0:
        return {
            "score": 0,
            "communication": 0,
            "confidence": 0,
            "emotional": 0,
            "speech": speech_data,
            "emotion_timeline": []
        }

    else:
        score = min(
            100,
            int(
                (speech_data["clarity"] * 0.5) +
                (vision_data["confidence"] * 0.3) +
                (filler_score * 0.2)
            )
        )

        return {
            "score": score,

            # "communication": speech_data["clarity"],
            "communication": int(
                speech_data["clarity"] * 0.6 +
                filler_score * 0.4
            ),

            "confidence": vision_data["confidence"],

            # "emotional": 100 - vision_data["nervous"],
            "emotional": int(
                (100 - vision_data["nervous"]) * 0.7 +
                vision_data["confidence"] * 0.3
            ),

            # 🔥 ADD THESE (for your UI)
            "speech": {
                "word_count": speech_data["word_count"],
                "speech_rate": speech_data["speech_rate"],
                "filler_count": speech_data["filler_count"],
                "clarity": speech_data["clarity"]
            },

            "emotion_timeline": vision_data["timeline"]  # 🔥 IMPORTANT
        }



# from speech import analyze_speech
# from fuzzy import compute_score
# from vision import analyze_video

# def run_pipeline(video_path):

#     speech_data = analyze_speech(video_path)
#     vision_data = analyze_video(video_path)

#     # score = compute_score(
#     #     speech_data["clarity"],
#     #     vision_data["confidence"],
#     #     vision_data["eye_contact"]
#     # )

#     # score = int((speech_data["clarity"] + vision_data["confidence"]) / 2)
#     # if speech_data["word_count"] == 0:
#     #     score = 0

#     filler_score = max(0, 100 - speech_data["filler_count"] * 3)

#     if speech_data["word_count"] == 0:
#         return {
#         "score": 0,
#         "communication": 0,
#         "confidence": 0,
#         "emotional": 0,
#         "speech": speech_data,
#         "emotion_timeline": []
#     }
#     else:
#         score = min(100, int(
#             (speech_data["clarity"] * 0.5) +
#             (vision_data["confidence"] * 0.3) +
#             ((filler_score * 0.2))
#         ))

#     return {
#         "score": score,
#         # "communication": speech_data["clarity"],
#         "communication": int(
#             speech_data["clarity"] * 0.6 +
#             filler_score * 0.4
#         ),
#         "confidence": vision_data["confidence"],
#         # "emotional": 100 - vision_data["nervous"],
#         "emotional": int(
#             (100 - vision_data["nervous"]) * 0.7 +
#             vision_data["confidence"] * 0.3
#         ),

#         # 🔥 ADD THESE (for your UI)
#         "speech": {
#             "word_count": speech_data["word_count"],
#             "speech_rate": speech_data["speech_rate"],
#             "filler_count": speech_data["filler_count"],
#             "clarity": speech_data["clarity"]
#         },

#         "emotion_timeline": vision_data["timeline"]  # 🔥 IMPORTANT
#     }