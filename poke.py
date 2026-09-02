from typing import TypedDict
import requests
import argparse
import sqlite3

API_URL = "https://pokeapi.co/api/v2/pokemon/"

class Pokemon(TypedDict):
    id: int
    name: str
    height: int
    weight: int

def handle_error(response: requests.Response, name: str, verbose: bool) -> None:
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        messages = {
            requests.codes.not_found: f"Hmm, {name} is not in the Pokedex. Maybe try another Pokemon?",
            requests.codes.unauthorized: "...You're not Ash!",
            requests.codes.internal_server_error: "Snorlax is sleeping, try again later.",
        }
        print(messages.get(response.status_code, f"Unknown error when fetching data for {name}."))
        if(verbose):
            print(e)
        exit(1)

def get_pokemon(conn: sqlite3.Connection, name: str, verbose: bool) -> Pokemon:
    cached = get_cached_pokemon(conn, name, verbose)
    if cached:
        return cached
    response = requests.get(f"{API_URL}{name.lower()}")
    handle_error(response, name, verbose)
    data = response.json()
    pokemon = Pokemon(
        id=data.get("id"),
        name=data.get("name"),
        height=data.get("height"),
        weight=data.get("weight"),
    )
    if verbose:
        print(f"Cache miss: {name}")
    cache_pokemon(conn, pokemon, verbose)
    return pokemon

def print_pokemon(pokemon: Pokemon) -> None:
    print("-" * 20)
    print(f"ID: {pokemon['id']}")
    print(f"Name: {pokemon['name']}")
    print(f"Height: {pokemon['height']}")
    print(f"Weight: {pokemon['weight']}")
    print("-" * 20)

def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch Pokemon data from the PokeAPI.")
    parser.add_argument("name", type=str, help="Name of the Pokemon to fetch.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
    # assignment brief is unclear on if the dictionary should be pretty printed or not
    parser.add_argument("-r", "--raw", action="store_true", help="Print raw JSON data.")
    return parser.parse_args()

def init_db() -> sqlite3.Connection:
    conn = sqlite3.connect("pokemon.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            height INTEGER NOT NULL,
            weight INTEGER NOT NULL
        )
    """)
    conn.commit()
    return conn

def cache_pokemon(conn: sqlite3.Connection, pokemon: Pokemon, verbose: bool) -> None:
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO pokemon (id, name, height, weight)
        VALUES (?, ?, ?, ?)
    """, (pokemon['id'], pokemon['name'], pokemon['height'], pokemon['weight']))
    conn.commit()
    if verbose:
        print(f"Cached: {pokemon['name']}")

def get_cached_pokemon(conn: sqlite3.Connection, name: str, verbose: bool) -> Pokemon | None:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, height, weight FROM pokemon WHERE name = ?",
        (name.lower(),),
    )
    row = cursor.fetchone()
    if row:
        id_, name, height, weight = row
        if verbose:
            print(f"Cache hit: {name}")
        return Pokemon(
            id=id_,
            name=name,
            height=height,
            weight=weight,
        )
    return None

if __name__ == "__main__":
    args = init_args()
    conn = init_db()
    pokemon_data = get_pokemon(conn, args.name, args.verbose)
    if args.raw:
        print(pokemon_data)
    else:
        print_pokemon(pokemon_data)