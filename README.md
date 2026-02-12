# mars-rover

Would normally use Poetry for environment and dependency management for larger production applications. I would also use Dynaconf for settings management. However, this seems like a cleaner approach for a small showcase app.

pip install -e .
pip install -e ".[dev]"  # for testing
python3 -m mars_rover

OR

docker build -t mars-rover .
docker run mars-rover
