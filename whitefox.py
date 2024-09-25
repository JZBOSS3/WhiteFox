import sys
import ipaddress
from colorama import Fore, Style

args = list()
network = ''

def print_ascii():
    ascii_txt = r"""
██╗    ██╗██╗  ██╗██╗████████╗███████╗███████╗ ██████╗ ██╗  ██╗
██║    ██║██║  ██║██║╚══██╔══╝██╔════╝██╔════╝██╔═══██╗╚██╗██╔╝
██║ █╗ ██║███████║██║   ██║   █████╗  █████╗  ██║   ██║ ╚███╔╝ 
██║███╗██║██╔══██║██║   ██║   ██╔══╝  ██╔══╝  ██║   ██║ ██╔██╗ 
╚███╔███╔╝██║  ██║██║   ██║   ███████╗██║     ╚██████╔╝██╔╝ ██╗
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝"""
    print(Fore.CYAN + ascii_txt + Style.RESET_ALL)
    print(Fore.CYAN + '\t\t🦊 By jzboss3 🦊' + Style.RESET_ALL)

def print_help():
    print()
    print(Fore.RED + 'Syntax: python3 whitefox.py 192.168.0.100/24' + Style.RESET_ALL)
    print()

def check_ip_type():
    ip = ipaddress.ip_address(args[1].split('/')[0])
    
    if ip.is_private:
        print('IP Type:', end=' ')
        print(Fore.LIGHTMAGENTA_EX + "Private" + Style.RESET_ALL)
    else:
        print('IP Type:', end=' ')
        print(Fore.LIGHTMAGENTA_EX + "Public" + Style.RESET_ALL)


def calc_ip():
    octets = str((args[1].split('/'))[0]).split('.')
    # Get the binary representation of the IP address
    print('IP Address:', end=' ')
    print(Fore.LIGHTMAGENTA_EX + f"{(args[1].split('/'))[0]}" + Style.RESET_ALL)
    binary_octets = [bin(int(octet))[2:].zfill(8) for octet in octets]
    ip_binary = '.'.join(binary_octets)
    print('IP Address (Binary):', end=' ')
    print(Fore.LIGHTMAGENTA_EX + f"{ip_binary}" + Style.RESET_ALL)

def calc_subnet():
    # Get the binary representation of the network mask
    mask_binary = '.'.join(format(int(octet), '08b') for octet in network.netmask.exploded.split('.'))
    # Split the binary string into 8-bit sections
    binary_octets = mask_binary.split('.')
    # Convert each binary section to decimal
    decimal_octets = [str(int(octet, 2)) for octet in binary_octets]
    # Join the decimal values into the final IP address
    decimal_ip = '.'.join(decimal_octets)
    print('Netmask:', end=' ')
    print(Fore.LIGHTMAGENTA_EX + f"{decimal_ip}" + Style.RESET_ALL)
    print('Netmask (Binary):', end=' ')
    print(Fore.LIGHTMAGENTA_EX + f"{mask_binary}" + Style.RESET_ALL)
    print('CIDR Notation:', end=' ')
    print(Fore.LIGHTMAGENTA_EX + f'/{(args[1].split("/"))[1]}' + Style.RESET_ALL)

def calc_network():
    # Get the network address
    network_address = network.network_address
    network_binary = '.'.join(format(int(octet), '08b') for octet in network.network_address.exploded.split('.'))
    print('Network Address:', end=' ')
    print(Fore.LIGHTMAGENTA_EX + f"{network_address}" + Style.RESET_ALL)
    print('Network Address (Binary):', end=' ')
    print(Fore.LIGHTMAGENTA_EX + f"{network_binary}" + Style.RESET_ALL)

def calc_broadcast():
    # Get the broadcast address
    broadcast_address = network.broadcast_address
    broadcast_binary = '.'.join(format(int(octet), '08b') for octet in network.broadcast_address.exploded.split('.'))
    print('Broadcast Address:', end=' ')
    print(Fore.LIGHTMAGENTA_EX + f"{broadcast_address}" + Style.RESET_ALL)
    print('Broadcast Address (Binary):', end=' ')
    print(Fore.LIGHTMAGENTA_EX + f"{broadcast_binary}" + Style.RESET_ALL)

def calc_usable_ip_range():
    # Calculate the first usable IP (network_address + 1)
    first_usable_ip = network.network_address + 1
    # Calculate the last usable IP (broadcast_address - 1)
    last_usable_ip = network.broadcast_address - 1
    
    # If it's a /31 or /32 network, there may be no usable IPs, so handle that
    if network.prefixlen >= 31:
        first_usable_ip = last_usable_ip = 'N/A'  # No usable IPs for /31 or /32 networks

    print('Usable IP Range:', end=' ')
    print(Fore.LIGHTMAGENTA_EX + f"{first_usable_ip} - {last_usable_ip}" + Style.RESET_ALL)

def calc_ips_number():
    total_ips = network.num_addresses
    if total_ips > 2:
        usable_ips = total_ips - 2
    else:
        usable_ips = total_ips # For /31 or /32, all IPs are usable
    print('Total IPs:', end=' ')
    print(Fore.LIGHTMAGENTA_EX + f"{total_ips}" + Style.RESET_ALL)
    print('Usable IPs:', end=' ')
    print(Fore.LIGHTMAGENTA_EX + f"{usable_ips}" + Style.RESET_ALL)

def run_tool():
    global args, network
    print_ascii()
    args = sys.argv
    if len(args) < 2:
        print(Fore.RED + 'Syntax: python3 whitefox.py 192.168.0.100/24' + Style.RESET_ALL)
        sys.exit()
    else:
        if '-h' in args:
            print_help()
            sys.exit()
        else:
            network = ipaddress.ip_network(args[1], strict=False)
            print()
            check_ip_type()
            calc_ip()
            try:
                calc_network()
                calc_subnet()
                calc_broadcast()
                calc_usable_ip_range()
                calc_ips_number()
            except Exception:
                pass

if __name__ == "__main__":
    try:
        run_tool()
    except KeyboardInterrupt:
        print(Fore.RED + 'Ctrl+C Detected! Exiting...' + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + 'Something Strange Happened While Launching The Tool!' + Style.RESET_ALL)
        print(e)
