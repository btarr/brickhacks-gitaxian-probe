import json
import tensorflow as tf

INPUT_PATH = './training_data'
TRAIN_PATH = '/train'
TEST_PATH = '/test'
CARD_JSON_PATH = '/cards.json'
IMAGES_PATH = '/images'

def parse_image(filename, label):
  image_string = tf.read_file(filename)
  image_decoded = tf.image.decode_png(image_string, channels=3)
  image = tf.cast(image_decoded, tf.float32)
  return image, label

def get_dataset(images, labels):
  dataset = tf.data.Dataset.from_tensor_slices((images, labels))
  dataset = dataset.map(parse_image)
  dataset = dataset.batch(2)

def data_to_tf_data(start_path):
  cards = []
  images = []
  labels = []
  with open(start_path + CARD_JSON_PATH, 'r') as cards_file:
    train_cards = json.loads(cards_file.read())
  for card in train_cards:
    images.append(start_path + IMAGES_PATH + '/' + card.get('file_name'))
    labels.append(card.get('name'))
  return tf.constant(images), tf.constant(labels)

def main():
  train_images, train_labels = data_to_tf_data(INPUT_PATH + TRAIN_PATH)
  test_images, test_labels = data_to_tf_data(INPUT_PATH + TEST_PATH)

  train_dataset = get_dataset(train_images, train_labels)
  test_dataset = get_dataset(test_images, test_labels)

if __name__ == '__main__':
  main()