#!/usr/bin/env python3

import sys, os, json
import requests as rq
import urllib.parse as urlparse
from iso3166 import countries

def main():
    trending_countries = []
    country_codes = ["Algeria", "Argentina", "Australia", "Austria", "Azerbaijan", "Bahrain", "Belarus", "Belgium", "Bolivia, Plurinational State of", "Bosnia and Herzegovina", "Brazil", "Bulgaria", "Canada", "Chile", "Colombia", "Costa Rica", "Croatia", "Czechia", "Denmark", "Ecuador", "Egypt", "El Salvador", "Estonia", "Finland", "France", "Georgia", "Germany", "Ghana", "Greece", "Guatemala", "Honduras", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iraq", "Ireland", "Israel", "Italy", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kuwait", "Latvia", "Lebanon", "Libya", "Lithuania", "Luxembourg", "North Macedonia", "Malaysia", "Mexico", "Montenegro", "Morocco", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Nigeria", "Norway", "Oman", "Pakistan", "Panama", "Peru", "Philippines", "Poland", "Portugal", "Puerto Rico", "Qatar", "Romania", "Russian Federation", "Saudi Arabia", "Senegal", "Serbia", "Singapore", "Slovakia", "Slovenia", "South Africa", "Korea, Republic of", "Spain", "Sri Lanka", "Sweden", "Switzerland", "Taiwan", "Tanzania, United Republic of", "Thailand", "Tunisia", "Turkey", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom of Great Britain and Northern Ireland", "United States of America", "Uruguay", "Viet Nam", "Yemen", "Zimbabwe"]
    
    print("Getting the latest data from YouTube. This may take a minute...")
    i = 0
    n = len(country_codes)
    for c in country_codes:
        results_dict = get_trending("&", countries.get(c)[1])
        video_ids = []
        for x in range(len(results_dict['items'])):
            video_ids.append(results_dict['items'][x]['id'])
        if video_id in video_ids:
            trending_countries.append((countries.get(c)[0], video_ids.index(video_id) + 1))
        sys.stdout.write('\r')
        sys.stdout.write("[{:{}}] {:.1f}%".format("="*i, n-1, (100/(n-1)*i)))
        sys.stdout.flush()
        i = i + 1
    
    print()

    for tup in trending_countries:
        print(tup[0], ":", tup[1])

    print("\033[1m", "Highest Position: ", "\033[0m", min(trending_countries, key=lambda x:x[1])[1])



def get_trending(page_token, country_code):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet{page_token}chart=mostPopular&regionCode={country_code}&maxResults=50&key={API_KEY}"
    request = session.get(url)

    if request.status_code == 429:
        print("Uh oh! You have been rate limited!")
        sys.exit(1)

    return request.json()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Incorrect number of arguments! Please only specify a YouTube URL.")
        sys.exit(1)
        
    video_url = urlparse.urlparse(sys.argv[1])
    query = urlparse.parse_qs(video_url.query)
    video_id = query["v"][0]
    
    if not "YT_API_KEY" in os.environ:
        print("No API key environment variable found. Please create one called YT_API_KEY")
        sys.exit(1)

    API_KEY = os.environ.get("YT_API_KEY")
    
    session = rq.Session()
    session.trust_env = False
    main()
