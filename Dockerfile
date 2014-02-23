FROM crosbymichael/python

RUN pip install rethinkdb psutil
ADD . /files

ENTRYPOINT ["python", "/files/monitor.py"]

