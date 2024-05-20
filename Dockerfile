FROM python:3.9-slim

# Install necessary dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . /app
WORKDIR /app

# Command to run the main application
CMD ["python", "main.py"]
