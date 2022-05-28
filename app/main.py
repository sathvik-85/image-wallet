from ast import While
from sys import path_hooks
from fastapi.middleware.cors import CORSMiddleware
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
from botocore.exceptions import ClientError
import os
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import random
from time import sleep




file_static = glob.glob('images')
image_list= []

DB = "football"
MSG_COLLECTION = "epl"
client = MongoClient("mongodb+srv://manreal:1cDVo7PUzjWF0CYs@cluster0.aslvs.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where()) 




app = FastAPI()

app.mount("/static", StaticFiles(directory="images"), name="s3_downloads")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    
    for obj in db_list:
        for key,value in obj.items():
            print(key,value)
    
    for img in files:
        with open(f"images/{img.filename}","wb") as buffer:
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
    print("ece")
    for x in date_timestamps:
        db_timestamp_list.append(x)
    
    
    for obj in db_timestamp_list:
        for key,value in obj.items():
          
            if obj["path"]:
                pathlist.append(obj["path"].split("/")[2])


            if obj["date"]<present_time:
                deleted = msg_collection.delete_one({"date":value})
    
    print(pathlist)
    for f in os.scandir("images"):
        print(f.name)
        if f.name not in pathlist:
        
            os.remove(f)




   