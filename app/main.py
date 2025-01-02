from dotenv import load_dotenv
import os
import tweepy
import random
import numpy as np

load_dotenv()

BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

PAI = (
  '1m', '2m', '3m', '4m', '5m', '5mRed', '6m', '7m', '8m', '9m',
  '1s', '2s', '3s', '4s', '5s', '5sRed', '6s', '7s', '8s', '9s',
  '1p', '2p', '3p', '4p', '5p', '5pRed', '6p', '7p', '8p', '9p',
  'ton', 'nan', 'sha', 'pei', 'haku', 'hatsu', 'chun'
)
ORDER = {}
for i, p in enumerate(PAI):
  ORDER[p] = i

def send_tile_dealing():
  # client = tweepy.Client(
  #   bearer_token=BEARER_TOKEN,
  #   consumer_key=CONSUMER_KEY,
  #   consumer_secret=CONSUMER_SECRET,
  #   access_token=ACCESS_TOKEN,
  #   access_token_secret=ACCESS_TOKEN_SECRET,
  #   wait_on_rate_limit=True
  # )
  # client.create_tweet(text="テスト")

  tile_dealing = select_tiles()
  tile_dealing.sort(key=lambda val: ORDER[val])
  print(tile_dealing)

def select_tiles():
  tiles = []
  while len(tiles) < 13:
    num = random.randint(0, len(PAI) - 1)
    append_tile = PAI[num]
    # 同じ赤が2枚以上入らないようにする
    if 'Red' in append_tile and append_tile in tiles:
      continue

    # 同じ牌が5枚以上入らないようにする
    if count_values(tiles, append_tile) == 4:
      continue

    # 赤 + 黒が5枚以上入らないようにする
    if (append_tile == '5m' or append_tile == '5mRed') and count_values(tiles, '5m') + count_values(tiles, '5mRed') == 4:
      continue
    if (append_tile == '5s' or append_tile == '5sRed') and count_values(tiles, '5s') + count_values(tiles, '5sRed') == 4:
      continue
    if (append_tile == '5p' or append_tile == '5pRed') and count_values(tiles, '5p') + count_values(tiles, '5pRed') == 4:
      continue

    tiles.append(PAI[num])

  return tiles

def count_values(arr, value):
  y = np.array(arr)
  return (y == value).sum()

if __name__ == '__main__':
  send_tile_dealing()
