from django.utils.text import slugify
import re
from bs4 import BeautifulSoup

def generate_unique_slug(model_instance, title, slug_field):
    """
    Generate a unique slug for blog posts and categories
    """
    slug = slugify(title)
    unique_slug = slug
    extension = 1
    ModelClass = model_instance.__class__

    while ModelClass._default_manager.filter(**{slug_field: unique_slug}).exists():
        unique_slug = f"{slug}-{extension}"
        extension += 1

    return unique_slug

def extract_first_image(content):
    """
    Extract the first image from blog content for thumbnail if not provided
    """
    soup = BeautifulSoup(content, 'html.parser')
    img = soup.find('img')
    return img.get('src') if img else None

def count_reading_time(content):
    """
    Calculate estimated reading time for blog posts
    """
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()
    word_count = len(re.findall(r'\w+', text))
    minutes = round(word_count / 200)  # Assuming average reading speed of 200 words per minute
    return max(1, minutes)  # Minimum 1 minute reading time