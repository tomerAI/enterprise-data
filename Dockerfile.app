# Dockerfile.app
FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY ./src/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy the src code
COPY ./src /app/src

EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
