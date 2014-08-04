FROM crosbymichael/python

RUN pip install influxdb psutil
ADD . /monitor

ENTRYPOINT ["python", "/monitor/monitor.py"]

