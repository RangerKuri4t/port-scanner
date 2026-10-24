import socket, concurrent.futures, time, argparse



parser = argparse.ArgumentParser(description="Port Scanner")
parser.add_argument("target", help="Target IP address or hostname")
parser.add_argument("start_port", type=int, help="Starting port number")
parser.add_argument("end_port", type=int, help="Ending port number")
parser.add_argument("-t",  "--timeout", type=float, default=1.0, help="Timeout in seconds (default: 1.0)")
parser.add_argument("-w", "--workers", type=int, default=100, help="Number of threads (default: 100)")


args = parser.parse_args()
target_ip = socket.gethostbyname(args.target)
start_port = args.start_port
end_port = args.end_port


def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(args.timeout)
        s.connect((target_ip, port))
        s.close()
        return port, True
    except:
        s.close()
        return port, False  





def scan_ports():
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(scan_port, range(start_port, end_port + 1)))
    for result in results:
        port_name = get_ServiceName(result[0])
        port, is_open = result
        if is_open:
            print(f"Port {port} ({port_name}) is open")
        else:
            if(end_port - start_port) < 100:
                print(f"Port {port} ({port_name}) is closed")
        
def get_ServiceName(port):
    try:
        service_name = socket.getservbyport(port)
        return service_name
    except OSError:
        return "Unknown Service"

if start_port < 1 or end_port > 65535 or start_port > end_port:
    print("Invalid port range. Please enter a valid range between 1 and 65535.")
else:
    scan_ports()
    #scan_ports()
    




