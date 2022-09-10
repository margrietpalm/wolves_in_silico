import pytest

from wolves_in_silico.core.group import Group, Village, Wolves, Civilians
from wolves_in_silico.core.player import Player, Role


class TestGroup:
    @pytest.mark.parametrize('has_major', [True, False])
    def test_init(self, has_major: bool):
        n = 3
        players = [Player(role=Role.CIV, id=i) for i in range(n)]
        if has_major:
            players[0].is_major = True
        group = Group(population=players)
        assert group.size == n
        assert group.has_major == has_major
        assert group.vote_size == n + .5 * has_major

    def test_remove(self):
        n = 3
        players = [Player(role=Role.CIV, id=i) for i in range(n)]
        group = Group(population=players)
        group.remove(players[0])
        assert group.size == n - 1
        assert not players[0] in group.population


class TestVillage:
    def test_init(self):
        village = Village(nciv=2, nwolf=2)
        assert village.nwolves == 2
        assert village.nciv == 2

    def test_remove_wolf(self):
        village = Village(nciv=2, nwolf=2)
        village.remove(village.wolves.population[0])
        assert village.size == 3
        assert village.nwolves == 1

    def test_remove_civ(self):
        village = Village(nciv=2, nwolf=2)
        village.remove(village.civilians.population[0])
        assert village.size == 3
        assert village.nciv == 1

    def test_day_kill(self):
        village = Village(nciv=2, nwolf=2)
        assert village.get_day_kill() in village.population


class TestCivilians:
    def test_init(self):
        civs = Civilians(n=1)
        assert civs.size == 1
        assert not civs.population[0].is_wolf


class TestWolves:
    def test_init(self):
        wolves = Wolves(n=1)
        assert wolves.size == 1
        assert wolves.population[0].is_wolf

    def test_kill(self):
        wolves = Wolves(n=1, p_kill=1)
        civs = Civilians(n=1)
        assert wolves.get_night_kill(civs.population) == civs.population[0]

    def test_turn(self):
        wolves = Wolves(n=1, p_kill=0)
        assert wolves.turn()
