#!/bin/bash

IMAGE_NAME="diabetis-predictor"
CONTAINER_NAME="diabetis_app"
HOST_PORT=8001
CONTAINER_PORT=8000

# Create Dockerfile dynamically
cat > Dockerfile <<EOF
# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY ./app ./app
COPY ./models ./models
COPY train_model_diabetis.py .

# Expose port
EXPOSE $CONTAINER_PORT

# Run uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$CONTAINER_PORT"]
EOF

echo "Dockerfile created."

# Stop and remove existing container if running
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
  echo "Stopping existing container $CONTAINER_NAME..."
  docker stop $CONTAINER_NAME
fi

if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
  echo "Removing existing container $CONTAINER_NAME..."
  docker rm $CONTAINER_NAME
fi

# Build Docker image
echo "Building Docker image $IMAGE_NAME..."
docker build -t $IMAGE_NAME:latest .

# Run Docker container
echo "Running Docker container $CONTAINER_NAME..."
docker run -d --name $CONTAINER_NAME -p $HOST_PORT:$CONTAINER_PORT $IMAGE_NAME:latest

# Wait for the FastAPI app to be ready before opening browser
URL="http://localhost:${HOST_PORT}/docs"
echo "Waiting for the app to be ready at $URL ..."
for i in {1..15}; do
  if curl -s --head "$URL" | grep "200 OK" > /dev/null; then
    echo "App is ready!"
    break
  else
    echo "Waiting... ($i)"
    sleep 1
  fi
done

# Open Swagger UI in browser
echo "Opening Swagger UI in browser at $URL ..."
if which xdg-open &> /dev/null; then
  xdg-open "$URL"
elif which open &> /dev/null; then
  open "$URL"
else
  echo "Please open $URL in your browser manually."
fi

echo "Done! FastAPI app running at $URL"
