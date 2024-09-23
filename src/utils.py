from pathlib import Path
import requests

__all__ = ["valid_path","get_image","download_image"]

def valid_path(path:Path):
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    return path

def get_image(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content

def download_image(url, save_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0'
    }
    response = requests.get(url, headers=headers,stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"图片已下载并保存为: {save_path}")
    else:
        print("下载失败")