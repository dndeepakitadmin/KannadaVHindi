FROM python:3.10

WORKDIR /app

# Copy everything into the image
COPY . /app

# Install your dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run your script
CMD ["python", "app.py"]
