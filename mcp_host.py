import subprocess
import json
import sys
import os
import requests
from time import sleep

# Function to load the configuration from the MCP config file
def load_config():
    config_path = "config/cli_desktop_config.json"  # Path to the MCP config file
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

# Function to interact with the MCP tools
def interact_with_mcp():
    tools = load_config()
    
    for tool in tools:
        print(f"Interacting with tool: {tool['name']}...")
        # Assuming the tools have a specific endpoint for interaction, like a messaging or command endpoint
        try:
            response = requests.post(tool['interaction_url'], json={"command": "start"})
            if response.status_code == 200:
                print(f"Successfully interacted with {tool['name']}: {response.json()}")
            else:
                print(f"Error interacting with {tool['name']}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error interacting with {tool['name']}: {e}")

def main():
    print("Starting MCP Host...")

    # Step 1: Ensure that MCP tools are running
    ensure_mcp_tools()

    # Step 2: Display current configuration of MCP tools
    display_config()

    # Step 3: Interact with MCP tools (you could customize this interaction based on tool type)
    interact_with_mcp()

if __name__ == "__main__":
    main()
