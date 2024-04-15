import requests

def request_web_page(url):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    try:
        response = requests.get(url=url,headers=headers)

        if response.status_code == 200:
            return response
        else:
            print(f"Failed to fetch: {url}. Status Code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occured for website: {url}. Error: {e}")
        return None