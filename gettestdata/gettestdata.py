import requests
import json
import time
import uuid
from PIL import Image
from io import BytesIO

BASE_API_URI = 'https://api.scryfall.com'
RANDOM_CARD_API = BASE_API_URI + '/cards/random'
REQUEST_DELAY = 1 #second(s)
OUTPUT_FOLDER = './output'
IMAGE_OUTPUT_FOLDER = './output/images'

def save_card_image(card_image, card_id):
  width, height = card_image.size
  card_image = card_image.crop((0, height / 32, width, height / 8))
  file_name = card_id + '.png'
  card_image.convert('LA').save(IMAGE_OUTPUT_FOLDER + '/' + file_name)
  return file_name

def fetch_random_card():
  card_request = requests.get(RANDOM_CARD_API)

  card = card_request.json()

  card_name = card['name']
  image_url = card['image_uris']['normal']

  # wait to request image so we don't overload the API
  time.sleep(REQUEST_DELAY)

  image_request = requests.get(image_url)
  card_image = Image.open(BytesIO(image_request.content))
  file_name = save_card_image(card_image, str(uuid.uuid4()))

  return ({
    "name": card_name,
    "file_name": file_name
  })

if __name__ == "__main__":
  cards = []
  cards.append(fetch_random_card())
  cards_json = json.dumps(cards)
  with open(OUTPUT_FOLDER + '/cards.json', 'w') as file:
    file.write(cards_json)