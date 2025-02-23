import vt
import os
import base64
import asyncio
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("VIRUSTOTAL_API_KEY")

def url_to_id(url: str) -> str:
    """Convert URL to VirusTotal URL identifier"""
    return base64.urlsafe_b64encode(url.encode()).decode().strip("=")

async def check_url_report(url: str):
    if not api_key:
        raise ValueError("VirusTotal API key not found in environment variables")
    
    async with vt.Client(api_key) as client:
        try:
            # First submit the URL for analysis
            url_id = url_to_id(url)
            
            # Try to get existing analysis first
            try:
                url_analysis = await client.get_object_async(f"/urls/{url_id}")
                return {
                    "url": url,
                    "stats": url_analysis.last_analysis_stats,
                    "reputation": url_analysis.reputation,
                    "times_submitted": url_analysis.times_submitted
                }
            except vt.error.APIError:
                # If no existing analysis, submit for scanning
                analysis = await client.scan_url_async(url)
                
                # Wait for analysis to complete
                while True:
                    analysis_result = await client.get_object_async(f"/analyses/{analysis.id}")
                    if analysis_result.status == "completed":
                        return {
                            "url": url,
                            "stats": analysis_result.stats,
                            "status": analysis_result.status
                        }
                    await asyncio.sleep(2)
                
        except Exception as e:
            return {"error": f"Error analyzing URL: {str(e)}"}