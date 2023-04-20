FROM python:3.10
WORKDIR /movies_admin
ENV DJANGO_SETTINGS_MODULE "config.settings"
COPY .env .env 
COPY ./requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip3 install -r requirements.txt --no-cache-dir
COPY . .
EXPOSE 8000
ENTRYPOINT ["bash", "backend_up.sh"]
