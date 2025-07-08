# FROM python:3.8-alpine
# COPY . /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# CMD python app.py


FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]