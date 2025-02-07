import os
import requests
from bs4 import BeautifulSoup
import subprocess

def get_video_title(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text.strip()
        invalid_chars = r'<>:"/\\|?*'
        for char in invalid_chars:
            title = title.replace(char, '')
        return title
    except Exception as e:
        print(f"获取视频标题时出错: {e}")
        return None

def download_video(url, title):
    if not os.path.exists(title):
        os.makedirs(title)
    try:
        # 添加 --debug 选项
        command = f'you-get --debug -o "{title}" -f best "{url}"'
        subprocess.run(command, shell=True, check=True)
        print(f"视频 {title} 下载完成")
    except subprocess.CalledProcessError as e:
        print(f"下载视频 {title} 时出错: {e}")

def main(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                url = line.strip()
                if url:
                    title = get_video_title(url)
                    if title:
                        download_video(url, title)
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    except Exception as e:
        print(f"发生未知错误: {e}")


if __name__ == "__main__":
    # 指定包含B站视频链接的文件路径
    file_path = 'd:/GitHub/jacksoncode.github.io/practise/Python/book/bilibili_links.txt'
    main(file_path)