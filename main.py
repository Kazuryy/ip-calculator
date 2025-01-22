import ipaddress

def calculate_network_address(ip, mask):
    network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    return str(network.network_address)

def calculate_broadcast_address(ip, mask):
    network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    return str(network.broadcast_address)

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

    network_address = calculate_network_address(ip, mask)
    broadcast_address = calculate_broadcast_address(ip, mask)
    subnets = subnet_network(ip, mask, num_subnets)

    print(f"\nAdresse Réseau: {network_address}")
    print(f"Adresse Broadcast: {broadcast_address}")
    print("Sous-réseaux:")
    for i, (net, broad, router, switch) in enumerate(subnets):
        print(f"  Sous Réseaux {i+1}0:")
        print(f"    Adresse Réseau: {net}")
        print(f"    Adresse Broadcast: {broad}")
        print(f"    IP du Routeur: {router}")
        print(f"    IP du Switch: {switch}")

if __name__ == "__main__":
    main()