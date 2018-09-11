#!/usr/bin/env python

"""
    Author: Eyal Godovich
    Date created: 11/09/2018
    Python Version: 3.6
"""

import unittest
from twister import Twister
import random

class TestTwister(unittest.TestCase):
	def test_twister(self):
		"""
		Very basic check to see if the twister works
		"""

		r = random.Random()
		numbers = [r.getrandbits(32) for i in range(624)]
		t = Twister()
		t.backtrack(numbers)

		for i in range(int(1e4)):
			self.assertEqual(t.getrandbits(32), r.getrandbits(32))


if __name__ == '__main__':
    unittest.main()