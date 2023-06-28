import os
import cv2
import subprocess
import torch
from torchvision import transforms
from PIL import Image

# Constants
RESOLUTION_H = 256 # Based on ViTPose-H
RESOLUTION_W = 192 # Based on ViTPose-H
MODEL_PATH = 'model.h5'  # Path to the trained model

# Load the trained model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.load(MODEL_PATH, map_location=device)
model.eval()  # Set the model to evaluation mode

# Define the transformation
transform = transforms.Compose([
    transforms.Resize((RESOLUTION_W, RESOLUTION_H)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Standard ImageNet mean and std
])

# Download the YouTube video.
def download_video(url, filename):
    command = ['youtube-dl', url, '-o', filename]
    subprocess.run(command)

# Split the video into frames.
def split_into_frames(filename):
    vidcap = cv2.VideoCapture(filename)
    success, image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(f'frame{count}.jpg', image)
        success, image = vidcap.read()
        count += 1

# Analyze a frame using the trained model.
def analyze_frame(filename):
    img = Image.open(filename)
    img_tensor = transform(img)
    img_tensor = img_tensor.unsqueeze(0).to(device)  # Add batch dimension and send to device
    prediction = model(img_tensor)
    return prediction

def main():
    # Get the URL of the YouTube video from environment variable
    url = os.getenv('DEV_TEST_VIDEO')
    if not url:
        raise ValueError("Please set the DEV_TEST_VIDEO environment variable")
    video_filename = 'video.mp4'

    # Download the video and split it into frames.
    download_video(url, video_filename)
    split_into_frames(video_filename)

    # Analyze each frame and print the results.
    for i in range(0, count):  # Assuming count is the number of frames
        filename = f'frame{i}.jpg'
        prediction = analyze_frame(filename)
        print(prediction)  # TODO: Change this to output video

if __name__ == '__main__':
    main()
