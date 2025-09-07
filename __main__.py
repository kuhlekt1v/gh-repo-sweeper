"""Entry point for the GitHub Repository Sweeper application.

This module sets up logging configuration and launches the main CLI interface.
All application logs are written to 'sweeper.log' for debugging purposes.
"""

import logging

from cli import main

if __name__ == "__main__":
    logging.basicConfig(
        filename="sweeper.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    exit_code = main()
    raise SystemExit(exit_code)
