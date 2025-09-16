import cv2
import mediapipe as mp
import time

# Morse dictionary
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D',
    '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H',
    '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P',
    '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z',
    '-----':'0', '.----':'1', '..---':'2', '...--':'3',
    '....-':'4', '.....':'5', '-....':'6', '--...':'7',
    '---..':'8', '----.':'9'
}

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

cap = cv2.VideoCapture(0)

morse_input = ""
decoded_text = ""
last_signal_time = time.time()
last_input_time = time.time()
RESET_DELAY = 10  # detik

def decode_morse(morse_str):
    return MORSE_CODE_DICT.get(morse_str, '')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    signal = None

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # ambil posisi jari
            landmarks = hand_landmarks.landmark
            h, w, _ = frame.shape
            finger_y = [landmarks[i].y for i in [8, 12]]  # telunjuk (8), tengah (12)

            # normalisasi -> bandingin sama pergelangan (0)
            wrist_y = landmarks[0].y

            telunjuk_up = finger_y[0] < wrist_y - 0.05
            tengah_up = finger_y[1] < wrist_y - 0.05

            if telunjuk_up and not tengah_up:
                signal = "."
            elif telunjuk_up and tengah_up:
                signal = "-"

    # kalau ada sinyal baru
    if signal:
        if time.time() - last_signal_time > 0.8:  # kasih jeda biar ga spam
            morse_input += signal
            last_signal_time = time.time()
            last_input_time = time.time()

    # kalau udah berhenti lebih dari 2 detik → decode jadi huruf
    if morse_input and time.time() - last_signal_time > 2:
        decoded_text += decode_morse(morse_input)
        morse_input = ""

    # kalau idle lebih dari 5 detik → reset
    if time.time() - last_input_time > RESET_DELAY:
        decoded_text = ""

    # tampilkan teks di pojok kiri atas
    cv2.putText(frame, f"Morse: {morse_input}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Text: {decoded_text}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Morse Hand Translator", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
