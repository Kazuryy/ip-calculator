# IP Calculator and Network Configurator

## Description

This project is a Python-based tool designed to assist network administrators in calculating subnet information and automating switch and router configuration. It simplifies the process of subnetting, VLAN creation, and device configuration, making it easier to manage complex network setups.

## Features

- **IP Address Validation**: Ensures the provided IP address is valid before proceeding.
- **Network Address Calculation**: Computes the network address and broadcast address for a given IP and subnet mask.
- **Subnetting**: Automatically generates subnets based on the desired number of subnets.
- **VLAN Configuration**: Allows users to define VLAN names and IDs for their subnets.
- **Switch Configuration**: Generates a configuration file (`switch_config.txt`) to set up VLANs and assign IP addresses to switch interfaces.
- **Router Configuration**: Generates a configuration file (`router_config.txt`) for router interfaces, including VLAN encapsulation and IP assignment.
- **Interactive CLI**: Guides the user through input steps for IP, subnet mask, VLAN details, and device configuration.

## How It Works

1. **Input**: The user provides an IP address, subnet mask, and the desired number of subnets.
2. **Calculation**: The tool calculates the network address, broadcast address, and subnet details.
3. **Configuration**: Optionally, it generates configuration files for switches and routers based on the calculated subnet information and user inputs.

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Kazuryy/ip-calculator.git
   ```
2. Navigate to the project directory:
   ```bash
   cd ip-calculator
   ```
3. Run the script:
   ```bash
   python main.py
   ```
4. Follow the interactive prompts to provide IP, mask, and subnet details.

## Output

- **Switch Configuration**: A `switch_config.txt` file containing the commands to configure VLANs and assign IP addresses.
- **Router Configuration**: A `router_config.txt` file with commands for VLAN encapsulation and IP assignment.

## Requirements

- Python 3.6 or later
- Standard library modules (`ipaddress`, `math`)

## Example

Here is an example of the interactive prompts:

```plaintext
Entrer une adresse IP (e.g., 192.168.1.0): 192.168.1.0
Entrer le masque de sous-réseau (e.g., 24): 24
Combien de sous-réseaux voulez-vous: 4
Entrer le nom du vlan: VLAN1
Entrer le nom du vlan: VLAN2
Entrer le nom du vlan: VLAN3
Entrer le nom du vlan: VLAN4
Voulez-vous configurer les switchs et routeurs? (O/N): O
```

## Future Improvements

- Add support for IPv6 subnetting and configuration.
- Enhance error handling for invalid inputs.
- Provide a graphical user interface (GUI) for better usability.
