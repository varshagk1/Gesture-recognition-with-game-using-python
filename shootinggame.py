import cv2
import mediapipe as mp
import random
import math

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

# Game settings
WIDTH, HEIGHT = 800, 600
target_radius = 30
bullet_radius = 8
targets = [{"x": random.randint(100, WIDTH - 100), "y": random.randint(100, HEIGHT - 100)} for _ in range(5)]
bullets = []
score = 0

# Function to detect finger and gesture
def detect_hand(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    finger_pos = None
    shoot = False
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            index_tip = handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = handLms.landmark[mp_hands.HandLandmark.THUMB_TIP]
            h, w, _ = frame.shape
            finger_pos = (int(index_tip.x * w), int(index_tip.y * h))
            # Detect thumbs up for shooting
            if thumb_tip.y < handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y:
                shoot = True
    return finger_pos, shoot

# Open webcam
cap = cv2.VideoCapture(0)

print("🕹️ Raise your hand to aim. Thumbs up to shoot. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Detect hand and gesture
    finger_pos, shoot = detect_hand(frame)

    # Draw targets
    for target in targets:
        cv2.circle(frame, (target["x"], target["y"]), target_radius, (0, 0, 255), -1)

    # Draw bullets and move them
    for bullet in bullets:
        bullet["y"] -= 20
        cv2.circle(frame, (bullet["x"], bullet["y"]), bullet_radius, (0, 255, 255), -1)

    # Remove bullets that go off-screen
    bullets = [b for b in bullets if b["y"] > 0]

    # Detect collisions
    for bullet in bullets[:]:
        for target in targets[:]:
            dist = math.hypot(bullet["x"] - target["x"], bullet["y"] - target["y"])
            if dist < target_radius + bullet_radius:
                bullets.remove(bullet)
                targets.remove(target)
                score += 1
                targets.append({
                    "x": random.randint(100, WIDTH - 100),
                    "y": random.randint(100, HEIGHT - 100)
                })
                break

    # Shooting gesture creates new bullet
    if finger_pos:
        cv2.circle(frame, finger_pos, 10, (0, 255, 0), -1)
        if shoot:
            bullets.append({"x": finger_pos[0], "y": finger_pos[1]})
            cv2.putText(frame, "BANG!", (finger_pos[0]-30, finger_pos[1]-20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Draw score
    cv2.putText(frame, f"Score: {score}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

    # Show window
    cv2.imshow("Gesture Shooting Game", frame)

    # Quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
