from pydantic import BaseModel
from pymongo import MongoClient
from fastapi import FastAPI, File, UploadFile
from typing import List, Optional
import shutil
import certifi
from bson.objectid import ObjectId
from datetime import datetime
from fastapi_utils.tasks import repeat_every
import time,datetime
import glob
import os
from fastapi.staticfiles import StaticFiles
from time import sleep
from  fastapi.middleware.cors import CORSMiddleware 

image_list= []

DB = "football"
MSG_COLLECTION = "epl"
client = MongoClient("mongo",27017) 
current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"images")

app = FastAPI()
	
image_dir = os.path.dirname("images")
img_realpath = os.path.join(current_path,image_dir)
    
app.mount("/static", StaticFiles(directory=img_realpath), name="s3_downloads")

origins = ["*"]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )



@app.get("/serv")
async def server_1():
    return {"server":"second server"}


@app.get("/image-gallery")  
async def images():
    msg_collection = client[DB][MSG_COLLECTION]
    date_timestamps = msg_collection.find({},{"_id":0,"date":0}) 
    db_timestamp_list = []
    for x in date_timestamps:
        db_timestamp_list.append(x)
        
            
    return (db_timestamp_list)
            


@app.post("/uploadfile/")       
async def upload_file(files: List[UploadFile] = File(...),date:Optional[int]=None):
    msg_collection = client[DB][MSG_COLLECTION]
        
    for img in files:
        result = msg_collection.insert_one({"date":date,"path":"/static/" + img.filename})
            
        result2 = msg_collection.find({},{"_id":0})
        db_list = []
    for x in result2:
        db_list.append(x)
        
        
    for img in files:
        with open(f"{current_path}/{img.filename}","wb") as buffer:
            shutil.copyfileobj(img.file,buffer)
    
    return db_list


@app.on_event("startup")
@repeat_every(seconds=20)  # 1 hour
def check_for_expired_images():
    pathlist = []
    present_time = int(time.mktime(datetime.datetime.today().timetuple()))
    msg_collection = client[DB][MSG_COLLECTION]
    date_timestamps = msg_collection.find({},{"_id":0})    
    db_timestamp_list = []
    for x in date_timestamps:
        db_timestamp_list.append(x)
        
        
    for obj in db_timestamp_list:
        for key,value in obj.items():
            
            if obj["path"]:
                pathlist.append(obj["path"].split("/")[2])


            if obj["date"]<present_time:
                deleted = msg_collection.delete_one({"date":value})
                image_path = os.path.join(current_path,obj["path"].split("/")[2])
                os.remove(image_path)




    
