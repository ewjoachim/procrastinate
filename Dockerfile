FROM python:3

WORKDIR /procrastinate_dev/
COPY requirements.txt setup.* ./
COPY procrastinate ./procrastinate/
RUN pip install -r requirements.txt

ENTRYPOINT ["procrastinate"]
CMD ["--help"]
