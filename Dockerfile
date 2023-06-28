# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Install system libraries required for PyTorch
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev

# Add current directory code to /app in the container
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install deps for mmdet
RUN pip install timm==0.4.9 einops

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
CMD ["python", "main.py"]
