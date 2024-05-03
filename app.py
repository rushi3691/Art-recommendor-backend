import base64
from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, UploadFile, File
from model.controller import select_image_controller, upload_image_controller
from utils import get_some_random_images
from config import IMAGES_DIR, UPLOAD_DIR
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


GLOBAL_UP_COUNTER = 0


@app.post("/get_rec_up")
async def upload_image(file: UploadFile = File(...)):
    global GLOBAL_UP_COUNTER
    contents = await file.read()
    ext = file.filename.split(".")[-1]
    if ext not in ["jpg", "jpeg", "png"]:
        return {"message": "Invalid file type"}
    GLOBAL_UP_COUNTER += 1
    file_name = f"up_{GLOBAL_UP_COUNTER}.{ext}"
    with open(f"{UPLOAD_DIR}/{file_name}", "wb") as f:
        f.write(contents)

    data = upload_image_controller(file_name.split(".")[0], file_name)
    # ["up_1", "image_688", "image_480", "image_1450", "image_1633", "image_854"]
    image_data = {}

    for image_name in data:
        try:
            if image_name[0] == 'u':
                with open(f"{UPLOAD_DIR}/{image_name}.jpg", "rb") as image_file:
                    encoded_string = base64.b64encode(
                        image_file.read()).decode()
                    image_data[image_name] = encoded_string
            else:
                with open(f"{IMAGES_DIR}/{image_name}.jpg", "rb") as image_file:
                    encoded_string = base64.b64encode(
                        image_file.read()).decode()
                    image_data[image_name] = encoded_string
        except FileNotFoundError:
            raise HTTPException(
                status_code=404, detail=f"Image {image_name} not found")
    # delete the uploaded image
    os.remove(f"{UPLOAD_DIR}/{file_name}")

    return image_data


@app.get("/get_rec/{img_id}")
async def get_rec(img_id: str):
    data = select_image_controller(img_id)
    # [
    #     "image_865",
    #     "image_2304",
    #     "image_605",
    #     "image_1207",
    #     "image_180",
    #     "image_495"
    # ]

    image_data = {}

    for image_name in data:
        try:
            with open(f"{IMAGES_DIR}/{image_name}.jpg", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                image_data[image_name] = encoded_string
        except FileNotFoundError:
            raise HTTPException(
                status_code=404, detail=f"Image {image_name} not found")

    return image_data


@app.get("/get_random_image_set")
async def send_random_image():
    images = get_some_random_images()
    return images


@app.get("/")
async def root():
    return {"message": "Hello World"}
