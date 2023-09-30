FROM python:latest
WORKDIR /app
COPY requirements.txt /app/
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "api.py"]
