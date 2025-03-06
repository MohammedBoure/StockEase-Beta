import socket
import ipaddress
import concurrent.futures

network = "192.168.1.0/24"
port = 3306
timeout = 1

def check_network(ip, port):
    """يتحقق مما إذا كان هناك اتصال بعنوان IP معين وبورت معين"""
    try:
        socket.setdefaulttimeout(timeout)
        with socket.create_connection((ip, port)):
            return ip
    except (socket.timeout, socket.error):
        return None

def scan_network(network, port):
    """يقوم بمسح الشبكة بالكامل لاكتشاف الأجهزة التي تعمل على بورت 3306"""
    alive_ips = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda ip: check_network(str(ip), port), ipaddress.IPv4Network(network).hosts())

    for result in results:
        if result:
            alive_ips.append(result)

    return alive_ips

# تشغيل المسح وإظهار النتائج
found_ips = scan_network(network, port)

print("\n🔍 الأجهزة التي تعمل عليها MySQL:")
if found_ips:
    for ip in found_ips:
        print(f"✅ MySQL متاح على: {ip}")
else:
    print("❌ لم يتم العثور على أي أجهزة تعمل على بورت 3306")
