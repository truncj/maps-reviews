import argparse
import json

import requests
from urllib.parse import quote
import analyze

# address = "Super 8 by Wyndham Mahwah"

parser = argparse.ArgumentParser()
parser.add_argument('--address', type=str, required=True, help='Address')
parser.add_argument('--api-key', type=str, dest="api_key", required=True, help='Address')

args = parser.parse_args()
address = args.address
api_key = args.api_key


def get_place_id(address):
  encoded_address = quote(address)
  resp = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?'
             f'address={encoded_address}&key={api_key}')
  resp_geocode = json.loads(resp.text)
  place_id = resp_geocode['results'][0]['place_id']

  return place_id


def get_reviews(place_id):
  resp = requests.get(f'https://maps.googleapis.com/maps/api/place/details/json?'
                      f'place_id={place_id}&key={api_key}')

  resp_details = json.loads(resp.text)

  if resp_details['status'] == 'OK':
    reviews = resp_details['result']['reviews']
    return reviews
  else:
    print('Failed to get json response:', resp_details)
    return ['Review is not found', place_id]


place_id = get_place_id(address)

reviews = get_reviews(place_id)

for review in reviews:
  print('---------------BEGIN----------------\n')
  text = review['text']
  print(text)
  print('-----------------------------------\n')
  analyze.sample_analyze_entity_sentiment(text)

