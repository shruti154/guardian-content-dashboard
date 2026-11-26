import os
import requests
import pandas as pd
import time

API_KEY = os.environ.get("GUARDIAN_API_KEY")
url = "https://content.guardianapis.com/search"

sections = ["technology", "business", "sport", "culture", "politics"]
all_articles = []

for section in sections:
    print(f"Fetching articles for section: {section}")
    for page in range(1, 6):
        params = {
            "api-key": API_KEY,
            "page-size": 100,
            "page": page,
            "section": section,
            "show-fields": "headline,wordcount,thumbnail",
            "order-by": "newest"
        }
        response = requests.get(url, params=params)
        data = response.json()
        articles = data["response"]["results"]
        all_articles.extend(articles)
        time.sleep(0.5)

df = pd.DataFrame(all_articles)
df.to_csv("guardian_articles.csv", index=False)
print(f"Saved {len(df)} articles total")
