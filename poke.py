from typing import TypedDict
import requests
import argparse

API_URL = "https://pokeapi.co/api/v2/pokemon/"

class Pokemon(TypedDict):
    id: int
    name: str
    height: int
    weight: int

def get_pokemon(name: str) -> Pokemon:
    response = requests.get(f"{API_URL}{name.lower()}")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        messages = {
            requests.codes.not_found: f"Hmm, {name} is not in the Pokedex. Maybe try another Pokemon?",
            requests.codes.unauthorized: "...You're not Ash!",
            requests.codes.internal_server_error: "Snorlax is sleeping, try again later.",
        }
        print(messages.get(e.response.status_code, f"Unknown error when fetching data for {name}."))
        if(args.verbose):
            print(e)
        exit(-1)

    data = response.json()
    return Pokemon(
        id=data.get("id"),
        name=data.get("name"),
        height=data.get("height"),
        weight=data.get("weight"),
    )

def print_pokemon(pokemon: Pokemon) -> None:
    print("-" * 20)
    print(f"ID: {pokemon['id']}")
    print(f"Name: {pokemon['name']}")
    print(f"Height: {pokemon['height']}")
    print(f"Weight: {pokemon['weight']}")
    print("-" * 20)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Pokemon data from the PokeAPI.")
    parser.add_argument("name", type=str, help="Name of the Pokemon to fetch.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
    # assignment brief is unclear on if the dictionary should be pretty printed or not
    parser.add_argument("-r", "--raw", action="store_true", help="Print raw JSON data.")
    args = parser.parse_args()
    pokemon_data = get_pokemon(args.name)
    if args.raw:
        print(pokemon_data)
    else:
        print_pokemon(pokemon_data)