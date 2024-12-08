# Use the official Python image as a base
FROM python:3.12.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Flask app code into the container
COPY . .

# Expose the Flask app port
EXPOSE 5000

# Add environment variable support
ENV FLASK_APP=main.py
ENV FLASK_ENV=development

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
