# Dockerfile
# This file defines how to build the Physio app

FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all other files (app.py, *.pkl)
COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
