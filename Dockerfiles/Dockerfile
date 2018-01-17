FROM ello/python-webapp

COPY . /app

ENV FIREBIRD_HOST=127.0.0.1
ENV FIREBIRD_USER=sysdba
ENV FIREBIRD_PASSWORD=masterkey

ENV TZ=America/Cuiaba
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

CMD ["gunicorn", "-w", "4", "-c", "gunicorn.conf", "run:app"]
