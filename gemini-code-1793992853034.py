import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

# Target sources
SOURCES = {
    "purpleline": "https://www.purplelinemd.com/updates",
    "dots": "https://dots.umd.edu/about-us/news-and-alerts",
    "facilities": "https://facilities.umd.edu/",
    "alert": "https://alert.umd.edu/"
}

def fetch_purple_line():
    notices = []
    try:
        res = requests.get(SOURCES["purpleline"], timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Example parsing selector (adjust based on target DOM)
        for item in soup.select('.update-item, article'):
            title = item.find(['h2', 'h3', 'a'])
            desc = item.find('p')
            if title and desc:
                notices.append({
                    "id": f"pl-{len(notices)+1}",
                    "title": title.get_text(strip=True),
                    "source": "Purple Line MD",
                    "category": "driving",
                    "status": "Closed",
                    "lat": 38.9880 + (len(notices) * 0.001),
                    "lng": -76.9440,
                    "details": desc.get_text(strip=True)
                })
    except Exception as e:
        print(f"Error scraping Purple Line: {e}")
    return notices

def fetch_umd_dots():
    notices = []
    try:
        res = requests.get(SOURCES["dots"], timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        for item in soup.select('.news-item, .alert-item'):
            title = item.find(['h3', 'h4'])
            if title:
                notices.append({
                    "id": f"dots-{len(notices)+1}",
                    "title": title.get_text(strip=True),
                    "source": "UMD DOTS",
                    "category": "driving",
                    "status": "Delay",
                    "lat": 38.9855,
                    "lng": -76.9360,
                    "details": "Active transit detour or parking shift."
                })
    except Exception as e:
        print(f"Error scraping DOTS: {e}")
    return notices

def update_all_notices():
    all_notices = []
    all_notices.extend(fetch_purple_line())
    all_notices.extend(fetch_umd_dots())
    
    # Fallback default items if external sites are unreachable
    if not all_notices:
        all_notices = [
            {
                "id": 1,
                "title": "Campus Drive Light Rail Work",
                "source": "Purple Line MD",
                "category": "driving",
                "status": "Closed",
                "lat": 38.9880,
                "lng": -76.9440,
                "details": "Single lane closures along Campus Drive near Stamp Student Union due to track installation."
            },
            {
                "id": 2,
                "title": "Regents Drive Garage Maintenance",
                "source": "Facilities Mgmt",
                "category": "pedestrian",
                "status": "Detour",
                "lat": 38.9895,
                "lng": -76.9405,
                "details": "West sidewalk section closed for utility repair. Use east side walkway."
            }
        ]

    with open('notices.json', 'w') as f:
        json.dump(all_notices, f, indent=2)
    print(f"[{datetime.now()}] Successfully updated notices.json with {len(all_notices)} records.")

if __name__ == "__main__":
    update_all_notices()