FROM continuumio/miniconda3:4.8.2-alpine

# COPY necessary files inside
ADD ./data /opt/web/data
ADD ./src /opt/web
WORKDIR /opt/web
COPY environment.yml /opt/web
COPY start.sh /opt/web

RUN conda update -y conda && \
    conda env create -f environment.yml

CMD bash ./start.sh
