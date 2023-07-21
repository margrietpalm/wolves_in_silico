import pytest
import numpy as np

from wolves_in_silico.abm.game import GameRecord
from wolves_in_silico.abm.group import Village


NCIV = [4, 4, 3, 3]
NWOLF = [2, 1, 1, 0]
CIV_WIN = True


@pytest.fixture(scope="module")
def record():
    states = [Village(nciv=NCIV[i], nwolf=NWOLF[i]) for i in range(len(NCIV))]
    return GameRecord(states=states, civ_win=CIV_WIN)


def test_nciv(record):
    assert record.nciv == NCIV


def test_nwolves(record):
    assert record.nwolves == NWOLF


def test_winner(record):
    assert record.civ_win
    assert not record.wolf_win


@pytest.mark.parametrize('idx', [0, 1, 2, 3])
def test_states(idx, record):
    assert Village(nciv=NCIV[idx], nwolf=NWOLF[idx]) == record.states[idx]


def test_time(record):
    np.testing.assert_array_equal(record.time, np.arange(0, len(NCIV)/2, .5))
