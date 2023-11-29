FROM python:3.10.12
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERD=1
WORKDIR /code/
COPY requirements.txt /code/
RUN pip install -r  requirements.txt
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY . /code/