import psutil
from flask import Flask, Response

app = Flask(__name__)

# Initialize cpu_percent to establish a baseline
psutil.cpu_percent(interval=None)

@app.route('/metrics')
def metrics():
    cpu = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()

    lines = [
        "# HELP system_cpu_percent CPU usage percentage",
        "# TYPE system_cpu_percent gauge",
        f"system_cpu_percent {cpu}",
        
        "# HELP system_memory_percent Memory usage percentage",
        "# TYPE system_memory_percent gauge",
        f"system_memory_percent {mem.percent}",
        
        "# HELP system_disk_percent Disk usage percentage",
        "# TYPE system_disk_percent gauge",
        f"system_disk_percent {disk.percent}",
        
        "# HELP system_network_bytes_sent Network bytes sent",
        "# TYPE system_network_bytes_sent gauge",
        f"system_network_bytes_sent {net.bytes_sent}",
        
        "# HELP system_network_bytes_recv Network bytes received",
        "# TYPE system_network_bytes_recv gauge",
        f"system_network_bytes_recv {net.bytes_recv}"
    ]
    return Response("\n".join(lines) + "\n", mimetype='text/plain')

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9100)
