import imghdr
import os
import urllib.request


def download_image(url: str, output_path: str, timeout: int = 20) -> bool:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "MimmsMuseumBot/1.0 (https://mimmsmuseum.org; contact@yourdomain.com)"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    with open(output_path, "wb") as f:
        f.write(data)

    image_type = imghdr.what(output_path)
    if image_type is None:
        os.remove(output_path)
        return False
    return True
