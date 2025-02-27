import requests
from bs4 import BeautifulSoup
import json

CDP_DOCS = {
    "segment": "https://segment.com/docs/",
    "mparticle": "https://docs.mparticle.com/",
    "lytics": "https://docs.lytics.com/",
    "zeotap": "https://docs.zeotap.com/home/en-us/"
}

def fetch_documentation(cdp_name, url):
    """Fetch documentation from the given URL and extract text content."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        print(f"Status Code: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract from <p> and <div> tags if Zeotap, otherwise just <p>
        if cdp_name == "zeotap":
            paragraphs = soup.find_all(["p", "div"])
        else:
            paragraphs = soup.find_all("p")

        content = "\n".join([p.get_text() for p in paragraphs])
        print(f"Extracted {len(content)} characters from {cdp_name}")

        if not content.strip():
            print(f"[⚠️] No content extracted from {cdp_name}!")

        # Save to JSON
        file_path = f"data/{cdp_name}.json"
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump({"content": content}, file, indent=4)

        print(f"[✅] Successfully saved {cdp_name} documentation to {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"[❌] Error fetching {cdp_name}: {e}")

if __name__ == "__main__":
    for cdp, url in CDP_DOCS.items():
        fetch_documentation(cdp, url)
