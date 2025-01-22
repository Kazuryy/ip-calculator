import ipaddress
import math

def calculate_network_address(ip, mask):
    network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    return str(network.network_address)

def calculate_broadcast_address(ip, mask):
    network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    return str(network.broadcast_address)

def calculate_subnet_mask_whynot(original_mask, num_subnets):
    additional_bits = math.ceil(math.log2(num_subnets))
    new_mask = original_mask + additional_bits
    return new_mask

def calculate_subnet_mask(ip, mask):
    print(ip, mask)
    network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    return str(network.netmask)

def subnet_network(ip, mask, num_subnets):
    network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    subnets = list(network.subnets(new_prefix=network.prefixlen + (num_subnets - 1).bit_length()))
    subnet_info = []
    for subnet in subnets:
        hosts = list(subnet.hosts())
        router_ip = str(hosts[-1])
        switch_ip = str(hosts[-2])
        subnet_info.append((str(subnet.network_address), str(subnet.broadcast_address), router_ip, switch_ip))
    return subnet_info

def main():
    ip = input("Entrer une adresse IP (e.g., 192.168.1.0): ")
    mask = int(input("Entrer le masque de sous-réseau (e.g., 24): "))
    num_subnets = int(input("Combien de sous-réseaux voulez-vous: "))
    
    vlan_tab =[]
    for i in range(num_subnets):
        namevlan = str(input("Entrer le nom du vlan: "))
        vlan_tab.append([namevlan, f"{i+1}0"])
    print(vlan_tab)

    network_address = calculate_network_address(ip, mask)
    broadcast_address = calculate_broadcast_address(ip, mask)
    subnets = subnet_network(ip, mask, num_subnets)

    print(f"\nAdresse Réseau: {network_address}")
    print(f"Adresse Broadcast: {broadcast_address}")
    print("Sous-réseaux:\n")
    # for i, (net, broad, router, switch) in enumerate(subnets):
    #     print(i)
    #     vlan = vlan_tab[i-1][1]
    #     print(f"  Sous Réseau {i+1}:")
    #     print(f"    Numéro du lan: vlan {i+1}0")
    #     print(f"    Adresse Réseau: {net}")
    #     print(f"    Adresse Broadcast: {broad}")
    #     print(f"    IP du Routeur: {router}")
    #     print(f"    IP du Switch: {switch}\n")
    #     print("Configuration du Routeur\n")
    #     print(configure_switch(router, vlan, num_subnets))
    #     print("Configuration du Switch:\n")
    #     print(configure_router(switch, vlan))
    print(ip, mask)
    configure_switch(subnets, vlan_tab, ip, mask)

def configure_switch(subnets, vlan_tab, ip, mask):
    print(ip, mask)
    with open("switch_config.txt", "w") as file:
        file.write("enable\nconf t\n")
        # Création des vlan
        for i in range(len(vlan_tab)):
            file.write(f"interface vlan {vlan_tab[i][1]}\n")
            file.write(f"name {vlan_tab[i][0]}\n")
        file.write("exit\n")
        # Configuration des vlan
        ip_mask = calculate_subnet_mask(ip, mask)
        for i in range(len(vlan_tab)):
            file.write(f"interface vlan {vlan_tab[i][1]}\n")
            switch_ip = subnets[i][3]
            file.write(f"ip address {switch_ip} {ip_mask}\n")
            file.write("exit\n")
        # Configuration des ports
        for i in range(len(vlan_tab)):
            port = input(f"Entrer le port du vlan {vlan_tab[i][0]}: ")
            file.write(f"interface {port}\n")
            file.write("switchport mode access\n")
            file.write(f"switchport access vlan {vlan_tab[i][1]}\n")
        port_routeur = input("Entrer le port du vlan routeur: ")
        file.write(f"interface {port_routeur}\n")
        file.write("switchport mode trunk\n")
        file.write("end\n")
 

if __name__ == "__main__":
    main()