import pytest

from wolves_in_silico.abm.game import Game
from wolves_in_silico.vis.plot import plot_game_results


def test_plot():
    g = Game(nciv=5, nwolf=2)
    result = g.play()
    # For now, just test if the plotting function does not crash
    # Catching specific exceptions and checking if the plots match will be considered later
    try:
        plot_game_results([result])
    except Exception as e:
        pytest.fail(f"Plotting failed - {e}")

