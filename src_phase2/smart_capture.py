import cv2
import os
import time

# ===== CHANGE WORD HERE =====
word = "STOP"
# ============================

save_dir = f"../data/word_frames/{word}"

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

existing_files = len(os.listdir(save_dir))
count = existing_files

total_images = 150
images_per_phase = 30

# 🔥 Updated for TWO HANDS
phases = [
    "Phase 1: BOTH hands CLOSE to camera",
    "Phase 2: BOTH hands FAR from camera",
    "Phase 3: Tilt BOTH hands LEFT",
    "Phase 4: Tilt BOTH hands RIGHT",
    "Phase 5: Natural movement with BOTH hands"
]

print(f"Starting 2-hand smart capture for word: {word}")
print(f"Already existing images: {existing_files}")

cap = cv2.VideoCapture(0)

current_phase = 0
phase_count = 0

print("Press SPACE to start auto capture")
print("Press Q to quit")

auto_capture = False
last_capture_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Display instructions
    cv2.putText(frame, f"Word: {word}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), 2)

    cv2.putText(frame, phases[current_phase], (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (255, 0, 0), 2)

    cv2.putText(frame, f"Captured: {count}", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 255), 2)

    cv2.putText(frame, "⚠ Show BOTH hands clearly", (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 0, 255), 2)

    cv2.imshow("Smart Capture (2-Hand)", frame)

    key = cv2.waitKey(1)

    if key == ord(' '):
        auto_capture = True

    if key == ord('q'):
        break

    if auto_capture:
        current_time = time.time()

        # Capture every 0.4 sec
        if current_time - last_capture_time > 0.4:
            filename = os.path.join(save_dir, f"{count}.jpg")
            cv2.imwrite(filename, frame)

            count += 1
            phase_count += 1
            last_capture_time = current_time

            if phase_count >= images_per_phase:
                current_phase += 1
                phase_count = 0

                if current_phase >= len(phases):
                    print("150 images captured successfully!")
                    break

cap.release()
cv2.destroyAllWindows()

print("2-hand smart capture completed.")