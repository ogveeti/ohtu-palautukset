import unittest

from player import Player
from statistics_service import StatisticsService


class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri", "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89),
        ]


class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(PlayerReaderStub())

    def test_search_finds_player_by_name(self):
        player = self.stats.search("Kurri")

        self.assertEqual(player.name, "Kurri")
        self.assertEqual(player.team, "EDM")
        self.assertEqual(player.goals, 37)
        self.assertEqual(player.assists, 53)

    def test_search_finds_player_by_partial_name(self):
        self.assertEqual(self.stats.search("Gret").name, "Gretzky")

    def test_search_returns_none_for_unknown_player(self):
        self.assertIsNone(self.stats.search("Unknown"))

    def test_team_returns_only_players_of_requested_team(self):
        players = self.stats.team("EDM")

        self.assertEqual(
            [player.name for player in players],
            ["Semenko", "Kurri", "Gretzky"],
        )

    def test_team_returns_empty_list_for_unknown_team(self):
        self.assertEqual(self.stats.team("PHI"), [])

    def test_top_returns_players_in_descending_points_order(self):
        # Nykyinen toteutus tulkitsee parametrin viimeiseksi indeksiksi.
        players = self.stats.top(4)

        self.assertEqual(
            [player.name for player in players],
            ["Gretzky", "Lemieux", "Yzerman", "Kurri", "Semenko"],
        )

    def test_top_zero_returns_highest_scoring_player(self):
        players = self.stats.top(0)

        self.assertEqual([player.name for player in players], ["Gretzky"])
