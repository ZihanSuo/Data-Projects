import requests
import pandas as pd
from datetime import datetime
from time import sleep


API_KEY = ''
SEARCH_QUERY = 'China travel'
PUBLISHED_AFTER = '2023-05-01T00:00:00Z'
PUBLISHED_BEFORE = '2025-05-01T00:00:00Z'


search_url = 'https://www.googleapis.com/youtube/v3/search'
video_url = 'https://www.googleapis.com/youtube/v3/videos'

video_infos = []
next_page_token = None
seen_video_ids = set()

print("📡 Start to scrap the qualified videos...")

#1: Scrap the qualified videos and get id
while True:
    params = {
        'key': API_KEY,
        'q': SEARCH_QUERY,
        'part': 'snippet',
        'type': 'video',
        'maxResults': 50,
        'publishedAfter': PUBLISHED_AFTER,
        'publishedBefore': PUBLISHED_BEFORE,
    }
    if next_page_token:
        params['pageToken'] = next_page_token

    response = requests.get(search_url, params=params, timeout=30)
    data = response.json()

    video_ids = [item['id']['videoId'] for item in data.get('items', [])]
    video_ids = [vid for vid in video_ids if vid not in seen_video_ids]
    seen_video_ids.update(video_ids)

    if not video_ids:
        break

    #2: Get the detailed info
    stats_params = {
        'key': API_KEY,
        'part': 'snippet,statistics',
        'id': ','.join(video_ids)
    }
    stats_response = requests.get(video_url, params=stats_params, timeout=30)
    stats_data = stats_response.json()

    for item in stats_data.get('items', []):
        try:
            views = int(item['statistics'].get('viewCount', 0))
            comments = int(item['statistics'].get('commentCount', 0))
            published_at = item['snippet']['publishedAt']
            video_infos.append({
                'videoId': item['id'],
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'publishedAt': published_at[:10],
                'viewCount': views,
                'commentCount': comments,
                'url': f"https://www.youtube.com/watch?v={item['id']}"
            })
        except Exception as e:
            print(f"ignore the abnormal ones: {e}")

    next_page_token = data.get('nextPageToken')
    if not next_page_token:
        break

    sleep(0.3) 

print(f"✅ Total videos：{len(video_infos)}")

#3: Filter the top 100 videos by number of views
df = pd.DataFrame(video_infos)
df = df.sort_values(by='viewCount', ascending=False).head(100).reset_index(drop=True)

#4: Store the results
df.to_csv("top100_videos.csv", index=False)
df['url'].to_csv("top100_urls.txt", index=False, header=False)

print("📁 Stored as top100_videos.csv 和 top100_urls.txt")
