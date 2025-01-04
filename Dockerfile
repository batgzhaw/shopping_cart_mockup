FROM python:3.11.3
WORKDIR /usr/src/app
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt
COPY . /usr/src/app
CMD [ "./app_entrypoint.sh" ]
