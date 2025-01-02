import unittest
from main import select_tiles, PAI
import numpy as np

class TestMain(unittest.TestCase):
  """test class of main.py
  """

  def test_select_tiles_5mRed_not_more_than_2(self):
    """test method for select tiles
    """
    tiles = select_tiles()
    self.assertLess(count_values(tiles, '5mRed'), 2)

  def test_select_tiles_5sRed_not_more_than_2(self):
    """test method for select tiles
    """
    tiles = select_tiles()
    self.assertLess(count_values(tiles, '5sRed'), 2)

  def test_select_tiles_5pRed_not_more_than_2(self):
    """test method for select tiles
    """
    tiles = select_tiles()
    self.assertLess(count_values(tiles, '5pRed'), 2)

  def test_select_tiles_not_same_tiles_more_than_4(self):
    """test method for select tiles
    """
    tiles = select_tiles()
    for p in PAI:
      self.assertLess(count_values(tiles, p), 5)

  def test_select_tiles_not_red_and_5tiles_more_than_4(self):
    """test method for select tiles
    """
    tiles = select_tiles()
    if '5mRed' in tiles:
      self.assertLess(count_values(tiles, '5m'), 4)
    if '5sRed' in tiles:
      self.assertLess(count_values(tiles, '5s'), 4)
    if '5pRed' in tiles:
      self.assertLess(count_values(tiles, '5p'), 4)

def count_values(arr, value):
  y = np.array(arr)
  return (y == value).sum()

if __name__ == "__main__":
  for i in range(100):
    unittest.main()
