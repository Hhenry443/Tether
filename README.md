# Tether - CLI SSH Connection Manager

Tether is a simple, interactive, and lightweight SSH profile manager for the command line. It allows you to store, list, connect, and remove SSH connection profiles with ease.

## Features

-   Add SSH connection profiles
    
-   List saved profiles
    
-   Connect to an SSH profile
    
-   Remove profiles
    
-   Interactive CLI for easy management
    

## Prerequisites

-   Python 3.x
    
-   `sshpass` (required for automatic SSH authentication)
    
-   `rich` (for enhanced CLI UI)
    

### Install dependencies:

```
pip install rich
```


## Setup Guide

### Step One: Clone the Repository

Clone the repository to your local machine using Git:

```
git clone https://github.com/Hhenry443/Tether.git
```

### Step Two: Make the Script Executable

You need to give the `planner` file permission to be executed as a script. Run this command in your terminal:

```
chmod +x /path/to/tether.py
```

Make sure to replace `/path/to/tether.py` with the actual path where you've cloned the repository.

### Step Three: Add the Directory to Your PATH

To make the script easily accessible from anywhere, add the directory containing the script to your system's PATH. This way, you can run it without needing to navigate to the directory where the script is located.

Run the following command in your terminal:

```
echo 'export PATH="/path/to/tether.py:$PATH"' >> ~/.bashrc
```

For users with zsh (the default shell for macOS), use this instead:

```
echo 'export PATH="/path/to/tether.py:$PATH"' >> ~/.zshrc
```

Afterwards, apply the changes by running:

```
source ~/.bashrc  # For bash users
source ~/.zshrc   # For zsh users
```

### Step Four: Run it as a Command

Now, you can run the script by typing:

```
tether
```

from anywhere in the terminal, and it will execute the program.

## Usage

You can use Tether either through CLI commands or in interactive mode.

### CLI Commands

```
tether add <profile_name> <user> <ip> <password> [-p <port>]
tether list [profile_name]
tether connect <profile_name>
tether remove <profile_name>
```

#### Examples:

Add a new profile:

```
tether add myserver user123 192.168.1.100 mypassword -p 2222
```

List all profiles:

```
tether list
```

Connect to a saved profile:

```
tether connect myserver
```

Remove a profile:

```
tether remove myserver
```

### Interactive Mode

Simply run the script without arguments to start the interactive CLI:

```
tether
```

This mode presents a menu where you can manage your SSH profiles interactively.

## Configuration

Tether stores connection profiles in a JSON file. Update `CONNECTIONS_FILE` in the script to specify a custom location:

```
CONNECTIONS_FILE = "/path/to/profiles.json"
```

## Security Warning

This script stores SSH passwords in plain text. Consider using SSH keys or a more secure method for authentication.