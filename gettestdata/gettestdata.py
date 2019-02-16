import requests
import json
import time
import uuid
from PIL import Image
from io import BytesIO
import os.path

BASE_API_URI = 'https://api.scryfall.com'
RANDOM_CARD_API = BASE_API_URI + '/cards/random'
REQUEST_DELAY = 1 #second(s)
OUTPUT_FOLDER = './output'
IMAGE_OUTPUT_FOLDER = './output/images'
NUMBER_OF_CARDS_TO_FETCH = 100
CARD_OUTPUT_FILE = OUTPUT_FOLDER + '/cards.json'

def log(text, space_below = False):
  print(text)
  if space_below:
    print('##########################################')

def delay_before_request():
  time.sleep(REQUEST_DELAY)

def save_card_image(card_image, card_id):
  width, height = card_image.size
  card_image = card_image.crop((0, height / 32, width, height / 8))
  file_name = card_id + '.png'
  card_image.convert('LA').save(IMAGE_OUTPUT_FOLDER + '/' + file_name)
  return file_name

def fetch_random_card():
  card_request = requests.get(RANDOM_CARD_API)

  card = card_request.json()

  if card is None:
    return None

  card_name = card.get('name')

  if not 'image_uris' in card:
    return None

  image_url = card.get('image_uris').get('normal')

  if card_name is None or image_url is None:
    return None

  # wait to request image so we don't overload the API

  delay_before_request()

  image_request = requests.get(image_url)
  card_image = Image.open(BytesIO(image_request.content))
  file_name = save_card_image(card_image, str(uuid.uuid4()))

  return ({
    "name": card_name,
    "file_name": file_name
  })

def main():
  cards = []
  if os.path.isfile(CARD_OUTPUT_FILE):
    with open(CARD_OUTPUT_FILE, 'r') as cards_file:
      cards = json.loads(cards_file.read())
  log('Fetching ' + str(NUMBER_OF_CARDS_TO_FETCH) + ' cards', True)
  for _ in range(0, NUMBER_OF_CARDS_TO_FETCH):
    log('Fetching card...')
    delay_before_request()
    card = fetch_random_card()
    if card is not None:
      card_name = card.get('name')
      log('Fetched: ' + card_name)
      cards.append(card)
      log(card_name + ' added', True)
      continue
    log('Fetch failed', True)
    log('Stopping fetches after failure', True)
    break
  cards_json = json.dumps(cards)
  with open(CARD_OUTPUT_FILE, 'w') as file:
    file.write(cards_json)

if __name__ == "__main__":
  main()