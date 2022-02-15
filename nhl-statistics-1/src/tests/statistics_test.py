import unittest
from statistics import Statistics
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

class TestStatistics(unittest.TestCase):
    def setUp(self):
        self.statistics = Statistics(PlayerReaderStub())

    def test_team(self):
        pla = self.statistics.team("PIT")
        self.assertEqual(len(pla), 1)
    
    def test_search(self):
        kurri = self.statistics.search("Kurri")
        self.assertEqual(kurri.name, "Kurri")

    def test_empty_search_result(self):
        empty = self.statistics.search("Pepe Lehtonen")
        self.assertEqual(empty, None)

    def test_top_scorers(self):
        tops = self.statistics.top_scorers(3)
        self.assertEqual(tops[0].name, "Gretzky")
        self.assertEqual(tops[1].points, 99)
        self.assertEqual(tops[2].name, "Yzerman")
