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

# 残り枚数
PAI_COUNT = {}
for p in PAI:
    if 'Red' in p:
        continue
    PAI_COUNT[p] = 4

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
    print(PAI_COUNT)

def select_tiles():
    tiles = []
    while len(tiles) < 13:
        num = random.randint(0, len(PAI) - 1)
        append_tile = PAI[num]
        count_key = append_tile.replace('Red', '')
        # 同じ赤が2枚以上入らないようにする
        if 'Red' in append_tile and append_tile in tiles:
            continue

        if PAI_COUNT[count_key] == 0:
            continue

        tiles.append(PAI[num])
        print(PAI_COUNT)
        PAI_COUNT[count_key] -= 1

    return tiles

if __name__ == '__main__':
  send_tile_dealing()
