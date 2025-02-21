import vt
import os
from utils.hashcalculator import calculate_file_hash
from dotenv import load_dotenv
import time

load_dotenv()
api_key = os.getenv("VIRUSTOTAL_API_KEY")

async def check_file_report(file_path: str):
    if not api_key:
        raise ValueError("VirusTotal API key not found in environment variables")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    # Check file size bcz VirusTotal limit is 32MB for basic API
    if os.path.getsize(file_path) > 32 * 1024 * 1024:
        raise ValueError("File size exceeds VirusTotal's 32MB limit")

    client = vt.Client(api_key)
    try:
        file_hash = calculate_file_hash(file_path)
        file_result = await client.get_object_async(f"/files/{file_hash}")
        if hasattr(file_result, 'last_analysis_stats'):
            return file_result.last_analysis_stats
        else:
            return await upload_file_for_report(client, file_path)
    except vt.error.APIError as e:
        error_msg = str(e)
        if "NotFoundError" in error_msg:
            return await upload_file_for_report(client, file_path)
        raise Exception(f"VirusTotal API error: {error_msg}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")
    finally:
        await client.close_async()

async def upload_file_for_report(client, file_path: str):
    try:
        with open(file_path, "rb") as f:
            analysis = await client.scan_file_async(f)
            
            retry_count = 0
            max_retries = 12  # 1 minute maximum wait time
            
            while True:
                if retry_count >= max_retries:
                    raise TimeoutError("Analysis timed out after 60 seconds")
                    
                analysis = await client.get_object_async(f"/analyses/{analysis.id}")
                if analysis.status == "completed":
                    break
                    
                retry_count += 1
                time.sleep(5)
                
        file_result = await client.get_object_async(f"/files/{analysis.id}")
        return file_result.last_analysis_stats
    except Exception as e:
        raise Exception(f"Error during file upload and analysis: {str(e)}")