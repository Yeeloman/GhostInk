# ghostink/cli.py
import argparse
from .core import GhostInk


def main():
    parser = argparse.ArgumentParser(description="GhostInk CLI Tool")
    parser.add_argument(
        "shade",
        choices=["t", "i", "d", "w", "e"],
        help="Task to perform with GhostInk",
    )
    parser.add_argument(
        "--filename",
        type=str,
        help="Optional filename for handling YAML files",
    )
    args = parser.parse_args()

    ink = GhostInk()

    if args.shade == "t":
        print("Adding task...")
    elif args.shade == "i":
        print("Removing task...")
    elif args.shade == "d":
        print("Listing tasks...")
    elif args.shade == "w":
        print("Warning tasks...")
    elif args.shade == "e":
        print("Error tasks...")

if __name__ == "__main__":
    main()
