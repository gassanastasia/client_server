import requests
from typing import Dict, Any, Optional
from datetime import datetime
import logging

from client.src.core.config import settings

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        self.base_url = settings.server_url.rstrip('/')
        self.timeout = settings.api_timeout
        self.session = requests.Session()
        self.click_count = 0
    
    def send_request(self, text: str) -> Optional[Dict[str, Any]]:
        """Send POST request to server."""
        try:
            self.click_count += 1
            current_date = datetime.now().strftime("%Y-%m-%d")
            current_time = datetime.now().strftime("%H:%M:%S")
            
            payload = {
                "text": text,
                "request_date": current_date,
                "request_time": current_time,
                "click_count": self.click_count
            }
            
            response = self.session.post(
                f"{self.base_url}/requests",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            logger.info(f"Request sent successfully: {payload}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send request: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def get_requests(self, page: int = 1, per_page: int = 10) -> Optional[Dict[str, Any]]:
        """GET requests from server with pagination."""
        try:
            response = self.session.get(
                f"{self.base_url}/requests",
                params={"page": page, "per_page": per_page},
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get requests: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def reset_click_count(self):
        """Reset click counter."""
        self.click_count = 0