FROM python:3.8.7-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python"]