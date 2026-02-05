
import json
import logging
import os
import requests

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Betika():
    def __init__(self):
        load_dotenv() 
        self.base_url = os.getenv("API_BASE_URL")
        
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "PostmanRuntime/7.44.0",
            "Cache-Control": "no-cache",
            "Host": "api.betika.com"
        }
        self.src = "MOBILE_WEB"
              
    def get_data(self, url):   
        try:
            response = requests.get(url)            
            return response.json()  # Assuming the response is JSON
        
        except requests.exceptions.HTTPError as http_err:
            logger.error("HTTP error occurred: %s", http_err)
        except requests.exceptions.ConnectionError as conn_err:
            logger.error("Connection error occurred: %s", conn_err)
        except requests.exceptions.Timeout as timeout_err:
            logger.error("Timeout error occurred: %s", timeout_err)
        except requests.exceptions.RequestException as req_err:
            logger.error("An error occurred: %s", req_err)
        except Exception as err:
            logger.error("Unexpected error: %s", err)
        
        return None
        
    def post_data(self, url, payload):
        try:
            # Sending the POST request
            response = requests.post(url, data=json.dumps(payload), headers=self.headers)
            return response.json()
            
        except requests.exceptions.HTTPError as http_err:
            logger.error("HTTP error occurred: %s", http_err)
        except requests.exceptions.ConnectionError as conn_err:
            logger.error("Connection error occurred: %s", conn_err)
        except requests.exceptions.Timeout as timeout_err:
            logger.error("Timeout error occurred: %s", timeout_err)
        except requests.exceptions.RequestException as req_err:
            logger.error("An error occurred: %s", req_err)
        except Exception as err:
            logger.error("Unexpected error: %s", err)
        
        return None

    def get_upcoming_matches(self, limit=1000, page=1):
        url = f'{self.base_url}/v1/uo/matches?sport_id=14&sort_id=1&esports=false&is_srl=false&limit={limit}&page={page}'
        response = self.get_data(url)
        
        if response:
            total = int(response.get('meta').get('total'))
            current_page = int(response.get('meta').get('current_page'))
            page = current_page + 1

            return total, page, response.get('data')
        else:
            return 0, 0, []
    
    
    def get_match_details(self, parent_match_id, live=False):
        url = f'{self.base_url}/v1/uo/match?parent_match_id={parent_match_id}'
        response = self.get_data(url)
        return response 
    
    
