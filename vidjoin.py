import json
import textwrap
from PIL import Image, ImageDraw, ImageFont

import http.client

conn = http.client.HTTPSConnection("api.quran.com")

payload = "{}"

conn.request("GET",  "/api/v4/quran/translations/161?verse_key=2%3A282", payload)

res = conn.getresponse()
data = json.loads(res.read().decode("utf-8"))

out = Image.new("RGB", (1024, 768), (255, 255, 255))

d = ImageDraw.Draw(out)
fnt = ImageFont.truetype("""C:\\Users\\Shadhin\\Downloads\\Nikosh\\Nikosh.ttf""", 50)

margin = offset = 40
for line in textwrap.wrap(data["translations"][0]["text"], width=40):
    d.text((margin, offset), line, font=fnt, fill="#aa0000")
    offset += fnt.getsize(line)[1]

out.show()
