import argparse
import sys

if __name__ == "__main__":
    from os.path import dirname as dir

    sys.path.append(dir(sys.path[0]))

from core.game import Game
from vis.plot import plot_game_results


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('civs', type=int, help='number of civilians')
    parser.add_argument('wolves', type=int, help='number of wolves')
    parser.add_argument('-r', '--runs', type=int, help='number of runs', default=1)
    return parser.parse_args()


def main():
    args = parse_args()
    results = []
    for rep in range(args.runs):
        g = Game(nciv=args.civs, nwolf=args.wolves)
        result = g.play()
        results.append(result)
    plot_game_results(results)


if __name__ == "__main__":
    main()
