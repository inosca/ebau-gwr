FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev wget build-essential \
&& wget -q https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /usr/local/bin \
&& chmod +x /usr/local/bin/wait-for-it.sh \
&& mkdir -p /app \
&& useradd -u 901 -r ebau-gwr --create-home \
# all project specific folders need to be accessible by newly created user but also for unknown users (when UID is set manually). Such users are in group root.
&& chown -R ebau-gwr:root /home/ebau-gwr \
&& chmod -R 770 /home/ebau-gwr

# needs to be set for users with manually set UID
ENV HOME=/home/ebau-gwr

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE ebau_gwr.settings
ENV APP_HOME=/app
ENV UWSGI_INI /app/uwsgi.ini

RUN pip install -U poetry

ARG INSTALL_DEV_DEPENDENCIES=false
COPY pyproject.toml poetry.lock $APP_HOME/
RUN if [ "$INSTALL_DEV_DEPENDENCIES"  = "true" ]; then poetry install --no-root; else poetry install --no-dev --no-root; fi

USER ebau-gwr

COPY . $APP_HOME

EXPOSE 8000

CMD /bin/sh -c "wait-for-it.sh $DATABASE_HOST:${DATABASE_PORT:-5432} -- poetry run ./manage.py migrate && uwsgi"
