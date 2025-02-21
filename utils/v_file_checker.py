import vt
import os
from lib.hashcalculator import calculate_file_hash
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("VIRUSTOTAL_API_KEY")

def check_file_report(file_path: str):
    if not api_key:
        raise ValueError("VirusTotal API key not found in environment variables")
    try:
        with vt.Client(api_key) as client:
            file_hash = calculate_file_hash(file_path)
            file_result = client.get_object(f"/files/{file_hash}")
            
            if file_result is None or not hasattr(file_result, 'last_analysis_stats'):
                return upload_file_for_report(file_path)
            return file_result.last_analysis_stats       
    except Exception as e:
        print(f"Error during file analysis: {e}")
        return upload_file_for_report(file_path)

def upload_file_for_report(file_path: str):
    print("Running function due to missing JSON data for that file --- uploading file for analysis ---- (Wait for Result)")
    try:
        with vt.Client(api_key) as client:
            with open(file_path, "rb") as f:
                file_result = client.scan_file(f, wait_for_completion=True)
            return file_result
    except Exception as e:
        raise Exception(f"Error uploading file for analysis: {e}")