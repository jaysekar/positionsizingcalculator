FROM python:3.9-slim

WORKDIR /position_calculator

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV PYTHONPATH=/position_calculator

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

