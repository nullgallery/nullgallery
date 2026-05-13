import os
from PIL import Image
from bs4 import BeautifulSoup

base_dir = r"E:\02_antigravity\nullgallery_web"
favicon_path = os.path.join(base_dir, "favicon.png")

# 1. Create a 512x512 pitch black image (Google recommends 48x48 multiple)
img = Image.new('RGB', (512, 512), color=(0, 0, 0))
img.save(favicon_path)
print(f"Created black favicon at {favicon_path}")

# 2. Inject into all HTML files
html_files = [f for f in os.listdir(base_dir) if f.endswith(".html")]

favicon_tags = [
    '<link rel="icon" href="/favicon.png" type="image/png">',
    '<link rel="apple-touch-icon" href="/favicon.png">'
]

for html_file in html_files:
    path = os.path.join(base_dir, html_file)
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    # Check if favicon already exists
    head = soup.find("head")
    if head:
        # Remove old icon links
        for link in head.find_all("link", rel=lambda r: r and "icon" in r.lower()):
            link.decompose()
        
        # Add new icon links
        icon_tag = soup.new_tag("link", rel="icon", href="/favicon.png", type="image/png")
        apple_tag = soup.new_tag("link", rel="apple-touch-icon", href="/favicon.png")
        
        # Insert them right after <title>
        title = head.find("title")
        if title:
            title.insert_after(apple_tag)
            title.insert_after(icon_tag)
        else:
            head.append(icon_tag)
            head.append(apple_tag)
            
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Injected favicon into {html_file}")

print("Done! You can now deploy.")
