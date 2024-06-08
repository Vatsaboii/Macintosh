FROM python:3.12.2-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY models/requirements.txt requirements_models.txt
RUN pip install -r requirements_models.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
