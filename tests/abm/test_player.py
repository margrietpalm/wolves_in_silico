import pytest

from wolves_in_silico.abm.player import Player
from wolves_in_silico.base.game import Role


def test_wolf():
    wolf = Player(role=Role.WOLF, id=0)
    assert wolf.is_wolf
    assert str(wolf) == 'wolf_00'


@pytest.mark.parametrize('major', (True, False))
def test_civ(major):
    civ = Player(role=Role.CIV, id=0)
    civ.is_major = major
    assert not civ.is_wolf
    if major:
        assert str(civ) == 'civ_00*'
    else:
        assert str(civ) == 'civ_00'

