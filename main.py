import argparse

from interfacegraphique import launchGame as GUILaunch
from miniprojet import launchGame as CLILaunch

if __name__ == "__main__":
    parser  = argparse.ArgumentParser()
    parser.add_argument("launch_method", nargs="?", choices=["cli", "gui"], default="gui")

    args = parser.parse_args()

    if args.launch_method == "cli":
        CLILaunch()
    else:
        GUILaunch()
