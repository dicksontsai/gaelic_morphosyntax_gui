import unittest
import doctest
import os
import sys
import app

class AppTest(unittest.TestCase):
	def setUp(self):
		self.app = app.app


if __name__ == "__main__":
	unittest.main(exit=False)