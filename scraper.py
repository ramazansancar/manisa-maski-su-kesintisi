import json
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def parse_location(text):
    """
    Input: "İlçe: TURGUTLU - Mahalle:ATATÜRK,CUMHURİYET"
    Output: ("TURGUTLU", ["ATATÜRK", "CUMHURİYET"])
    """
    try:
        # Clean "İlçe:" part
        clean_text = text.replace("İlçe:", "").strip()
        
        # Split by dash (District and Neighborhood separation)
        parts = clean_text.split("- Mahalle:")
        
        district = parts[0].strip()
        
        if len(parts) > 1:
            # Split neighborhoods by comma and convert to list
            neighborhoods = [m.strip() for m in parts[1].split(",") if m.strip()]
        else:
            neighborhoods = []
            
        return district, neighborhoods
    except:
        return text, []

def parse_dates(text):
    """
    Input: "10.01.2026 10:10 - 10.01.2026 12:34"
    Output: ("10.01.2026 10:10", "10.01.2026 12:34")
    """
    try:
        parts = text.split("-")
        if len(parts) >= 2:
            start = parts[0].strip()
            end = parts[1].strip()
            return start, end
        return text, ""
    except:
        return text, ""

def get_outages():
    # --- Browser Settings ---
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    url = "https://www.manisasu.gov.tr/su_kesintileri"
    
    try:
        driver.get(url)
        
        # Wait for page body instead of specific outage sections (page can show "no outage" state)
        wait = WebDriverWait(driver, 40)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(2) # Short wait for rendering
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        outages = []
        
        sections = soup.find_all("section", class_="text-info")
        
        for sec in sections:
            # Temporary data holders
            raw_reason = "Belirtilmemiş"
            raw_location = ""
            raw_date = ""

            # 1. Extract reason (h2)
            h2_tag = sec.find("h2")
            if h2_tag:
                raw_reason = h2_tag.get_text(strip=True)

            # 2. Scan paragraphs (Location and Date)
            paragraphs = sec.find_all("p", class_="lead")
            for p in paragraphs:
                text = p.get_text(strip=True)
                if "İlçe:" in text:
                    raw_location = text
                elif re.search(r'\d{2}\.\d{2}\.\d{4}', text):
                    raw_date = text
            
            # Process if location or date exists
            if raw_location or raw_date:
                district, neighborhoods = parse_location(raw_location)
                start, end = parse_dates(raw_date)
                
                # Desired data structure
                outage_entry = {
                    "city": "Manisa",
                    "district": district,
                    "neighborhoods": neighborhoods,
                    "description": raw_reason,
                    "start": start,
                    "end": end
                }
                
                outages.append(outage_entry)

        # If no outage sections exist, check for "no outage" notice and return empty list without raising
        if not sections:
            no_outage_msg = soup.find("h2", class_="text-primary")
            if no_outage_msg and "su kesintisi bulunmamaktadır" in no_outage_msg.get_text(strip=True).lower():
                return []

        return outages

    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        driver.quit()

if __name__ == "__main__":
    data = get_outages()
    
    output = {
        "count": len(data),
        "data": data
    }
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Process completed. {len(data)} records parsed.")
