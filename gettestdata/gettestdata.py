import requests
import json
import time
from PIL import Image
from io import BytesIO

BASE_API_URI = 'https://api.scryfall.com'
RANDOM_CARD_API = BASE_API_URI + '/cards/random'
REQUEST_DELAY = 1 #second(s)

def save_card_name_image(card_image):
  width, height = card_image.size
  card_image.crop((0, 0, width, height/8)).convert('LA').save('./test.png')

def fetch_random_card():
  card_request = requests.get(RANDOM_CARD_API)

  card = card_request.json()

  card_name = card['name']
  image_url = card['image_uris']['normal']

  # wait to request image so we don't overload the API
  time.sleep(REQUEST_DELAY)

  image_request = requests.get(image_url)
  card_image = Image.open(BytesIO(image_request.content))
  save_card_name_image(card_image)

if __name__ == "__main__":
  fetch_random_card()