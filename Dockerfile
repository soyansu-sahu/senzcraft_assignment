

FROM python:3.9-slim

WORKDIR /app

# Install build essentials
RUN apt-get update && \
    apt-get install -y build-essential gcc libffi-dev
COPY . .
# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Expose port and set command
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
