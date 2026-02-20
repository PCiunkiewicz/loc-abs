FROM python:3.13-slim

RUN apt-get update && apt-get install -y gcc g++

WORKDIR /app
RUN pip install -U pip
RUN pip install dash==3.3.0 dash-bootstrap-components==2.0.4 plotly==6.4.0 numpy==2.2.2 pandas==2.3.2 loguru==0.7.3 yappi==1.6.10 dash_ag_grid==32.3.2 dash_daq==0.6.0
ENV DOCKERIZED=1

ENTRYPOINT ["python", "app.py"]
