FROM crosbymichael/hy

RUN pip install psutil influxdb
ADD . /files

ENTRYPOINT ["hy", "/files/monitor.hy"]

