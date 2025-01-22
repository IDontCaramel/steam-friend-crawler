import requests
import time
import csv
import re

API_KEY = "GET YOUR OWN API KEY >:("

FRIENDS_URL = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/"
PLAYER_SUMMARY_URL = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"

OUTPUT_FILE = "steam_friends.csv"

player_name_cache = {}

def get_friends(steam_id):
    """Fetch friends of a Steam user."""
    params = {
        'key': API_KEY,
        'steamid': steam_id,
        'relationship': 'friend'
    }
    response = requests.get(FRIENDS_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('friendslist', {}).get('friends', [])
    else:
        print(f"Error fetching friends for Steam ID {steam_id}")
        return []

def get_player_names(steam_ids):
    """Fetch the persona names of multiple players given their Steam IDs."""
    ids_to_fetch = [sid for sid in steam_ids if sid not in player_name_cache]
    
    if not ids_to_fetch:
        return {steam_id: player_name_cache[steam_id] for steam_id in steam_ids}

    params = {
        'key': API_KEY,
        'steamids': ','.join(ids_to_fetch)
    }
    response = requests.get(PLAYER_SUMMARY_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        players = data.get('response', {}).get('players', [])
        for player in players:
            steam_id = player.get('steamid')
            persona_name = player.get('personaname', 'Unknown')
            player_name_cache[steam_id] = persona_name
    return {steam_id: player_name_cache.get(steam_id, 'Unknown') for steam_id in steam_ids}

def format_name(name):
    """Format a name by removing unwanted characters and replacing spaces with underscores."""
    name = name.replace(' ', '_')
    return re.sub(r'[^a-zA-Z0-9_]', '', name)

def export_to_file(source, target):
    """Export the friendship connection to the CSV file."""
    with open(OUTPUT_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([source, target])

def explore_friends(steam_id, layers):
    """Explore friends up to a given number of layers."""
    visited = set()
    queue = [(steam_id, 0)]
    total_explored = 0

    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["source", "target"])

    while queue:
        current_id, depth = queue.pop(0)

        if current_id in visited:
            continue
        visited.add(current_id)

        if depth > layers:
            continue

        current_name = get_player_names([current_id])[current_id]
        print(f"Exploring: {current_name} (Depth: {depth})")

        friends = get_friends(current_id)
        friend_ids = [friend.get('steamid') for friend in friends]

        friend_names = get_player_names(friend_ids)

        for idx, friend_id in enumerate(friend_ids, start=1):
            friend_name = friend_names.get(friend_id)
            
            export_to_file(current_name, friend_name)
            
            print(f"{current_name} - Friend {idx}/{len(friends)}: {friend_name} (Depth: {depth + 1})")
            
            if depth < layers:
                queue.append((friend_id, depth))
        
        total_explored += 1
        print(f"Total explored so far: {total_explored}")

        time.sleep(1)

if __name__ == "__main__":
    starting_steam_id = "76561198814089395"
    layers = 2
    explore_friends(starting_steam_id, layers)
