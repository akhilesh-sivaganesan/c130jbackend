FROM lmregistry.us.lmco.com/ext.hub.docker.com/library/python:3.9

# set working directory
WORKDIR /app
RUN mkdir -p app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD ["base.py" ]