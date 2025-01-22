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

def is_valid_ip(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

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
    while True:
        ip = input("Entrer une adresse IP (e.g., 192.168.1.0): ")
        if is_valid_ip(ip):
            break
        else:
            print("Adresse IP invalide. Veuillez réessayer.")

    while True:
        try:
            mask = int(input("Entrer le masque de sous-réseau (e.g., 24): "))
            if 0 <= mask <= 32:
                break
            else:
                print("Masque de sous-réseau invalide. Veuillez entrer un nombre entre 0 et 32.")
        except ValueError:
            print("Masque de sous-réseau invalide. Veuillez entrer un nombre entre 0 et 32.")
    # Ptn c'est long tout ça
    while True:
        try:
            num_subnets = int(input("Combien de sous-réseaux voulez-vous: "))
            if num_subnets > 0:
                break
            else:
                print("Le nombre de sous-réseaux doit être supérieur à 0.")
        except ValueError:
            print("Nombre de sous-réseaux invalide. Veuillez entrer un nombre entier.")
    # 
    vlan_tab =[]
    for i in range(num_subnets):
        namevlan = str(input("Entrer le nom du vlan: "))
        vlan_tab.append([namevlan, f"{i+1}0"])
    print(vlan_tab)

    network_address = calculate_network_address(ip, mask)
    broadcast_address = calculate_broadcast_address(ip, mask)
    ip_mask = calculate_subnet_mask(ip, mask)
    subnets = subnet_network(ip, mask, num_subnets)
    print(subnets)
    print(f"\nAdresse Réseau: {network_address}")
    print(f"Adresse Broadcast: {broadcast_address}")
    print("Sous-réseaux:\n")
    for i, (net, broad, router, switch) in enumerate(subnets):
        print(f"  Sous Réseau {i+1}:")
        print(f"    Numéro du lan: vlan {i+1}0")
        print(f"    Adresse Réseau: {net}")
        print(f"    Adresse Broadcast: {broad}")
        print(f"    IP du Routeur: {router}")
        print(f"    IP du Switch: {switch}\n")

    # Config ou pas du switch et routeur
    choix_config_switch = input("Voulez-vous configurer les switchs et routeurs? (O/N): ")
    if choix_config_switch.lower() == "o":
        configure_switch(subnets, vlan_tab, ip_mask)
    choix_config_router = input("Voulez-vous configurer les switchs et routeurs? (O/N): ")
    if choix_config_router.lower() == "o":
        configure_router(subnets, vlan_tab, ip_mask)

def configure_switch(subnets, vlan_tab, ip_mask):
    with open("switch_config.txt", "w") as file:
        file.write("enable\nconf t\n")
        # Création des vlan
        for i in range(len(vlan_tab)):
            file.write(f"interface vlan {vlan_tab[i][1]}\n")
            file.write(f"name {vlan_tab[i][0]}\n")
        file.write("exit\n")
        # Configuration des vlan
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

def configure_router(subnets, vlan_tab, ip_mask):
    with open("router_config.txt", "w") as file:
        file.write("enable\nconf t\n")
        # Création des vlan
        for i in range(len(vlan_tab)):
            file.write(f"interface gi0/0.{vlan_tab[i][1]}\n")
            file.write(f"encapsulation dot1Q {vlan_tab[i][1]}\n")
            file.write(f"ip address {subnets[i][2]} {ip_mask}\n")
        file.write("interface gi0/0\n")
        file.write("no shutdown\n")


if __name__ == "__main__":
    main()