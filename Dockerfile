FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install .
CMD ["uvicorn", "sysmon_api:app", "--host", "0.0.0.0", "--port", "8000"]

