# NAPIER

```
     ●     ●    
       ╳       
     ●     ●    

 N A P I E R
 
 power to people
```

## Overview

NAPIER is a local LLM agent with MCP (Model Context Protocol) capabilities. It allows you to:

1. Chat with local LLM models through Ollama
2. Act as an MCP host that can connect to various MCP-compatible tools
3. Configure and manage these tools through a simple CLI interface

## Features

- **Local LLM Access**: Uses Ollama to run language models locally on your machine
- **MCP Host**: Acts as a host for the Model Context Protocol
- **Tool Integration**: Connect to any MCP-compatible tools (like WhatsApp, file systems, web browsers, etc.)
- **Easy Configuration**: Simple CLI interface to manage your tools and preferences
- **API Server**: Exposes an API for other applications to interact with NAPIER

## Installation

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/) (will be installed automatically if not present)

### Setting Up

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/napier.git
   cd napier
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run NAPIER:
   ```bash
   python napier_cli.py
   ```

## Usage

### Chat with Local LLM

NAPIER automatically manages Ollama for you. Once started, you can chat with your local LLM models through a simple interface.

### Managing MCP Tools

You can add, remove, and configure MCP tools through the interactive menu:

1. **Add Tool**: Configure a new MCP-compatible tool
2. **Remove Tool**: Remove an existing tool
3. **Start/Restart Tools**: Ensure all configured tools are running

### Example: Adding WhatsApp MCP

```
Tool ID: whatsapp-mcp
Tool Name: WhatsApp MCP
Tool URL: http://localhost:3000
Start Command: npm run start
Command Directory: ./mcp-servers/whatsapp-mcp/
Capabilities: messaging,contact_management
Installation Command: npm install
```

## Configuration

NAPIER stores its configuration in `config/napier_config.json`. This file contains:

- Basic NAPIER settings
- Default LLM model
- MCP host configuration
- Configured tools

## Model Context Protocol (MCP)

The Model Context Protocol is a specification that standardizes how AI assistants interact with local tools and applications. NAPIER implements the MCP Host API, allowing it to:

1. Discover MCP-compatible tools
2. Execute actions on these tools
3. Receive data from tools
4. Manage permissions and security

Learn more about MCP at [modelcontextprotocol.io](https://modelcontextprotocol.io)

## Developing MCP Tools

You can create your own MCP-compatible tools that work with NAPIER. An MCP tool should:

1. Expose a REST API (typically on localhost)
2. Implement the required MCP endpoints:
   - `/status` - Returns the status of the tool
   - `/capabilities` - Lists the capabilities of the tool
   - `/actions/{action}` - Endpoints for each action the tool can perform

## API Reference

NAPIER exposes an API server at `http://0.0.0.0:8000` with the following endpoints:

- `GET /tools` - List all configured tools
- `GET /tools/{tool_id}` - Get information about a specific tool
- `POST /tools/{tool_id}/start` - Start a specific tool
- `POST /chat` - Send a chat message to the local LLM

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.