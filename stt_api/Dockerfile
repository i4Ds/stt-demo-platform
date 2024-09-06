FROM python:3.9.12-alpine

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app


RUN mkdir /home/app/web

WORKDIR /home/app/web

# copy project
COPY . /home/app/web

# install dependencies
RUN pip --no-cache-dir install --upgrade pip & \
    pip --no-cache-dir install -r requirements.txt

RUN chmod +x  /home/app/web/entrypoint.sh

# chown all the files to the app user
RUN chown -R app:app /home/app/web

# change to the app user
USER app

# ENTRYPOINT [ "/home/app/web/entrypoint.sh" ]
