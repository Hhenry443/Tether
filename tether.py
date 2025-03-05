#!/usr/bin/env python3
import argparse
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
import os
import json

CONNECTIONS_FILE = "/Path/to/profiles.json"
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
add_parser.add_argument("password", type=str, help="The system password")
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

def display_connections_table(connections):
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Profile Name", style="dim")
    table.add_column("User")
    table.add_column("IP Address")
    table.add_column("Port")
    table.add_column("Password")

    for profile, details in connections.items():
        table.add_row(profile, details['user'], details['ip'], str(details['port']), "****")
    
    console.print(table)

def display_view_connections(profileName=None):
    console.print("\n")
    console.print(Panel("Your Saved Connections", style="bold red"))
    
    connections = load_connections()

    if profileName is not None:
        if profileName in connections:
            connection = connections[profileName]
            display_connections_table({profileName: connection})
        else:
            console.print(f"[red]Profile {profileName} not found![/red]")
    else:
        display_connections_table(connections)
    
    Prompt.ask("Press Enter to continue")

def display_add_connection_menu():
    console.print("\n")
    console.print(Panel("Add a Connection (type 'exit' to cancel)", style="bold red"))
    connections = load_connections()

    display_connections_table(connections)

    while True:
        profile_name = Prompt.ask("Enter profile alias (or 'exit' to cancel)")
        if profile_name.lower() == "exit":
            console.print("[yellow]Operation cancelled.[/yellow]")
            return
        if profile_name:
            break

    if profile_name in connections:
        console.print(f"\nYou are about to override the profile {profile_name}.")
        ans = Prompt.ask("Is that ok? Y/n")
        if ans.lower() != "y":
            console.print("Aborting...")
            return
    
    while True:
        user = Prompt.ask("\nEnter system user (or 'exit' to cancel)")
        if user.lower() == "exit":
            console.print("[yellow]Operation cancelled.[/yellow]")
            return
        if user:
            break
    
    while True:
        ip = Prompt.ask("Enter system IP (or 'exit' to cancel)")
        if ip.lower() == "exit":
            console.print("[yellow]Operation cancelled.[/yellow]")
            return
        if ip:
            break
            
    while True: 
        password = Prompt.ask("Enter password (or 'exit' to cancel)", password=True)
        if password.lower() == "exit":
            console.print("[yellow]Operation cancelled.[/yellow]")
            return
        if password:
            break
            
    port = Prompt.ask("Enter port", default="22")

    connections[profile_name] = {"user": user, "ip": ip, "password": password, "port": int(port)}
    
    with open(CONNECTIONS_FILE, "w") as f:
        json.dump(connections, f, indent=4)
    
    console.print(f"\n[green]Connection profile for {profile_name} added successfully.[/green]\n")

    Prompt.ask('Press Enter To Exit')

def display_remove_connection_menu(profile_name=None):
    console.print("\n")
    console.print(Panel("Delete a Connection", style="bold red"))
    connections = load_connections()

    # Show connections before asking for a profile
    display_connections_table(connections)
    
    while True:
        profile_name = Prompt.ask("\nEnter profile alias to remove (or 'exit' to cancel)")
        if profile_name.lower() == "exit":
            console.print("[yellow]Operation cancelled.[/yellow]")
            return
        if profile_name in connections:
            break
        console.print("[red]Profile not found. Try again.[/red]")
        
    if profile_name in connections:
        del connections[profile_name]
        with open(CONNECTIONS_FILE, "w") as f:
            json.dump(connections, f, indent=4)
        console.print(f"\nProfile {profile_name} removed successfully.")
    else:
        console.print(f"\nProfile {profile_name} not found.")
    
    console.print("")
    Prompt.ask("Press Enter to continue")

def display_connection_menu():
    console.print("\n")
    console.print(Panel("What Profile Do You Want To Connect To? (type 'exit' to cancel)", style="bold red"))

    connections = load_connections()
    display_connections_table(connections)
    
    while True:
        profile_name = Prompt.ask("\nEnter profile alias to connect to (or 'exit' to cancel)")
        if profile_name.lower() == "exit":
            console.print("[yellow]Operation cancelled.[/yellow]")
            return
        if profile_name:
            break
    
    connect(profile_name)

    
def connect(profile_name):
    connections = load_connections()
    
    if profile_name not in connections:
        console.print(f"[red]Profile {profile_name} not found![/red]")
        Prompt.ask('Enter to continue')
        return
    
    profile = connections[profile_name]
    ssh_command = f"sshpass -p '{profile['password']}' ssh -p {profile['port']} {profile['user']}@{profile['ip']}"
    
    console.print(f"[green]Connecting to {profile_name} ({profile['user']}@{profile['ip']} on port {profile['port']})...[/green]")
    os.system(ssh_command)
    
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
        connect(args.profile_name)
        console.print(f"Connecting to profile: {args.profile_name}...")
    elif args.command == "remove":
        display_remove_connection_menu(args.profile_name)

if __name__ == "__main__":
    main()
