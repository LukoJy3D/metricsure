FROM python:3.13-slim

COPY * .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "validate.py"]
