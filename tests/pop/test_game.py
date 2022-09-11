from wolves_in_silico.pop.game import Game
from wolves_in_silico.base.game import Result, Phase, Role


class TestGame:
    def test_init(self):
        game = Game(nciv=2, nwolf=2)
        assert not game.finished
        assert game.winner is None
        assert game.village.has_mayor
        assert game.phase == Phase.NIGHT

    def test_choose_mayor(self):
        game = Game(nciv=2, nwolf=2)
        game.village.wolves.has_mayor = False
        game.village.civilians.has_mayor = False
        game.choose_mayor()
        assert game.village.has_mayor

    def test_play_night(self):
        game = Game(nciv=2, nwolf=2)
        game.play_night()
        assert game.village.size == 3
        assert game.village.nciv == 1
        assert game.village.nwolves == 2
        assert game.village.has_mayor
        assert game.phase == Phase.DAY

    def test_play_day(self):
        game = Game(nciv=2, nwolf=2)
        game.phase = Phase.DAY
        game.play_day()
        assert game.village.size == 3
        assert game.phase == Phase.NIGHT

    def test_game_wolf_win(self):
        # this game is rigged for wolves to win after one night
        game = Game(nciv=2, nwolf=2)
        game.play()
        assert game.winner == Role.WOLF
        assert game.finished

    def test_game_civ_win(self):
        # This is currently very hard to rig because day kills are random
        game = Game(nciv=2, nwolf=0)
        game.phase = Phase.DAY
        game.play()
        assert game.winner == Role.CIV
        assert game.finished
