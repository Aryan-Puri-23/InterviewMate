from fastapi import FastAPI
from fastapi import UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil, os, subprocess

from pipeline import run_pipeline

from pymongo import MongoClient
from bson import ObjectId
import os
import uuid 

# ✅ MongoDB
MONGO_URI = "mongodb+srv://interviewUser:Interview%40123@cluster0.e1yb9wf.mongodb.net/interview_mastery?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["interview_mastery"]
interviews_collection = db["interviews"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

# @app.post("/analyze")
# async def analyze(
#     file: UploadFile = File(...),
#     user_id: str = Form(...),
#     video_url: str = Form(...)
# )
#
# 
#


# @app.post("/analyze")
# async def analyze(
#     file: UploadFile = File(...),   # ✅ IMPORTANT
#     user_id: str = Form(...),        # ✅ IMPORTANT
#     video_url: str = Form(...) 
# ): 

#     filepath = os.path.join(UPLOAD_DIR, file.filename)

#     with open(filepath, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     # mp4_path = filepath.replace(".webm", ".mp4")

#     # subprocess.run([
#     #     "ffmpeg", "-i", filepath, mp4_path
#     # ])

#     # result = run_pipeline(mp4_path)

#     result = run_pipeline(filepath)

#     # ✅ SAVE USER DATA
#     doc = {
#     "user_id": user_id,
#     "video_url": video_url,  # 👈 ADD THIS
#     "score": result["score"],
#     "communication": result["communication"],
#     "confidence": result["confidence"],
#     "emotional": result["emotional"],
#     "speech": result["speech"],
#     "emotion_timeline": result["emotion_timeline"]
# }

#     inserted = interviews_collection.insert_one(doc)

#     result["_id"] = str(inserted.inserted_id)

#     os.remove(filepath)
#     os.remove(mp4_path)

#     return result


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    video_url: str = Form(...)
):

    # filepath = os.path.join(UPLOAD_DIR, file.filename)
    filename = f"{uuid.uuid4()}.webm"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ✅ NO FFMPEG
    result = run_pipeline(filepath)

    doc = {
        "user_id": user_id,
        "video_url": video_url,
        "score": result["score"],
        "communication": result["communication"],
        "confidence": result["confidence"],
        "emotional": result["emotional"],
        "speech": result["speech"],
        "emotion_timeline": result["emotion_timeline"]
    }

    inserted = interviews_collection.insert_one(doc)

    result["_id"] = str(inserted.inserted_id)

    # os.remove(filepath)
    try:
        os.remove(filepath)
    except Exception as e:
        print("File delete failed:", e)

    return result


@app.get("/interviews/{user_id}")
def get_user_interviews(user_id: str):

    data = list(interviews_collection.find({"user_id": user_id}))

    for d in data:
        d["_id"] = str(d["_id"])

    return data


@app.get("/interview/{id}")
def get_interview(id: str):

    data = interviews_collection.find_one({"_id": ObjectId(id)})

    if not data:
        return {"error": "Not found"}

    data["_id"] = str(data["_id"])

    return data