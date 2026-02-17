# Mars Rover Simulator

A command-line application that simulates a Mars rover navigating a tabletop surface. Built with Python 3.12.

## Overview

This application simulates a rover moving on a 5x5 grid (expandable). The rover can be placed at any position with a direction (NORTH, SOUTH, EAST, WEST) and can move forward, rotate left/right, and report its current position. The rover is prevented from falling off the table boundary during operation.

## Architecture

```
mars_rover/
├── __init__.py
├── __main__.py
├── commands.py      # Command pattern-like implementation
├── exceptions.py    # Exceptions
├── main.py          # CLI interface
├── messages.py      # Error messages
├── models.py        # Domain models
├── parser.py        # Command parsing
├── result.py        # CommandResult type
└── rover.py         # Rover logic
```

## Requirements

- Python 3.12+
- Dependencies: `pydantic==2.12.5`
- Dev Dependencies: `pytest==9.0.2`, `pytest-cov`, `flake8`

## Installation & Usage

```bash
# Install the package
pip install -e .

# For development (includes testing tools)
pip install -e ".[dev]"

# Run the application
python3 -m mars_rover
```

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `PLACE X,Y,F` | Place rover at position (X,Y) facing direction F | `PLACE 0,0,NORTH` |
| `MOVE` | Move one unit forward in current direction | `MOVE` |
| `LEFT` | Rotate 90° counter-clockwise | `LEFT` |
| `RIGHT` | Rotate 90° clockwise | `RIGHT` |
| `REPORT` | Output current position and direction | `REPORT` |
| `EXIT` | Quit the application | `EXIT` |

**Valid Directions**: NORTH, SOUTH, EAST, WEST
**Valid Positions**: 0,0 through 5,5

## Example Session

```
Mars Rover Simulator
Commands: PLACE X,Y,F | MOVE | LEFT | RIGHT | REPORT | EXIT

> PLACE 0,0,NORTH
> MOVE
> REPORT
0,1,NORTH
> RIGHT
> MOVE
> REPORT
1,1,EAST
> EXIT
Goodbye!
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=mars_rover --cov-report=term-missing

# Run linting
flake8 mars_rover tests
```

Current test coverage: **96%** (73 tests)

### Test Data

Sample input files in `tests/test_data/` exercise the application:

| File | Description |
|------|-------------|
| `basic_movement.txt` | Simple placement and forward movement |
| `rotation_test.txt` | LEFT and RIGHT rotation commands |
| `boundary_test.txt` | Boundary prevention at table edges |
| `full_tour.txt` | Multi-step navigation with direction changes |
| `full_tour_detailed.txt` | Comprehensive tour with frequent position reports |
| `error_cases.txt` | Invalid commands and edge cases |

```bash
python3 -m mars_rover < tests/test_data/basic_movement.txt
python3 -m mars_rover < tests/test_data/rotation_test.txt
python3 -m mars_rover < tests/test_data/boundary_test.txt
python3 -m mars_rover < tests/test_data/full_tour.txt
python3 -m mars_rover < tests/test_data/full_tour_detailed.txt
python3 -m mars_rover < tests/test_data/error_cases.txt
```

## Configuration

Table bounds can be customized by modifying the `TableBounds` initialization in `main.py`:

```python
bounds = TableBounds(min_x=0, min_y=0, max_x=5, max_y=5)
```

## Error Handling

- Centralized error messages in `messages.py`
- Domain-specific exceptions (`RoverNotPlacedException`, `InvalidCommandException`)
- CommandResult pattern for success/failure
- Boundary violations prevented with feedback

## Production Considerations

For larger deployments, consider:

- **Poetry** for dependency management
- **Dynaconf** for configuration management
- **Structured logging** with correlation IDs
- **CI/CD** pipeline for automated testing
- **Docker** for multi-system deployment
