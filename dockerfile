FROM python:3.9
WORKDIR /app

# Install the application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# We now want to copy the rest of the app into the container
COPY . .
RUN chmod +x run.sh

# Start the app
ENTRYPOINT ["./run.sh"]