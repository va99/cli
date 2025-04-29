import subprocess
import requests
import json
import sys
import os
from time import sleep
from rich.console import Console
import shutil
from pathlib import Path

# Initialize console for rich output
console = Console()

# ASCII art greeting
ascii_art = """
     ●     ●    
       ╳       
     ●     ●    

 N A P I E R
 
 power to people
"""

# Function to display animated ASCII art greeting
def animated_greeting(ascii_art, delay=0.05):
    os.system('cls' if os.name == 'nt' else 'clear')
    for line in ascii_art.strip().split('\n'):
        console.print(line, style="bold white")
        sleep(delay)
    console.print("\n[bold green]Hello, welcome to your local AI assistant![/bold green]\n")

# Function to check if Ollama is installed by checking the PATH
def is_ollama_installed():
    return shutil.which("ollama") is not None

# Function to install Ollama automatically
def install_ollama():
    print("Ollama is not installed. Would you like to install it? (Y/N): ", end="")
    user_input = input().strip().lower()
    
    if user_input == 'y':
        print("Ollama installation starting...")
        # Download and install Ollama using the official installation script
        install_command = "curl -fsSL https://ollama.com/install.sh | sh"
        try:
            subprocess.run(install_command, shell=True, check=True)
            print("Ollama installation completed successfully.")
        except subprocess.CalledProcessError:
            print("Error: Ollama installation failed. Please check your internet connection or system permissions.")
            sys.exit(1)
    else:
        print("Ollama installation aborted. You won't be able to use the local AI assistant without it.")
        sys.exit(0)

# Function to generate or load the secret key
def generate_or_load_secret_key():
    secret_key_path = Path(os.path.expanduser("~")) / ".ollama/id_ed25519"
    
    if not secret_key_path.exists():
        print(f"Could not find the secret key at {secret_key_path}. Generating a new key.")
        # Generate the key
        try:
            subprocess.run(["ollama", "generate-key"], check=True)
            print(f"New secret key generated and saved to {secret_key_path}.")
        except subprocess.CalledProcessError:
            print("Error: Could not generate the secret key.")
            sys.exit(1)
    else:
        print(f"Found existing secret key at {secret_key_path}.")

# Function to start Ollama after installation
def start_ollama():
    print("Starting Ollama...")
    try:
        subprocess.Popen(["ollama", "serve"])
        print("Ollama is running in the background.")
    except Exception as e:
        print(f"Error: Failed to start Ollama. {e}")
        sys.exit(1)

# Function to stop Ollama
def stop_ollama():
    try:
        # First, check if Ollama is running
        ollama_process = subprocess.Popen(["pgrep", "-f", "ollama"], stdout=subprocess.PIPE)
        pid = ollama_process.communicate()[0].decode("utf-8").strip()
        
        if pid:
            # Kill the process
            subprocess.run(["kill", pid], check=True)
            print("Ollama has been stopped.")
        else:
            print("Ollama is not running.")
    except Exception as e:
        print(f"Error stopping Ollama: {e}")

# Function to load configuration for MCP tools
def load_config():
    config_path = "config/cli_desktop_config.json"
    if not os.path.exists(config_path):
        print(f"Config file not found at {config_path}. Please ensure the config file is in place.")
        sys.exit(1)

    with open(config_path) as f:
        return json.load(f).get("tools", [])

# Check if necessary MCP tools are installed and running
def ensure_mcp_tools():
    tools = load_config()
    
    # Check each tool if they are running and reachable
    for tool in tools:
        print(f"Checking connection to {tool['name']}...")
        if not is_tool_running(tool['id']):
            print(f"[ERROR] Tool {tool['name']} is not running. Starting it now...")
            start_mcp_tool(tool['id'])
        else:
            print(f"{tool['name']} is already running.")

# Function to check if a specific tool is running
def is_tool_running(tool_id):
    tool = next((t for t in load_config() if t['id'] == tool_id), None)
    if not tool:
        print(f"[ERROR] Tool {tool_id} not found.")
        return False
    
    try:
        response = requests.get(tool['url'])
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Function to start a specific MCP tool
def start_mcp_tool(tool_id):
    tool = next((t for t in load_config() if t['id'] == tool_id), None)
    if tool:
        print(f"Starting tool {tool['name']}...")
        subprocess.Popen([tool['start_command']])  # Assuming each tool has a start command
        sleep(2)  # Give the tool some time to start before checking
        ensure_mcp_tools()

# Function to display the current MCP tool configuration
def display_config():
    tools = load_config()
    print("Current MCP Tool Configuration:")
    for tool in tools:
        print(f"- {tool['name']} (ID: {tool['id']}) running at {tool['url']}")
        print(f"  Start Command: {tool['start_command']}")

# Function to chat with Ollama locally
def chat_with_ollama():
    API_URL = "http://localhost:11434/api/generate"  # Local Ollama URL
    while True:
        prompt = input("Ask me anything (or type 'exit' to quit): ")
        if prompt.lower() == 'exit':
            print("Goodbye!")
            break
        
        # Send the request to Ollama
        try:
            response = requests.post(API_URL, json={"model": "llama3", "prompt": prompt})
            if response.status_code == 200:
                print(f"LLM Response: {response.json()['response']}")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}. Make sure Ollama is running locally.")

# Main program logic
def main():
    # Step 1: Display the animated ASCII art greeting
    animated_greeting(ascii_art)
    
    # Step 2: Check if Ollama is installed
    if not is_ollama_installed():
        install_ollama()  # Ask to install Ollama if not found

    # Step 3: Generate or load the secret key if necessary
    generate_or_load_secret_key()

    # Step 4: Make sure Ollama is running in the background
    print("Checking if Ollama is running...")
    if not is_ollama_installed():
        print("Error: Ollama installation failed!")
        sys.exit(1)
    
    # Start Ollama in the background if it's not running
    start_ollama()

    # Step 5: Ensure MCP tools are running and available
    ensure_mcp_tools()

    # Step 6: Ask the user if they want to stop Ollama at any point
    stop_input = input("Would you like to stop Ollama after using it? (Y/N): ").strip().lower()
    if stop_input == 'y':
        stop_ollama()

    # Step 7: Display the current MCP tool configuration
    display_config()

    # Step 8: Start the interaction with Ollama
    chat_with_ollama()

if __name__ == "__main__":
    main()
