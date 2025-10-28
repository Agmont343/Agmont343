import requests
import re
from pathlib import Path

README_PATH = Path("README.md")

def get_random_dog_image() -> str:
    url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()["message"]

def update_readme(image_url: str):
    content = README_PATH.read_text(encoding="utf-8")
    new_content = re.sub(
        r"!\[Dog of the Day\]\(.*?\)",
        f"![Dog of the Day]({image_url})",
        content
    )
    README_PATH.write_text(new_content, encoding="utf-8")
    print(f"✅ Updated dog image: {image_url}")

if __name__ == "__main__":
    image_url = get_random_dog_image()
    update_readme(image_url)
