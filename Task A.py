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
