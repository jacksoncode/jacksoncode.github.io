import os
import requests
from bs4 import BeautifulSoup
import yt_dlp

def read_video_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        links = file.readlines()
    return [link.strip() for link in links if link.strip()]

def get_video_title(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.text.split('-')[0].strip()
        return title
    return "Unknown Title"

def download_video(url, output_dir):
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    file_path = 'd:/GitHub/jacksoncode.github.io/practise/Python/book/bilibili_links.txt'  # 替换为你的文本文件路径
    video_links = read_video_links(file_path)
    
    for link in video_links:
        title = get_video_title(link)
        output_dir = os.path.join('downloads', title)
        os.makedirs(output_dir, exist_ok=True)
        print(f"Downloading video from {link} to {output_dir}")
        download_video(link, output_dir)

if __name__ == "__main__":
    main()