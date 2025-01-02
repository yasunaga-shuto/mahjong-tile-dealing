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

pai = (
  '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m', '5mRed',
  '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '5sRed',
  '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p', '5pRed',
  'ton', 'nan', 'sha', 'pei', 'haku', 'hatsu', 'chun'
)

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
  print(tile_dealing)

def select_tiles():
  tiles = []
  while len(tiles) < 13:
    num = random.randint(0, len(pai) - 1)
    append_tile = pai[num]
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

    tiles.append(pai[num])

  return tiles

def count_values(arr, value):
  y = np.array(arr)
  return (y == value).sum()

if __name__ == '__main__':
  send_tile_dealing()
