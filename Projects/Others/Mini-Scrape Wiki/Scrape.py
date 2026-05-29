import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def scrape_wikipedia(url):
    headers = {
        "User-Agent": "TezendraBot/1.0 (https://example.com/contact; your@email.com)"
    }
    print(f"Scraping {url}...")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve URL: {e}")
        return

    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Get page title
    page_title = soup.find("h1", id="firstHeading")
    page_title_str = page_title.text.strip() if page_title else "wikipedia_page"
    
    infobox = soup.find("table", class_="infobox")
    
    data = {}
    if infobox:
        rows = infobox.find_all("tr")
        for row in rows:
            header = row.find("th")
            value = row.find("td")
            
            if header and value:
                data[header.text.strip()] = value.text.strip()
                
        print(f"Found {len(data)} items in infobox.")
    else:
        print("Infobox NOT FOUND on this page.")

    if data:
        table = pd.DataFrame(list(data.items()), columns = ['Key', 'Value'])
        
        # Save to excel with dynamic name
        # Remove any characters that are invalid in file paths
        safe_title = "".join(c for c in page_title_str if c.isalnum() or c in (' ', '_')).rstrip()
        filename = f"{safe_title.replace(' ', '_').lower()}_summary_table.xlsx"
        
        try:
            table.to_excel(filename, index=False)
            print(f"Successfully saved data to {filename}")
        except Exception as e:
            print(f"Failed to save excel file: {e}")
    else:
        print("No data extracted, skipping excel creation.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Wikipedia Scraper")
    parser.add_argument("url", nargs="?", default="https://en.wikipedia.org/wiki/Samsung", help="URL of the Wikipedia page to scrape")
    args = parser.parse_args()
    
    scrape_wikipedia(args.url)