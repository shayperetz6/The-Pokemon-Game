from unittest import TestCase
from algo_stuff import AlgoStuff


class TestAlgoStuff(TestCase):

    def test_add_agents_algo(self):
        ag = AlgoStuff(None, None, None)
        TestCase.assertTrue(False == ag.add_agents_algo(), "hello")

    def test_dist(self):
        ag = AlgoStuff(None,None,None)
        TestCase.assertTrue(ag.dist(0, 0, 0, 1) == 1, "hello")

    def test_calc_src_node(self):
        ag = AlgoStuff(None, None, None)
        TestCase.assertTrue(ag.calc_src_node(None) == False, "hello")

    def test_next_node2(self):
        ag = AlgoStuff(1, None, None)
        TestCase.assertTrue(ag.next_node2()==False, "hello")
        ag = AlgoStuff(None, None, None)
        TestCase.assertTrue(ag.next_node2() == False, "hello")
