from __future__ import annotations

from .worker_daemon import main as worker_main


def main() -> None:
    worker_main()


if __name__ == "__main__":
    main()
