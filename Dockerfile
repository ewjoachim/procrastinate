FROM python:3

WORKDIR /procrastinate_dev/
COPY . ./
RUN pip install -r requirements.txt

ENTRYPOINT ["procrastinate"]
CMD ["--help"]
