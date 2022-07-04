# FROM python:3.9.13-buster
# FROM python:3.9.13-alpine
FROM long0709/python-with-pip:3.9.13-alpine

USER root
# create the app user
# RUN addgroup --system app && adduser --system --group app
RUN addgroup -S app && adduser -S app -G app

WORKDIR /app

COPY . /app
RUN chmod +x run.sh
# RUN apk add -u zlib-dev jpeg-dev gcc musl-dev python3-dev libffi-dev openssl-dev cargo
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt
ENV PYTHONPATH=/app

# chown all the files to the app user
RUN chown -R app:app $HOME
RUN chown -R app:app /app

# change to the app user
# Switch to a non-root user
USER app
# Run the run script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Uvicorn
CMD ["./run.sh"]
# CMD ["sh", "-c", "tail -f /dev/null"]