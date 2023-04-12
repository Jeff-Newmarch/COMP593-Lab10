'''
Library for interacting with the PokeAPI.
https://pokeapi.co/
'''
import requests
import image_lib
import os

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Test out the get_pokemon_into() function
    # Use breakpoints to view returned dictionary
    #poke_info = get_pokemon_info("Rockruff")
    #poke_info = get_pokemon_info(123)

    #names = get_pokemon_names()
    download_pokemon_artwork('dugtrio', r'C:\temp')

    return

def get_pokemon_info(pokemon_name):
    """Gets information about a specified Pokemon from the PokeAPI.

    Args:
        pokemon_name (str): Pokemon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    # Clean the Pokemon name parameter by:
    # - Converting to a string object, 
    # - Removing leading and trailing whitespace, and
    # - Converting to all lowercase letters
    pokemon_name = str(pokemon_name).strip().lower()

    # Check if Pokemon name is an empty string
    if pokemon_name == '':
        print('Error: No Pokemon name specified.')
        return

    # Send GET request for Pokemon info
    print(f'Getting information for {pokemon_name}...', end='')
    url = POKE_API_URL + pokemon_name
    resp_msg = requests.get(url)

    # Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Return dictionary of Pokemon info
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')         
        return


def get_pokemon_names(offset=0, limit=100000):
    """Gets the list of pokemon names from the PokeAPI.

    Args:
        offset (int) : Choose where to start the list from. Defaults to 0.
        limit (int) : How many pokemon it can have in the list. Defaults to 100000.

    Returns:
        list: It returns a list of pokemon names
    """
    query_str_params = {
        'offset' : offset,
        'limit' : limit
    }
    print(f'Getting list of Pokemon name...', end='')
    resp_msg = requests.get(POKE_API_URL, params=query_str_params)

    if resp_msg.status_code ==requests.codes.ok:
        print('success')
        pokemon_dict = resp_msg.json()
        pokemon_names_list = [p['name'] for p in pokemon_dict['results']]
        return pokemon_names_list
    else:
         print('failure')
         print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
         return
    
def download_pokemon_artwork(pokemon_name, save_dir):
    """Downloading the pictures of the pokemon from the PokeAPI.

    Args:
        pokemon_name (str): Pokemon name.
        save_dir (str): What directory to save the file into.

    Returns:
        image_path: The path of where the image was saved to.
    """
    # Get all info for the specified pokemon
    pokemon_info = get_pokemon_info(pokemon_name)
    if pokemon_info is None:
        return
    
    # Extract the artwork URL from the info dictionary
    artwork_url = pokemon_info['sprites']['other']['official-artwork']['front_default']

    # Download the artwork
    image_bytes = image_lib.download_image(artwork_url)
    if image_bytes is None:
        return
    
    # Determine the image file path
    file_ext = artwork_url.split('.')[-1]
    image_path = os.path.join(save_dir, f'{pokemon_name}.{file_ext}')

    # Save the image file
    if image_lib.save_image_file(image_bytes, image_path):
        return image_path



    if __name__ == '__main__':
        main()