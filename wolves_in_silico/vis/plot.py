from pathlib import Path

import matplotlib.pyplot as plt

from wolves_in_silico.core.game import Result


def plot_game_results(results: list[Result], outdir: Path = Path('./')):
    # get some counts from the results
    nrep = len(results)
    nwin_civ = sum([result.civ_win for result in results])
    nciv = results[0].nciv[0]
    nwolf = results[0].nwolves[0]
    # create plots
    with plt.xkcd():
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    axes[0].set(xlabel='day', ylabel='number of players', title='civilians', yticks=range(0,nciv+1))
    axes[1].set(xlabel='day', ylabel='number of players', title='wolves', yticks=range(0,nwolf+1))
    for result in results:
        axes[0].plot(result.time, result.nciv)
        axes[1].plot(result.time, result.nwolves)
    fig.suptitle(f'{nrep} games with {nciv} civilians and {nwolf} wolves')
    axes[2].bar(['civilians', 'wolves'], [nwin_civ, nrep - nwin_civ])
    axes[2].set(title='result', ylabel='wins')
    plt.tight_layout()
    plt.savefig(outdir.joinpath('results.png'))
