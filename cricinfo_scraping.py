import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import requests
import json
import numpy as np
import os


df = pd.read_csv('data/CountyChamp25Cricinfo.csv')

def update_df(df):
    for index, row in df.iterrows():
        name_parts = row['Player'].split()
        
        if len(name_parts) > 1:
            team = name_parts[-1].replace(')', '').replace('(', '')
            new_name = ' '.join(name_parts[:-1])
        else:
            team = ''
            new_name = row['Player']
        
        df.at[index, 'Team'] = team
        df.at[index, 'Name'] = new_name

    df.to_csv('data/CountyChamp25CricinfoUpdated.csv', index=False)

update_df(df)


def get_player_information(player_name, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    img = soup.find("img", alt=True)
    if img is None:
        print(f"No image found for {url}")
        return

    img_url = img.get("src")
    alt_text = img.get("alt", "player_image")

    save_path = f'images/{player_name}.png'

    img_resp = requests.get(img_url)
    img_resp.raise_for_status()
    with open(save_path, "wb") as f:
        f.write(img_resp.content)
    print(f"Downloaded {save_path}")

