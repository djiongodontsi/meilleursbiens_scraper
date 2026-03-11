import requests
from bs4 import BeautifulSoup
import csv
import time
import re

BASE_URL = "https://meilleursbiens.com"
AGENTS_URL = "https://meilleursbiens.com/agents"
HEADERS = {"User-Agent": "Mozilla/5.0"}
DELAY = 1

def get_agent_links():
    agent_links = []
    page = 1
    while True:
        print(f"Scraping page {page}")
        url = f"{AGENTS_URL}?page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200: break
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.select("a[href*='/site/']")
        if not links: break
        for link in links:
            href = link.get("href")
            full_url = BASE_URL + href
            if full_url not in agent_links:
                agent_links.append(full_url)
        page += 1
        time.sleep(DELAY)
    return agent_links

def scrape_agent(url):
    print("Profil:", url)
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        
        name = soup.select_one("h1").get_text(strip=True) if soup.select_one("h1") else ""
        parts = name.split()
        first_name = parts[0] if parts else ""
        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        
        location = soup.select_one(".agent-location").get_text(strip=True) if soup.select_one(".agent-location") else ""
        postal_code, city = ("", "")
        match_loc = re.search(r"(\d{5})\s(.+)", location)
        if match_loc:
            postal_code, city = match_loc.groups()

        page_text = soup.get_text()
        phone = re.search(r"\+?\d[\d\s]{8,}", page_text)
        email = re.search(r"[A-Za-z0-9._%+-]+@meilleursbiens\.com", page_text)
        
        # Mandats et ventes (0 par défaut si absent) [cite: 37]
        nb_mandates = re.search(r"(\d+)\sbiens?\sen\svente", page_text)
        nb_sales = re.search(r"(\d+)\sbien[s]?\svendu", page_text)
        
        return [
            first_name, last_name, postal_code, city,
            phone.group(0).replace(" ", "") if phone else "",
            email.group(0) if email else "",
            nb_mandates.group(1) if nb_mandates else 0,
            0,
            nb_sales.group(1) if nb_sales else 0,
            ""
        ]
    except Exception as e:
        return None

def main():
    links = get_agent_links()
    with open("meilleursbiens_agents.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["first_name", "last_name", "postal_code", "city", "phone_number", 
                         "email", "nb_mandates", "avg_mandate_price", "nb_sales", "linkedin_url"]) [cite: 166-177]
        for url in links:
            data = scrape_agent(url)
            if data: writer.writerow(data)
            time.sleep(DELAY)

if __name__ == "__main__":
    main()