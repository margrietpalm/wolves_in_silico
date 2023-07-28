import pytest

from wolves_in_silico.abm.player import Player
from wolves_in_silico.abm.game import Role
from wolves_in_silico.abm.group import Group


@pytest.mark.parametrize('role', (Role.WOLF, Role.CIV))
def test_role(role):
    player = Player(role=role, id=0)
    assert player.role == role
    assert player.id == 0
    assert not player.is_mayor


@pytest.mark.parametrize('mayor', (True, False))
@pytest.mark.parametrize('role', (Role.WOLF, Role.CIV))
def test_repr(mayor, role):
    player = Player(role=role, id=0)
    player.is_mayor = mayor
    s = str(player)
    assert s.split('_')[0] == role.name.lower()
    assert int(s.split('_')[1][0:2]) == player.id
    if mayor:
        assert s[-1] == '*'


def test_vote_no_self():
    g = Group([Player(role=Role.CIV, id=i) for i in range(2)])
    assert g.population[0].vote(g) == g.population[1]


def test_vote_self():
    g = Group([Player(role=Role.CIV, id=0)])
    assert g.population[0].vote(g, allow_self=True) == g.population[0]


def test_vote_no_options():
    g = Group([Player(role=Role.CIV, id=0)])
    with pytest.raises(Exception):
        g.population[0].vote(g)


def test_vote_not_in_group():
    g = Group([Player(role=Role.CIV, id=i) for i in range(2)])
    p = Player(role=Role.CIV, id=2)
    p.vote(g)
