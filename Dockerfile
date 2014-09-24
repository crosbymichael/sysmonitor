FROM crosbymichael/python

RUN pip install rethinkdb psutil
ADD . /monitor

ENTRYPOINT ["python", "/monitor/monitor.py"]

