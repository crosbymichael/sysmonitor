from psutil import cpu_times, cpu_percent, virtual_memory, swap_memory, disk_usage
from time import sleep
from os import getenv
import socket
import rethinkdb as r

duration = int(getenv('DURATION', 60))

def collect_data(hostname):
    return {
            'timestamp': r.now(),
            'host': hostname,
            'cpu': cpu_percent(),
            'memory': virtual_memory().percent,
            'swap': swap_memory().percent,
            'disk': disk_usage('/').percent,
    }

def monitor(conn, table):
    hostname = socket.gethostname()
    while True:
        data = collect_data(hostname)
        table.insert(data).run(conn)
        sleep(duration)
    conn.close()

def main():
    url = getenv('RETHINKDB_ADDR')
    if not url:
        raise Exception("RETHINKDB_ADDR not found in environment")
    conn = r.connect(host=url, db='metrics')
    monitor(conn, r.db(db_name).table('hosts'))

if __name__=='__main__': main()
