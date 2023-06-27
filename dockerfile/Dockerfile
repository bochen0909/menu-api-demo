FROM python:3.10
LABEL maintainer="Bo Chen <bochen0909@gmail.com>"

RUN pip install --no-cache-dir \
fastapi==0.98.0 \
uvicorn[standard]==0.22.0 \
beautifulsoup4==4.12.2 \
elasticsearch==8.8.0 

RUN apt-get update && apt-get install -y iputils-ping

ARG CACHEBUST=0 
RUN git clone https://github.com/bochen0909/menu-api-demo.git  /menu-api-demo && ln -s /menu-api-demo/scripts/load_data_elasticsearch.py /usr/bin/
ENV DATA_HOME=/menu-api-demo/data/restaurants/ 
ENV PYTHONPATH=/menu-api-demo/src
CMD  uvicorn app.main:app --host 0.0.0.0

