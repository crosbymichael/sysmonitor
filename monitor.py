from psutil import cpu_times, cpu_percent, virtual_memory, swap_memory, disk_usage
from time import sleep
from os import getenv
from influxdb import InfluxDBClient

duration = int(getenv('DURATION', 60))

def collect_data(table):
    return [{
        'points': [
            [cpu_percent(), virtual_memory().percent, swap_memory().percent, disk_usage('/').percent]
        ],
        'name': table,
        'columns': ['cpu', 'memory', 'swap', 'disk']
    }]

def monitor(client, table):
    while True:
        data = collect_data(table)
        client.write_points(data)
        sleep(duration)

def main():
    host = getenv('INFLUX_HOST')
    user = getenv('INFLUX_USER')
    password = getenv('INFLUX_PASSWORD')
    db = getenv('INFLUX_DB')
    table = getenv('INFLUX_TABLE')

    client = InfluxDBClient(host, 8086, user, password, db)

    monitor(client, table)

if __name__=='__main__': main()
