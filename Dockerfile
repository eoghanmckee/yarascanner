FROM python:3.7
MAINTAINER emckee
COPY . /app
WORKDIR /app
RUN mkdir -p tmp
RUN mkdir -p logs
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
