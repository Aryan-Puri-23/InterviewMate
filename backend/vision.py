import cv2
from deepface import DeepFace

def analyze_video(video_path):

    cap = cv2.VideoCapture(video_path)

    total_frames = 0
    confidence_scores = []
    nervous_scores = []

    timeline = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        total_frames += 1

        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, silent=True)

            emotion = result[0]["dominant_emotion"]

            # 🎯 map emotion → confidence/nervous
            if emotion in ["happy", "neutral"]:
                confidence = 80
                nervous = 20
            else:
                confidence = 50
                nervous = 50

        except:
            confidence = 50
            nervous = 50

        confidence_scores.append(confidence)
        nervous_scores.append(nervous)

        if total_frames % 30 == 0:
            timeline.append({
                "time": f"{int(total_frames/30)}s",
                "confidence": confidence,
                "nervous": nervous
            })

    cap.release()

    avg_conf = int(sum(confidence_scores) / max(len(confidence_scores), 1))
    avg_nerv = int(sum(nervous_scores) / max(len(nervous_scores), 1))

    return {
        "confidence": avg_conf,
        "eye_contact": avg_conf,
        "nervous": avg_nerv,
        "timeline": timeline
    }