import requests
import re
import json
from pytube import YouTube


jay_key = '周杰倫'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
}


res = requests.get(f'https://www.youtube.com/results?search_query={jay_key}', headers=headers).text
pattern = re.compile('var ytInitialData = ({.*?});', re.DOTALL)
res = pattern.search(res)

result = res.group(1) if res else 'No result'
# print(result)

# with open('jayson.txt', 'w+', encoding='utf-8') as f:
#     f.write(result)

if result != 'No result':
    result = json.loads(result)
    video_info_list = result['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
    yt_site = []
    for i, video_info in enumerate(video_info_list):
        # 目前先抓取 videoRenderer 提供的影片
        video_renderer = video_info.get('videoRenderer')
        if not video_renderer: continue
        site = f"https://www.youtube.com/watch?v={video_renderer['videoId']}"
        video_title = video_renderer['title']['runs'][0]['text']
        print(site, video_title)
        yt_site.append(site)

    print('開始下載')
    for site in yt_site:
        yt = YouTube(site)
        audio_streams = yt.streams.filter(only_audio=True)
        chosen_audio_stream = audio_streams[-1]
        download_path = "./yt_try_dl"
        chosen_audio_stream.download(download_path)
        print(f'{site} 正在下載')
        print(f"{site} 下载完成！")
    print('全部下載完成')

