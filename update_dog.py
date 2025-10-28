import requests
import re
from pathlib import Path
from datetime import datetime

README_PATH = Path("README.md")
DOG_BLOCK_PATTERN = re.compile(
    r"(<!-- DOG_OF_DAY_START -->).*?(<!-- DOG_OF_DAY_END -->)",
    re.DOTALL
)

def get_random_dog_image() -> str:
    """Получает случайную ссылку на картинку собаки с API."""
    url = "https://dog.ceo/api/breeds/image/random"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data.get("message")

def make_new_block(image_url: str) -> str:
    """Формирует новый HTML/Markdown блок с картинкой и датой."""
    date_str = datetime.now().strftime("%d %b %Y") 
    block = (
        "<!-- DOG_OF_DAY_START -->\n"
        f"![Dog of the Day]({image_url})\n"
        f"_Last updated: {date_str}_\n"
        "<!-- DOG_OF_DAY_END -->"
    )
    return block

def update_readme(image_url: str):
    """Заменяет блок между маркерами в README.md."""
    if not README_PATH.exists():
        raise FileNotFoundError("README.md not found in repo root")
    content = README_PATH.read_text(encoding="utf-8")

    if not DOG_BLOCK_PATTERN.search(content):
        raise RuntimeError("Dog block markers not found in README.md. "
                           "Make sure README contains <!-- DOG_OF_DAY_START --> and <!-- DOG_OF_DAY_END -->")

    new_block = make_new_block(image_url)
    new_content = DOG_BLOCK_PATTERN.sub(lambda m: new_block, content, count=1)

    if new_content == content:
        print("No changes to README (same content).")
    else:
        README_PATH.write_text(new_content, encoding="utf-8")
        print(f"✅ Updated README with new dog image: {image_url}")

if __name__ == "__main__":
    img = get_random_dog_image()
    if not img:
        raise RuntimeError("Failed to get image URL from API response")
    update_readme(img)
