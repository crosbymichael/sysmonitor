(import [psutil [cpu_times cpu_percent virtual_memory swap_memory disk_usage]])
(import [time [sleep]])
(import [influxdb [InfluxDBClient]])
(import [os [getenv]])

(def client (InfluxDBClient "influxdb.production.docker" 8086 "hy" "reporter" "metrics"))
(def duration (int (getenv "DURATION" 5)))
(def series_name (getenv "SERIES_NAME" "system"))

(defn write [data]
    (client.write_points [data]))

(defn get_data []
    (def cpup (cpu_percent))
    (def vmem (virtual_memory))
    (def smem (swap_memory))
    (def disk (disk_usage "/"))
    
    {"points" [[cpup vmem.percent smem.percent disk.percent]] "name" series_name "columns" ["cpu" "memory" "swap" "disk"]})

(while true
    (write (get_data))
    (sleep duration))
