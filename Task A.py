import cv2
import numpy as np
import matplotlib.pyplot as plt

# === DISABLE OpenCL to avoid memory errors ===
cv2.ocl.setUseOpenCL(False)

# === PARAMETERS ===
BRIGHTNESS_THRESHOLD = 100

# === USER INPUT ===
video_path = input("Enter video path (e.g., 'street.mp4'): ").strip()

# === OPEN VIDEO ===
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# === READ FIRST 50 FRAMES TO CHECK BRIGHTNESS ===
brightness_values = []
for _ in range(50):
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    brightness_values.append(brightness)

cap.release()

# === CHECK IF FRAMES WERE READ ===
if not brightness_values:
    print("Error: No frames read from the video.")
    exit()

# === CALCULATE AVERAGE BRIGHTNESS ===
average_brightness = np.mean(brightness_values)
print("Average Brightness:", average_brightness)

# === CLASSIFY DAY OR NIGHT ===
if average_brightness >= BRIGHTNESS_THRESHOLD:
    print("This is likely a daytime video.")
else:
    print("This is likely a nighttime video.")

# === PLOT HISTOGRAM OF BRIGHTNESS ===
plt.figure(figsize=(8, 5))
plt.hist(brightness_values, bins=20, color='blue', edgecolor='black')
plt.title('Brightness Distribution (First 50 Frames)')
plt.xlabel('Average Brightness per Frame')
plt.ylabel('Number of Frames')
plt.grid(True)
plt.tight_layout()
plt.show()


#Part5_addEndScreen

# Part 1: Set input/output info
# Open the first video
video1 = cv2.VideoCapture("street.mp4")

# Open the second video
video2 = cv2.VideoCapture("endscreen.mp4")

# Make sure both videos are opened successfully
if not video1.isOpened() or not video2.isOpened():
    print("Error opening one of the videos.")
    exit()

# Get properties (assuming both videos have same resolution and FPS)
fps = video1.get(cv2.CAP_PROP_FPS)  # Should be 30.0
width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create output writer
out = cv2.VideoWriter("merged_video.avi",
                      cv2.VideoWriter_fourcc(*"MJPG"),
                      fps,
                      (width, height))

# Part 2: Write frames of Video 1
# Get total frames in Video 1
total_frames_v1 = int(video1.get(cv2.CAP_PROP_FRAME_COUNT))

for frame_count in range(total_frames_v1):
    success, frame = video1.read()  # Read a frame
    if not success:
        break  # End if read fails
    out.write(frame)  # Write to output

# Part 3: Write frames of Video 2
# Get total frames in Video 2
total_frames_v2 = int(video2.get(cv2.CAP_PROP_FRAME_COUNT))

for frame_count in range(total_frames_v2):
    success, frame = video2.read()  # Read a frame
    if not success:
        break  # End if read fails
    out.write(frame)  # Append to output

# Part 4: Release resources
video1.release()
video2.release()
out.release()

print("Merged video created successfully.")