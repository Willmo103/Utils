import json
import yaml
import os
import sys

def load_config(config_path):
    if not os.path.exists(config_path):
        print(f"Configuration file '{config_path}' does not exist. Creating a new configuration.")
        return {}
    
    with open(config_path, 'r') as f:
        if config_path.endswith('.json'):
            return json.load(f)
        elif config_path.endswith(('.yaml', '.yml')):
            return yaml.safe_load(f)
        else:
            print("Unsupported file format. Please provide a .json or .yaml file.")
            sys.exit(1)

def save_config(config, config_path):
    with open(config_path, 'w') as f:
        if config_path.endswith('.json'):
            json.dump(config, f, indent=4)
            print(f"Configuration saved to {config_path}")
        elif config_path.endswith(('.yaml', '.yml')):
            yaml.dump(config, f, sort_keys=False)
            print(f"Configuration saved to {config_path}")
        else:
            print("Unsupported file format. Please provide a .json or .yaml file.")
            sys.exit(1)

def prompt_modify_config(config):
    print("\n--- Current Configuration ---")
    print(json.dumps(config, indent=4) if isinstance(config, dict) else config)
    print("\n--- Modify Configuration ---")

    # Modify Server Name
    server_name = input(f"Enter the server name [{config.get('server_name', 'localhost')}]: ").strip()
    if server_name:
        config['server_name'] = server_name

    # Modify Listen Port
    listen_port = input(f"Enter the listen port [{config.get('listen_port', '80')}]: ").strip()
    if listen_port:
        if listen_port.isdigit():
            config['listen_port'] = listen_port
        else:
            print("Invalid port number. Keeping the previous value.")

    # Modify Location Blocks
    if 'locations' not in config or not isinstance(config['locations'], list):
        config['locations'] = []

    while True:
        action = input("\nDo you want to (a)dd, (m)odify, or (d)elete a location block? (a/m/d/none): ").strip().lower()
        if action == 'a':
            add_location(config)
        elif action == 'm':
            modify_location(config)
        elif action == 'd':
            delete_location(config)
        else:
            break

    return config

def add_location(config):
    location = {}
    location['path'] = input("Enter the location path (e.g., /api): ").strip()
    location['proxy_pass'] = input("Enter the proxy pass URL (e.g., http://localhost:3000): ").strip()
    config['locations'].append(location)
    print("Location added.")

def modify_location(config):
    if not config['locations']:
        print("No locations to modify.")
        return
    print("\nExisting Locations:")
    for idx, loc in enumerate(config['locations'], start=1):
        print(f"{idx}. Path: {loc.get('path')}, Proxy Pass: {loc.get('proxy_pass')}")
    try:
        choice = int(input("Enter the number of the location to modify: "))
        if 1 <= choice <= len(config['locations']):
            loc = config['locations'][choice - 1]
            new_path = input(f"Enter new path [{loc.get('path')}]: ").strip()
            new_proxy = input(f"Enter new proxy pass [{loc.get('proxy_pass')}]: ").strip()
            if new_path:
                loc['path'] = new_path
            if new_proxy:
                loc['proxy_pass'] = new_proxy
            print("Location modified.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

def delete_location(config):
    if not config['locations']:
        print("No locations to delete.")
        return
    print("\nExisting Locations:")
    for idx, loc in enumerate(config['locations'], start=1):
        print(f"{idx}. Path: {loc.get('path')}, Proxy Pass: {loc.get('proxy_pass')}")
    try:
        choice = int(input("Enter the number of the location to delete: "))
        if 1 <= choice <= len(config['locations']):
            removed = config['locations'].pop(choice - 1)
            print(f"Removed location: {removed}")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python modify_nginx_config.py <path_to_config>")
        sys.exit(1)
    
    config_path = sys.argv[1]
    config = load_config(config_path)
    config = prompt_modify_config(config)
    save_config(config, config_path)

if __name__ == "__main__":
    main()
