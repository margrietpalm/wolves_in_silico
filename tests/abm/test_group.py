import pytest

from wolves_in_silico.abm.group import Group, Village, Wolves, Civilians
from wolves_in_silico.abm.player import Player, Role


class TestGroup:
    @pytest.mark.parametrize('has_mayor', [True, False])
    def test_init(self, has_mayor: bool):
        n = 3
        players = [Player(role=Role.CIV, id=i) for i in range(n)]
        if has_mayor:
            players[0].is_mayor = True
        group = Group(population=players)
        assert group.size == n
        assert group.has_mayor == has_mayor
        assert group.vote_size == n + .5 * has_mayor

    def test_remove(self):
        n = 3
        players = [Player(role=Role.CIV, id=i) for i in range(n)]
        group = Group(population=players)
        group.remove(players[0])
        assert group.size == n - 1
        assert not players[0] in group.population

    def test_eq(self):
        g1 = Group(population=[Player(Role.WOLF, 1)])
        g2 = Group(population=[Player(Role.WOLF, 1)])
        assert g1 == g2

    def test_not_eq(self):
        g1 = Group(population=[Player(Role.WOLF, 1)])
        g2 = Group(population=[Player(Role.WOLF, 2)])
        assert g1 != g2

    def test_get_mayor(self):
        n = 3
        players = [Player(role=Role.CIV, id=i) for i in range(n)]
        players[0].is_mayor = True
        group = Group(population=players)
        assert group.mayor == players[0]

    def test_get_mayor_none(self):
        n = 3
        players = [Player(role=Role.CIV, id=i) for i in range(n)]
        group = Group(population=players)
        assert group.mayor is None

    def test_get_mayor_too_many(self):
        n = 3
        players = [Player(role=Role.CIV, id=i) for i in range(n)]
        group = Group(population=players)
        players[0].is_mayor = True
        players[1].is_mayor = True
        with pytest.raises(Exception):
            group.mayor


class TestVillage:
    def test_init(self):
        village = Village(nciv=2, nwolf=2)
        assert village.nwolves == 2
        assert village.nciv == 2

    def test_choose_mayor(self):
        village = Village(nciv=2, nwolf=2)
        mayor = village.choose_mayor()
        assert mayor in village.population

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
        assert wolves.get_night_kill(civs) == civs.population[0]

    def test_turn(self):
        wolves = Wolves(n=1, p_kill=0)
        assert wolves.turn()
