from psutil import cpu_times, cpu_percent, virtual_memory, swap_memory, disk_usage
from time import sleep
from os import getenv
import rethinkdb as r

duration = int(getenv('DURATION', 60))

def collect_data():
    return {
            'timestamp': r.now(),
            'cpu': cpu_percent(),
            'memory': virtual_memory().percent,
            'swap': swap_memory().percent,
            'disk': disk_usage('/').percent,
    }

def monitor(conn, table):
    while True:
        data = collect_data()
        table.insert(data).run(conn)
        sleep(duration)
    conn.close()

def main():
    url = getenv('RETHINK_ADDR')
    if not url:
        raise Exception("RETHINK_ADDR not found in environment")
    db_name = getenv('RETHINK_NAME')
    if not db_name:
        raise Exception("RETHINK_NAME not found in environment")
    conn = r.connect(host=url, db=db_name)
    monitor(conn, r.db(db_name).table('metrics_system'))

if __name__=='__main__': main()
