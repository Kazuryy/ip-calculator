import ipaddress
import math

def is_valid_ip(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def calculate_network_address(ip, mask):
    network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    return str(network.network_address)

def calculate_broadcast_address(ip, mask):
    network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    return str(network.broadcast_address)

def calculate_subnet_mask(hosts_needed):
    """
    Calculate subnet mask that provides exactly the right number of usable IPs
    """
    total_ips_needed = hosts_needed + 2
    host_bits = math.ceil(math.log2(total_ips_needed))
    subnet_mask = 32 - host_bits
    return subnet_mask

def subnet_network_with_custom_hosts(ip, mask, num_subnets, hosts_per_subnet):
    """
    Create subnets with custom host counts, ensuring consecutive IP allocation
    """
    # Calculate subnet masks for each subnet
    subnet_masks = [calculate_subnet_mask(hosts) for hosts in hosts_per_subnet]
    
    # Start with the initial network
    network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    current_ip = network.network_address
    subnets = []
    
    for hosts_count, subnet_mask in zip(hosts_per_subnet, subnet_masks):
        # Create a network starting from current_ip
        network = ipaddress.IPv4Network(f"{current_ip}/{subnet_mask}", strict=False)
        
        # Validate subnet has enough hosts
        hosts = list(network.hosts())
        if len(hosts) < hosts_count:
            raise ValueError(f"Pas assez d'hôtes pour {hosts_count} machines")
        
        # Store the subnet
        subnets.append(network)
        
        # Move to the IP after the broadcast of this subnet
        current_ip = ipaddress.IPv4Address(int(network.broadcast_address) + 1)
    
    # Prepare subnet information
    subnet_info = []
    for subnet in subnets:
        hosts = list(subnet.hosts())
        
        router_ip = str(hosts[-1])
        switch_ip = str(hosts[-2])
        subnet_mask = str(subnet.netmask)
        subnet_info.append((
            str(subnet.network_address), 
            str(subnet.broadcast_address), 
            router_ip, 
            switch_ip, 
            subnet_mask
        ))
    
    return subnet_info

def configure_switch(subnets, vlan_tab):
    with open("switch_config.txt", "w") as file:
        file.write("enable\nconf t\n")
        # Création des VLANs
        for i in range(len(vlan_tab)):
            file.write(f"interface vlan {vlan_tab[i][1]}\n")
            file.write(f"name {vlan_tab[i][0]}\n")
        file.write("exit\n")
        # Configuration des VLANs
        for i in range(len(vlan_tab)):
            file.write(f"interface vlan {vlan_tab[i][1]}\n")
            switch_ip = subnets[i][3]
            subnet_mask = subnets[i][4]
            file.write(f"ip address {switch_ip} {subnet_mask}\n")
        file.write("exit\n")
        # Configuration des ports
        for i in range(len(vlan_tab)):
            port = input(f"Entrer le port du VLAN {vlan_tab[i][0]}: ")
            file.write(f"interface {port}\n")
            file.write("switchport mode access\n")
            file.write(f"switchport access vlan {vlan_tab[i][1]}\n")
        file.write("exit\n")
        port_routeur = input("Entrer le port du VLAN routeur (côté switch): ")
        file.write(f"interface {port_routeur}\n")
        file.write("switchport mode trunk\n")
        file.write("end\n")

def configure_router(subnets, vlan_tab):
    with open("router_config.txt", "w") as file:
        file.write("enable\nconf t\n")
        # Création des VLANs
        for i in range(len(vlan_tab)):
            file.write(f"interface gi0/0.{vlan_tab[i][1]}\n")
            file.write(f"encapsulation dot1Q {vlan_tab[i][1]}\n")
            file.write(f"ip address {subnets[i][2]} {subnets[i][4]}\n")
        file.write(f"interface {str(input("Entrer le port du VLAN routeur (e.g. gi0/0) : "))}\n")
        file.write("no shutdown\n")


def main():
    print("Choisissez un mode de calcul de sous-réseau:")
    print("1. Nombre de sous-réseaux standard")
    print("2. Nombre de machines par sous-réseau")
    
    while True:
        try:
            mode = int(input("Entrez le numéro du mode (1 ou 2): "))
            if mode in [1, 2]:
                break
            else:
                print("Mode invalide. Choisissez 1 ou 2.")
        except ValueError:
            print("Entrée invalide. Choisissez 1 ou 2.")
    
    # IP Address Input
    while True:
        ip = input("Entrer une adresse IP (e.g., 192.168.1.0): ")
        if is_valid_ip(ip):
            break
        else:
            print("Adresse IP invalide. Veuillez réessayer.")

    # Subnet Mask Input
    while True:
        try:
            mask = int(input("Entrer le masque de sous-réseau (e.g., 24): "))
            if 0 <= mask <= 32:
                break
            else:
                print("Masque de sous-réseau invalide. Veuillez entrer un nombre entre 0 et 32.")
        except ValueError:
            print("Masque de sous-réseau invalide. Veuillez entrer un nombre entre 0 et 32.")
    
    # Number of Subnets Input
    while True:
        try:
            num_subnets = int(input("Combien de sous-réseaux voulez-vous: "))
            if num_subnets > 0:
                break
            else:
                print("Le nombre de sous-réseaux doit être supérieur à 0.")
        except ValueError:
            print("Nombre de sous-réseaux invalide. Veuillez entrer un nombre entier.")
    
    # VLAN Names
    vlan_tab = []
    for i in range(num_subnets):
        namevlan = str(input(f"Entrer le nom du vlan {i+1}: "))
        vlan_tab.append([namevlan, f"{i+1}0"])
    
    # Subnet Calculation Based on Mode
    try:
        if mode == 1:
            # Standard Mode
            hosts_default = 10  # Default 10 hosts per subnet
            subnets = subnet_network_with_custom_hosts(
                ip, mask, num_subnets, 
                [hosts_default] * num_subnets
            )
            print(f"\nCalcul des sous-réseaux en mode standard (10 machines par défaut par sous-réseau)")
        else:
            # Custom Hosts Mode
            hosts_per_subnet = []
            for i in range(num_subnets):
                while True:
                    try:
                        hosts = int(input(f"Nombre de machines pour le sous-réseau {i+1}: "))
                        if hosts > 0:
                            hosts_per_subnet.append(hosts)
                            break
                        else:
                            print("Le nombre de machines doit être supérieur à 0.")
                    except ValueError:
                        print("Entrée invalide. Veuillez entrer un nombre entier.")
            
            subnets = subnet_network_with_custom_hosts(ip, mask, num_subnets, hosts_per_subnet)
            print("\nCalcul des sous-réseaux en mode personnalisé:")
        
        # Network and Broadcast Address
        network_address = calculate_network_address(ip, mask)
        broadcast_address = calculate_broadcast_address(ip, mask)
        
        print(f"\nAdresse Réseau: {network_address}")
        print(f"Adresse Broadcast: {broadcast_address}")
        print("Sous-réseaux:\n")
        
        # Display Subnet Information
        for i, (net, broad, router, switch, ip_mask) in enumerate(subnets):
            print(f"  Sous Réseau {i+1}:")
            print(f"    Numéro du lan: vlan {i+1}0")
            print(f"    Adresse Réseau: {net}")
            print(f"    Adresse Broadcast: {broad}")
            print(f"    IP du Routeur: {router}")
            print(f"    IP du Switch: {switch}")
            print(f"    Mask: {ip_mask}\n")
        choix_config_switch = input("Voulez-vous configurer les switchs et routeurs? (O/N): ")
        if choix_config_switch.lower() == "o":
            configure_switch(subnets, vlan_tab)
        choix_config_router = input("Voulez-vous configurer les switchs et routeurs? (O/N): ")
        if choix_config_router.lower() == "o":
            configure_router(subnets, vlan_tab)
    
    except ValueError as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    main()