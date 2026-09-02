
# Poke

## Requirements

- Python 3.10 or later
- `requests` 2.34.2 or later

## Setup

1. Clone this repo.
```
git clone https://github.com/AdamWHY2K/oakland-tech-assessment
cd oakland-tech-assessment
```
2. Install the dependency:
```
pip install -r requirements.txt
```

## Usage

Run the script with a Pokemon name:
```
python poke.py clefairy
```

This pretty prints the id, name, height, and weight.

### Options

| Flag | Effect |
|---|---|
| `-v`, `--verbose` | Print extra detail: cache hits, cache misses, and full error text. |
| `-r`, `--raw` | Print the plain Python dictionary instead of the formatted block. |

Example:

```
python poke.py pikachu -r -v
```