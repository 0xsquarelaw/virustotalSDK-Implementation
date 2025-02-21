import os
from fastapi import FastAPI, UploadFile, HTTPException
from utils.v_file_checker import check_file_report

app = FastAPI()

@app.get("/")
def root_dir():
    print("Working FastAPI....!!")
    return {"Hello": "World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    try:
        os.makedirs("temp", exist_ok=True)
        file_path = f"temp/{file.filename}"
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Check file report
        result = await check_file_report(file_path)
        
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return {
            "filename": file.filename,
            "scan_result": result
        }
    except Exception as e:
        # Ensure cleanup even if error occurs
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))