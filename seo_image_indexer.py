import os
import csv
from bs4 import BeautifulSoup

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REVIEWS_CSV = os.path.join(BASE_DIR, "reviews.csv")
EXHIBITIONS_CSV = os.path.join(BASE_DIR, "exhibitions.csv")
SITEMAP_XML = os.path.join(BASE_DIR, "sitemap.xml")
REVIEWS_HTML = os.path.join(BASE_DIR, "reviews.html")
EXHIBITION_HTML = os.path.join(BASE_DIR, "exhibition.html")

# Data structures to hold image info
review_images = []
exhibition_images = []

# 1. Read CSVs
if os.path.exists(REVIEWS_CSV):
    with open(REVIEWS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "image" in row and row["image"]:
                review_images.append({
                    "src": f"images/reviews/{row['image']}",
                    "alt": f"[밀양 가볼만한곳] 널갤러리 방문 후기 - {row['comment'][:30]}... (밀양 핫플 추천, 경남 전시회)"
                })

if os.path.exists(EXHIBITIONS_CSV):
    with open(EXHIBITIONS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "thumbnail" in row and row["thumbnail"]:
                # Note: Exhibition images are usually in images/{folder}/{thumbnail}
                folder = row.get("folder", "")
                thumb = row["thumbnail"]
                if folder:
                    src = f"images/{thumb}" # In original html, they were stored in images/ directly or inside folder.
                    # Looking at script.js or ron_mueck.html, ron_mueck_hero.png is in images/
                    exhibition_images.append({
                        "src": f"images/{thumb}",
                        "alt": f"밀양 가볼만한곳 널갤러리 전시 - {row['title']}"
                    })

# 2. Update HTML files with <noscript>
def inject_noscript_images(html_path, images):
    if not images or not os.path.exists(html_path): return
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, "html.parser")
    hidden_div = soup.find("div", class_="visually-hidden")
    
    if hidden_div:
        # Remove old noscript if exists
        old_noscript = hidden_div.find("noscript", id="seo-images")
        if old_noscript:
            old_noscript.decompose()
            
        noscript_tag = soup.new_tag("noscript", id="seo-images")
        for img in images:
            img_tag = soup.new_tag("img", src=img["src"], alt=img["alt"])
            noscript_tag.append(img_tag)
            
        hidden_div.append(noscript_tag)
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"[OK] Injected {len(images)} images into <noscript> in {os.path.basename(html_path)}")

inject_noscript_images(REVIEWS_HTML, review_images)
inject_noscript_images(EXHIBITION_HTML, exhibition_images)

# 3. Update Sitemap.xml
def update_sitemap(sitemap_path, page_url, new_images):
    if not os.path.exists(sitemap_path) or not new_images: return
    with open(sitemap_path, "r", encoding="utf-8") as f:
        sitemap_content = f.read()
        
    soup = BeautifulSoup(sitemap_content, "xml")
    
    # Find the <url> block for the specific page
    target_url = None
    for url_tag in soup.find_all("url"):
        loc = url_tag.find("loc")
        if loc and loc.text == page_url:
            target_url = url_tag
            break
            
    if target_url:
        # Remove existing image tags to avoid duplicates
        for img in target_url.find_all("image:image"):
            img.decompose()
            
        # Add new image tags
        for img in new_images:
            image_tag = soup.new_tag("image:image")
            
            loc_tag = soup.new_tag("image:loc")
            loc_tag.string = f"https://nullgallery.kr/{img['src']}"
            image_tag.append(loc_tag)
            
            caption_tag = soup.new_tag("image:caption")
            caption_tag.string = img["alt"]
            image_tag.append(caption_tag)
            
            target_url.append(image_tag)
            
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"[OK] Added {len(new_images)} images to {page_url} in sitemap.xml")

update_sitemap(SITEMAP_XML, "https://nullgallery.kr/reviews.html", review_images)
update_sitemap(SITEMAP_XML, "https://nullgallery.kr/exhibition.html", exhibition_images)

print("SEO Image Indexing Fix Complete!")
