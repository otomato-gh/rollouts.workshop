FROM python:alpine
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD flask --app api run -h 0.0.0.0
