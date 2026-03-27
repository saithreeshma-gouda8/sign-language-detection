import cv2
import mediapipe as mp
import numpy as np
import os

INPUT_DIR = "../data/word_frames"
OUTPUT_DIR = "../data/landmarks_2hand"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

for word in os.listdir(INPUT_DIR):

    word_path = os.path.join(INPUT_DIR, word)
    if not os.path.isdir(word_path):
        continue

    print(f"\nProcessing word: {word}")

    data = []

    for img_name in os.listdir(word_path):

        img_path = os.path.join(word_path, img_name)
        image = cv2.imread(img_path)

        if image is None:
            continue

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        sample = []

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks[:2]:

                base_x = hand.landmark[0].x
                base_y = hand.landmark[0].y

                for lm in hand.landmark:
                    sample.append(lm.x - base_x)
                    sample.append(lm.y - base_y)

        while len(sample) < 84:
            sample.append(0)

        if len(sample) == 84:
            data.append(sample)

    data = np.array(data)
    np.save(os.path.join(OUTPUT_DIR, f"{word}.npy"), data)

print("\n2-hand landmark extraction completed.")