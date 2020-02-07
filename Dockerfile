FROM python:3.7-buster

WORKDIR /procrastinate_dev/
COPY requirements.txt ./
COPY setup.* ./
COPY procrastinate ./procrastinate/
RUN pip install -r requirements.txt

COPY procrastinate_demo ./procrastinate_demo/

ENTRYPOINT ["procrastinate"]
CMD ["--help"]
