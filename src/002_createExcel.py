import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import json
import hashlib
import os
from PIL import Image
import glob
import pandas as pd
import openpyxl

prefix_url = "https://nakamura196.github.io/shajikaido"
prefix_path = "../docs"

rows_0 = [
    ["ID", "Title", "Thumbnail", "manifest", "viewingDirection", "Relation", "viewingHint", "rights", "attribution"],
    ["http://purl.org/dc/terms/identifier", "http://purl.org/dc/terms/title", "http://xmlns.com/foaf/0.1/thumbnail", "http://schema.org/url", "http://iiif.io/api/presentation/2#viewingDirection", "http://purl.org/dc/terms/relation", "http://iiif.io/api/presentation/2#viewingHint", "http://purl.org/dc/terms/rights", ""],
    ["Literal", "Literal", "Resource", "Resource", "Resource", "Resource", "Resource", "Resource", "Literal"],
    ["", "", "", "", "", "", ""],
]

rows_1 = [
    ["ID", "Thumbnail"]
]

rows_2 = [
    ["ID", "Original", "Thumbnail", "Width", "Height"]
]

rows_3 = [
    ["label", "url"],
    ["社寺会堂デジタルアーカイブラボ", prefix_url+"/iiif/collection/top.json"]
]

ids = ["アッサラームファンデーション候補画像", "寛永寺", "神田明神", "湯島聖堂", "湯島天満宮"]

for id in ids:
    files = glob.glob(prefix_path + "/files/original/"+id+"/*.jpg", recursive=True)
    files = sorted(files)

    thumbnail_url_0 = ""

    for file in files:
        original_url = file.replace(prefix_path, prefix_url)
        img = Image.open(file)
        thumbnail_url = original_url.replace("/original/", "/medium/")

        rows_1.append([id, thumbnail_url])

        rows_2.append([id, original_url, thumbnail_url, img.width, img.height])

        if thumbnail_url_0 == "":
            thumbnail_url_0 = thumbnail_url

    manifest = prefix_url + "/iiif/"+id+"/manifest.json"

    rows_0.append([id, id, thumbnail_url_0, manifest, "http://iiif.io/api/presentation/2#rightToLeftDirection", "http://universalviewer.io/examples/uv/uv.html#?manifest="+manifest, "", "http://creativecommons.org/publicdomain/zero/1.0/", id])

df_0 = pd.DataFrame(rows_0)
df_1 = pd.DataFrame(rows_1)

with pd.ExcelWriter('data/main.xlsx') as writer:
    df_0.to_excel(writer, sheet_name='item', index=False, header=False)
    df_1.to_excel(writer, sheet_name='thumbnail', index=False, header=False)
    pd.DataFrame(rows_2).to_excel(writer, sheet_name='media', index=False, header=False)
    pd.DataFrame(rows_3).to_excel(writer, sheet_name='collection', index=False, header=False)
    pd.DataFrame([]).to_excel(writer, sheet_name='toc', index=False, header=False)


