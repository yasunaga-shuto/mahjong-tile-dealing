from fastapi import FastAPI, Request, status
from dotenv import load_dotenv
import os
import tweepy
import random
import numpy as np
from PIL import Image
from fastapi.responses import Response

app = FastAPI()

load_dotenv()

BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
CRON_SECRET = os.environ.get('CRON_SECRET')

PAI = (
  '1m', '2m', '3m', '4m', '5m', '5mRed', '6m', '7m', '8m', '9m',
  '1p', '2p', '3p', '4p', '5p', '5pRed', '6p', '7p', '8p', '9p',
  '1s', '2s', '3s', '4s', '5s', '5sRed', '6s', '7s', '8s', '9s',
  'ton', 'nan', 'sha', 'pei', 'haku', 'hatsu', 'chun'
)
ORDER = {}
for i, p in enumerate(PAI):
  ORDER[p] = i

# 残り枚数
PAI_COUNT = {}
for p in PAI:
  if 'Red' in p:
    PAI_COUNT[p] = 1
  elif '5' in p:
    PAI_COUNT[p] = 3
  else:
    PAI_COUNT[p] = 4

@app.get("/send")
def send_tile_dealing(req: Request):
  if req.headers.get('Authorization') != f"Bearer {CRON_SECRET}":
    return Response(status_code=401)

  # ドラ表示牌
  dra_indicator = random_tile()
  PAI_COUNT[dra_indicator] -= 1
  # 配牌
  tiles = select_tiles()
  tiles.sort(key=lambda val: ORDER[val])

  # ツモ牌
  drawn_tile = draw_tile()

  background = Image.open('img/background.webp')
  for i, t in enumerate(tiles):
    img = Image.open(f'img/{t}.webp').resize((36, 49))
    background.paste(img, (i * 36 + 30, 120))

  drawn_tile_img = Image.open(f'img/{drawn_tile}.webp').resize((36, 49))
  background.paste(drawn_tile_img, (508, 120))

  dra_indicator_img = Image.open(f'img/{dra_indicator}.webp').resize((36, 49))
  back = Image.open('img/back.webp').resize((36, 49))

  for i in range(7):
    if i == 2:
      background.paste(dra_indicator_img, (i * 36 + 270, 35))
    else:
      background.paste(back, (i * 36 + 270, 35))

  background.save('/tmp/tiles.webp', quality=100)

  # 送信
  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
  api = tweepy.API(auth)
  client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    wait_on_rate_limit=True
  )
  media = api.media_upload(filename='/tmp/tiles.webp')
  client.create_tweet(text='', media_ids=[media.media_id])

def select_tiles():
  tiles = []
  while len(tiles) < 13:
    append_tile = random_tile()
    # 同じ赤が2枚以上入らないようにする
    if 'Red' in append_tile and append_tile in tiles:
      continue

    if PAI_COUNT[append_tile] == 0:
      continue

    tiles.append(append_tile)
    PAI_COUNT[append_tile] -= 1

  return tiles

def random_tile():
  num = random.randint(0, len(PAI) - 1)
  tile = PAI[num]
  return tile

def draw_tile():
  while True:
    tile = random_tile()
    if PAI_COUNT[tile] > 0:
      break

  return tile
