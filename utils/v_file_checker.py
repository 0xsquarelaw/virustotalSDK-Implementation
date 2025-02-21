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

    client = vt.Client(api_key)
    try:
        file_hash = calculate_file_hash(file_path)
        file_result = await client.get_object_async(f"/files/{file_hash}")
        if hasattr(file_result, 'last_analysis_stats'):
                return file_result.last_analysis_stats
        else:
            return await upload_file_for_report(client, file_path)
    except:
        print("File ki gand mar gayi h")
    finally:
        await client.close_async()

async def upload_file_for_report(client, file_path: str):
    # Uploading file for analysis...
    with open(file_path, "rb") as f:
        analysis = await client.scan_file_async(f)
        while True:
            analysis = await client.get_object_async(f"/analyses/{analysis.id}")
            if analysis.status == "completed":
                break
            time.sleep(5)
    file_result = await client.get_object_async(f"/files/{analysis.id}")
    return file_result.last_analysis_stats