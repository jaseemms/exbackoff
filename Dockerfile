FROM python:3.9.6-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN addgroup -S app && adduser -S app -G app
RUN chown -R app:app /home/app
RUN mkdir /home/app/staticfiles
RUN chmod a+rwx -R /home/app/staticfiles

ENV PATH="/home/app/.local/bin:${PATH}"

USER app
WORKDIR /home/app

COPY . .

RUN sed -i 's/\r$//g' /home/app/entrypoint.sh
RUN chmod +x /home/app/entrypoint.sh

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000