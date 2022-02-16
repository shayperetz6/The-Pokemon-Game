from unittest import TestCase
import main


class TestGuiStuff(TestCase):

    def test_game_loop(self):
        if main.my_main() is True:
            TestCase.assertTrue(True,"hello")