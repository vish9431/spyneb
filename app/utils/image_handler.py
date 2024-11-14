import os
import shutil
from fastapi import UploadFile
from typing import List
import uuid

async def save_images(files: List[UploadFile], max_images: int = 10) -> List[str]:
    if len(files) > max_images:
        raise ValueError(f"Maximum {max_images} images allowed")
    
    UPLOAD_DIR = "uploads"
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    saved_paths = []
    for file in files:
        file_extension = os.path.splitext(file.filename)[1]
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        saved_paths.append(file_path)
    
    return saved_paths