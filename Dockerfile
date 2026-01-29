# Use Python 3.9 
FROM python:3.9-slim

# 1. XGBOOST: Install 'libgomp1'

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 2. SECURITY FIX: Create user "choreouser" (ID 10014)
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid 10014 \
    "choreouser"

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 3. PERMISSION FIX
RUN chown -R 10014:10014 /app

# 4. SWITCH USER
USER 10014

# 5. PORT FIX
EXPOSE 8501

# 6. RUN COMMAND

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
