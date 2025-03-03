#!/usr/bin/env python3
import argparse
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
import os
import json

CONNECTIONS_FILE = "/Users/henrybarnes/Documents/GIT/SSH Manager/profiles.json"
console = Console()

# Argument parser
parser = argparse.ArgumentParser(description="Simple SSH Connection Manager For The CLI")

# Define subcommands
subparsers = parser.add_subparsers(dest="command", required=False)

# Add a connection command
add_parser = subparsers.add_parser("add", help="Add a new connection")
add_parser.add_argument("profile_name", type=str, help="The profile alias")
add_parser.add_argument("user", type=str, help="The system user")
add_parser.add_argument("ip", type=str, help="The system IP")
add_parser.add_argument("-p", "--port", type=int, default=22, help="The port number (default: 22)")

# List saved connections command
list_parser = subparsers.add_parser("list", help="List saved connections")
list_parser.add_argument("profile_name", type=str, nargs="?", help="The profile alias to list (optional)")

# Connect to a Server command
connect_parser = subparsers.add_parser("connect", help="Connect to a profile")
connect_parser.add_argument("profile_name", type=str, help="The profile alias to connect to")

# Remove a connection command
remove_parser = subparsers.add_parser("remove", help="Removes a profile")
remove_parser.add_argument("profile_name", type=str, help="The profile alias to remove")

# Parse arguments
args = parser.parse_args()

def load_connections():
    if os.path.exists(CONNECTIONS_FILE):
        try:
            with open(CONNECTIONS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            console.print("[red]WARNING: The JSON file is corrupted or empty.[/red]")
            return {}
    return {}


def display_view_connections(profileName=None):
    console.print("\n")
    console.print(Panel("Your Saved Connections", style="bold red"))
    
    connections = load_connections()

    if profileName is not None:
        if profileName in connections:
            connection = connections[profileName]
            # Create a table for a single connection profile
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Profile Name", style="dim")
            table.add_column("User")
            table.add_column("IP Address")
            table.add_column("Port")
            table.add_row(profileName, connection['user'], connection['ip'], str(connection['port']))
            console.print(table)
        else:
            console.print(f"[red]Profile {profileName} not found![/red]")
    else:
        # Create a table to display all connections
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Profile Name", style="dim")
        table.add_column("User")
        table.add_column("IP Address")
        table.add_column("Port")

        for profile, details in connections.items():
            table.add_row(profile, details['user'], details['ip'], str(details['port']))

        console.print(table)
    
    Prompt.ask("Enter to go back")

def display_add_connection_menu():
    console.print("\n")
    console.print(Panel("Add a Connection", style="bold red"))
    console.print("\n")

    # Prompt for the connection details
    profile_name = Prompt.ask("Enter profile alias")
    user = Prompt.ask("Enter system user")
    ip = Prompt.ask("Enter system IP")
    port = Prompt.ask("Enter port", default=22)

    # Save the connection details to the JSON file
    connections = load_connections()
    connections[profile_name] = {"user": user, "ip": ip, "port": port}
    
    with open(CONNECTIONS_FILE, "w") as f:
        json.dump(connections, f, indent=4)
    
    console.print(f"Connection profile for {profile_name} added successfully.")
    console.print("\n")
    Prompt.ask("Enter to go back")

def display_remove_connection_menu(profile_name=None):
    console.print("\n")
    console.print(Panel("Delete a Connection", style="bold red"))
    
    connections = load_connections()
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Profile Name", style="dim")
    table.add_column("User")
    table.add_column("IP Address")
    table.add_column("Port")

    for profile, details in connections.items():
        table.add_row(profile, details['user'], details['ip'], str(details['port']))

    console.print(table)
    
    if profile_name == None:
        profile_name = Prompt.ask("Enter profile alias to remove")
        
    connections = load_connections()
    if profile_name in connections:
        del connections[profile_name]
        with open(CONNECTIONS_FILE, "w") as f:
            json.dump(connections, f, indent=4)
        console.print(f"Profile {profile_name} removed successfully.")
    else:
        console.print(f"Profile {profile_name} not found.")
    
    console.print("\n")
    Prompt.ask("Enter to go back")

def display_connection_menu():
    console.print("\n")
    console.print(Panel("What Profile Do You Want To Connect To?", style="bold red"))
    
    connections = load_connections()
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Profile Name", style="dim")
    table.add_column("User")
    table.add_column("IP Address")
    table.add_column("Port")

    for profile, details in connections.items():
        table.add_row(profile, details['user'], details['ip'], str(details['port']))
    
    console.print(table)
    console.print("\n")
    
    profile_name = Prompt.ask("Enter profile name to connect")
    connect(profile_name)
    
def connect(profileName=None):
    console.print("\n")
    console.print(Panel("What Profile Do You Want To Connect To?", style="bold red"))
    
def main():
    # If no command is passed, start interactive menu
    if args.command is None:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            console.print(Panel("Welcome to Tether! A lightweight SSH Profile Manager, directly in your CLI!", style="bold red"))
            console.print("\n[1] Connect to a Profile")
            console.print("[2] View Connections")
            console.print("[3] Add a Connection")
            console.print("[4] Remove a Connection")
            console.print("[5] Exit\n")
            
            choice = Prompt.ask("Select an option (1/2/3/4/5)")
            
            if choice == "1":
                display_connection_menu()
            elif choice == "2":
                display_view_connections()
            elif choice == "3":
                display_add_connection_menu()
            elif choice == "4":
                display_remove_connection_menu()
            elif choice == "5":
                console.print("Goodbye!", style="bold red")
                break
            else:
                console.print("\nInvalid option. Please select again.\n", style="bold red")
    
    # Handle the commands directly passed from the CLI
    elif args.command == "add":
        display_add_connection_menu()
    elif args.command == "list":
        display_view_connections(args.profile_name)
    elif args.command == "connect":
        console.print(f"Connecting to profile: {args.profile_name}...")
    elif args.command == "remove":
        display_remove_connection_menu(args.profile_name)

if __name__ == "__main__":
    main()
