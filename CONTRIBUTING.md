# Contributing to Alien Invasion

First off, thank you for taking the time to contribute! 🚀

This project started as a personal learning journey, and I'm excited to open it up to the community. Whether you're fixing a bug, polishing the gameplay, improving the docs, or just sharing an idea — all contributions are welcome.

By contributing, you agree that your work is licensed under the project's [MIT License](LICENSE).

## Table of Contents

- [How to Contribute](#how-to-contribute)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Running the Game](#running-the-game)
- [Code Style](#code-style)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Pull Request Checklist](#pull-request-checklist)
- [Reporting Bugs & Requesting Features](#reporting-bugs--requesting-features)

## How to Contribute

There are several ways you can contribute:

1. **Report bugs** — found something broken? Open an issue with a clear description.
2. **Request features** — have an idea to make the game better? Open an issue.
3. **Fix bugs or add features** — fork the repo, make your changes, and open a pull request.
4. **Improve documentation** — typos, clarifications, and better docs are always appreciated.

## Getting Started

1. **Fork the repository** and clone your fork:

   ```bash
   git clone git@github.com:<your-username>/Alien_Invasion.git
   cd Alien_Invasion
   ```

2. **Add the upstream remote** (so you can stay up to date):

   ```bash
   git remote add upstream git@github.com:henderson-01/Alien_Invasion.git
   ```

3. **Create a branch** for your work:

   ```bash
   git checkout -b your-branch-name
   ```

4. **Install dependencies** with `uv`:

   ```bash
   uv sync
   ```

> This project requires **Python 3.12+** and uses [uv](https://docs.astral.sh/uv/) for dependency management.

## Project Structure

- `alien_invasion.py`: Main game file. Contains the `AlienInvasion` class which manages the game loop, events, and rendering.
- `ship.py`: Contains the `Ship` class which manages the player's spaceship movement and rendering.
- `alien.py`: Contains the `Alien` class which manages individual alien movement, edge checking, and rendering.
- `bullet.py`: Contains the `Bullet` class which manages bullet movement and rendering.
- `settings.py`: Contains all settings for the game, such as screen dimensions, colors, and speeds.
- `game_stats.py`: Contains the `GameStats` class which tracks game statistics like `ships_left`, `score`, and `level`.
- `scoreboard.py`: Contains the `Scoreboard` class which displays the score, level, high score, and remaining ships.
- `button.py`: Contains the `Button` class used for the "Play" button on the start screen.
- `dropdown.py`: Contains the `Dropdown` class used to pick a saved username on the name entry screen.
- `high_score_manager.py`: Handles reading and writing per-user high scores to `high_score.json`.

## Running the Game

From the project root:

```bash
uv run alien_invasion.py
```

## Code Style

- Follow the existing style of the codebase (PEP 8 conventions, docstrings on classes and methods).
- The project uses [ruff](https://docs.astral.sh/ruff/) as its linter.
- Run the linter before submitting your changes:

  ```bash
  uv run ruff check .
  ```

- Keep changes focused. A PR should address **one** issue or feature, not several unrelated things.

## Submitting a Pull Request

1. Make sure your branch is up to date with `main`:

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Push your branch to your fork:

   ```bash
   git push origin your-branch-name
   ```

3. Open a pull request from your fork to `henderson-01/Alien_Invasion`'s `main` branch.
4. Fill out the [pull request template](.github/PULL_REQUEST_TEMPLATE.md) with a clear description of your changes.
5. Wait for a review. Please be patient — feedback may take a little while, and I may ask you to make changes.

## Pull Request Checklist

Before opening a PR, make sure:

- [ ] My change addresses one specific issue or feature.
- [ ] I've tested the game manually, and it runs without errors (`uv run alien_invasion.py`).
- [ ] `uv run ruff check .` passes with no errors.
- [ ] I've followed the existing code style (docstrings, naming, formatting).
- [ ] I've updated documentation (README, comments) if my change affects behavior.
- [ ] My PR description explains *what* changed and *why*.

## Reporting Bugs & Requesting Features

Please use the built-in issue templates on GitHub:

- **Bug reports:** use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md). Include your OS, Python and pygame versions, the steps to reproduce, and what you expected to happen.
- **Feature requests:** use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md). Describe the problem you're trying to solve and your proposed solution.

Before opening a new issue, please **search existing issues** to see if it has already been reported.

---

Happy coding! ⌨️
