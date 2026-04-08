import cv2
from deepface import DeepFace
from collections import deque


def analyze_video(video_path):

    cap = cv2.VideoCapture(video_path)

    total_frames = 0
    confidence_scores = []
    nervous_scores = []
    timeline = []

    window = deque(maxlen=5)

    # fps = cap.get(cv2.CAP_PROP_FPS) or 30
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # if not fps or fps < 10:
    #     fps = 30

    fps = cap.get(cv2.CAP_PROP_FPS)
    fps = int(fps) if fps and fps > 0 else 30

    window_nerv = deque(maxlen=5)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        total_frames += 1

        try:
            result = DeepFace.analyze(
                frame,
                actions=['emotion'],
                enforce_detection=False,
                silent=True
            )

            # emotion = result[0]["dominant_emotion"]

            # 🎯 map emotion → confidence/nervous
            # if emotion in ["happy", "neutral"]:
            #     confidence = 80
            #     nervous = 20
            # else:
            #     confidence = 50
            #     nervous = 50

            emotion_scores = result[0]["emotion"]
            total = sum(emotion_scores.values()) or 1

            positive = (
                emotion_scores.get("happy", 0) +
                emotion_scores.get("neutral", 0)
            )
            confidence = int((positive / total) * 100)

            # nervous = int(
            #     emotion_scores.get("fear", 0) +
            #     emotion_scores.get("sad", 0) +
            #     emotion_scores.get("angry", 0)
            # )

            negative = (
                emotion_scores.get("fear", 0) +
                emotion_scores.get("sad", 0) +
                emotion_scores.get("angry", 0) +
                emotion_scores.get("disgust", 0)
            )
            nervous = int((negative / total) * 100)

        except:
            confidence = 50
            nervous = 50

        # confidence_scores.append(confidence)
        window.append(confidence)
        smooth_conf = int(sum(window) / len(window))
        confidence_scores.append(smooth_conf)

        # nervous_scores.append(nervous)
        window_nerv.append(nervous)
        smooth_nerv = int(sum(window_nerv) / len(window_nerv))
        nervous_scores.append(smooth_nerv)

        # if total_frames % 30 == 0:
        # if total_frames % 60 == 0:
        # timeline.append({
        #     "time": f"{int(total_frames/30)}s",

        if total_frames % int(fps) == 0:
            timeline.append({
                "time": f"{int(total_frames / fps)}s",
                # "confidence": confidence,
                "confidence": smooth_conf,
                # "nervous": nervous
                "nervous": smooth_nerv
            })

    cap.release()

    avg_conf = int(sum(confidence_scores) / max(len(confidence_scores), 1))
    avg_nerv = int(sum(nervous_scores) / max(len(nervous_scores), 1))

    if len(timeline) == 0:
        timeline.append({
        "time": "0s",
        "confidence": avg_conf,
        "nervous": avg_nerv
    })

    return {
        "confidence": avg_conf,
        "eye_contact": avg_conf,
        "nervous": avg_nerv,
        "timeline": timeline
    }



# import cv2
# from deepface import DeepFace
# from collections import deque

# def analyze_video(video_path):
#     cap = cv2.VideoCapture(video_path)
#     total_frames = 0
#     confidence_scores = []
#     nervous_scores = []
#     timeline = []
#     window = deque(maxlen=5)

#     # fps = cap.get(cv2.CAP_PROP_FPS) or 30
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     if not fps or fps < 10:
#         fps = 30

#     window_nerv = deque(maxlen=5)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         total_frames += 1

#         if total_frames % int(fps / 2) != 0:
#             continue

#         try:
#             result = DeepFace.analyze(
#                 frame,
#                 actions=['emotion'],
#                 enforce_detection=False,
#                 silent=True
#             )

#             # emotion = result[0]["dominant_emotion"]

#             # 🎯 map emotion → confidence/nervous
#             # if emotion in ["happy", "neutral"]:
#             #     confidence = 80
#             #     nervous = 20
#             # else:
#             #     confidence = 50
#             #     nervous = 50

#             emotion_scores = result[0]["emotion"]
#             total = sum(emotion_scores.values()) or 1

#             positive = (
#                 emotion_scores.get("happy", 0) +
#                 emotion_scores.get("neutral", 0)
#             )
#             confidence = int((positive / total) * 100)

#             # nervous = int(
#             #     emotion_scores.get("fear", 0) +
#             #     emotion_scores.get("sad", 0) +
#             #     emotion_scores.get("angry", 0)
#             # )

#             negative = (
#                 emotion_scores.get("fear", 0) +
#                 emotion_scores.get("sad", 0) +
#                 emotion_scores.get("angry", 0) +
#                 emotion_scores.get("disgust", 0)
#             )
#             nervous = int((negative / total) * 100)

#         except:
#             confidence = 50
#             nervous = 50

#         # confidence_scores.append(confidence)
#         window.append(confidence)
#         smooth_conf = int(sum(window) / len(window))
#         confidence_scores.append(smooth_conf)

#         # nervous_scores.append(nervous)
#         window_nerv.append(nervous)
#         smooth_nerv = int(sum(window_nerv) / len(window_nerv))
#         nervous_scores.append(smooth_nerv)

#         # if total_frames % 30 == 0:
#         # if total_frames % 60 == 0:
#         # timeline.append({
#         #     "time": f"{int(total_frames/30)}s",

#         # if total_frames % int(fps) == 0:
#         #     timeline.append({
#         #         "time": f"{int(total_frames / fps)}s",
#         #         # "confidence": confidence,
#         #         "confidence": smooth_conf,
#         #         # "nervous": nervous
#         #         "nervous": smooth_nerv
#         #     })

#         # if total_frames % 5 == 0:
#         if total_frames % int(fps * 2) == 0:   # every 2 seconds
#             # sec = int(total_frames / fps) if fps else total_frames // 5
#             sec = int(total_frames // fps)
#             timeline.append({
#                 "time": f"{sec}s",
#                 "confidence": smooth_conf,
#                 "nervous": smooth_nerv
#             })

#     cap.release()

#     avg_conf = int(sum(confidence_scores) / max(len(confidence_scores), 1))
#     avg_nerv = int(sum(nervous_scores) / max(len(nervous_scores), 1))

#     if len(timeline) == 0:
#         timeline.append({
#             "time": "0s",
#             "confidence": avg_conf,
#             "nervous": avg_nerv
#         })

#     return {
#         "confidence": avg_conf,
#         "eye_contact": avg_conf,
#         "nervous": avg_nerv,
#         "timeline": timeline
#     }