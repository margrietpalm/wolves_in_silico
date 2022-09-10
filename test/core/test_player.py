import pytest

from wolves_in_silico.core.player import Role, Player


def test_wolf():
    assert Player(role=Role.WOLF, id=0).is_wolf


def test_civ():
    assert not Player(role=Role.CIV, id=0).is_wolf
