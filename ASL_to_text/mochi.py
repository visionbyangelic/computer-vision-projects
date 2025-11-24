# mochi.py
# A real-time ASL-to-text chat app with pink UI, using a CNN for 29 classes (A-Z + del, space, nothing).
import customtkinter as ctk
import cv2
import mediapipe as mp
import threading
import time
import numpy as np
import tensorflow as tf

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mochi - Sign & Chat")
        self.geometry("600x600")
        self.configure(fg_color="#FFE0EA")  # Fixed: Use fg_color for CustomTkinter.

        self.chat_frame = ctk.CTkScrollableFrame(self, width=380, height=500, fg_color="#FFD0DF")
        self.chat_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.input_frame = ctk.CTkFrame(self, fg_color="#FFC0D4")
        self.input_frame.pack(pady=5, padx=10, fill="x")
        
        self.message_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Type or sign a message...", width=250, fg_color="#FFF0F5", text_color="black")
        self.message_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        self.message_entry.bind("<Return>", lambda event: self.send_message())
        
        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message, fg_color="#cf2c89", hover_color="#f2adad")
        self.send_button.pack(side="right", padx=5, pady=5)
        
        self.sign_mode = False
        self.sign_button = ctk.CTkButton(self.input_frame, text="Sign Mode: Off", command=self.toggle_sign_mode, fg_color="#cf2c89", hover_color="#f2adad")
        self.sign_button.pack(side="right", padx=5, pady=5)

        self.mp_hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.cap = None
        self.sign_thread = None
        self.is_detecting = False  # Added: Thread safety flag.
        self.last_sign_time = 0
        
        # Load the 29-class model.
        self.model = tf.keras.models.load_model("asl_29_model.keras")
        self.letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["del", "space", "nothing"]  # 29 classes.

    def send_message(self):
        message = self.message_entry.get().strip()
        if message:
            msg_label = ctk.CTkLabel(self.chat_frame, text=f"You: {message}", fg_color="#FFF0F5", text_color="black", padx=10, pady=5, anchor="e")
            msg_label.pack(padx=5, pady=2, fill="x", anchor="e")
            self.message_entry.delete(0, "end")

    def toggle_sign_mode(self):
        self.sign_mode = not self.sign_mode
        self.sign_button.configure(text=f"Sign Mode: {'On' if self.sign_mode else 'Off'}")
        print(f"Sign Mode toggled to: {self.sign_mode}")
        if self.sign_mode:
            self.start_sign_detection()
        else:
            self.stop_sign_detection()

    def start_sign_detection(self):
        if self.is_detecting:
            print("Detection already running!")
            return
        if not self.cap:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Error: Could not open webcam.")
                self.toggle_sign_mode()
                return
            print("Webcam opened successfully.")
        self.is_detecting = True
        self.sign_thread = threading.Thread(target=self.detect_signs, daemon=True)
        self.sign_thread.start()
        print("Sign detection thread started.")

    def stop_sign_detection(self):
        self.is_detecting = False
        if self.cap:
            self.cap.release()
            self.cap = None
            print("Webcam stopped.")
        if cv2.getWindowProperty("Mochi Sign Detection", cv2.WND_PROP_VISIBLE) >= 1:  # Fixed: Safe window check.
            cv2.destroyAllWindows()

    def detect_signs(self):
        print("Starting sign detection loop...")
        while self.sign_mode and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to read frame from webcam.")
                break
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.mp_hands.process(frame_rgb)

            current_time = time.time()
            if not results.multi_hand_landmarks:
                # No hand = predict 'nothing' explicitly.
                landmark_array = np.zeros(63)  # Zero vector for 'nothing'.
                landmark_array = np.expand_dims(landmark_array, axis=0)
            else:
                if current_time - self.last_sign_time < 1:
                    continue
                hand_landmarks = results.multi_hand_landmarks[0]
                landmark_array = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()
                if len(landmark_array) != 63:  # Fixed: Safety check for landmark count.
                    print("Error: Unexpected landmark count, skipping prediction.")
                    continue
                landmark_array = np.expand_dims(landmark_array, axis=0)

            # Predict using the 29-class model.
            prediction = self.model.predict(landmark_array, verbose=0)
            sign_idx = np.argmax(prediction)
            
            if sign_idx >= len(self.letters):  # Shouldn’t happen, but safety first.
                print(f"Error: sign_idx {sign_idx} out of range for {len(self.letters)} classes.")
                continue
            
            sign = self.letters[sign_idx]
            print(f"Detected '{sign}'")
            
            # Handle signs explicitly—cleaner logic.
            if sign == "del":
                children = self.chat_frame.winfo_children()
                if children:  # Fixed: Explicit empty check.
                    children[-1].destroy()
                    self.last_sign_time = current_time
            elif sign == "space":
                self.message_entry.insert("end", " ")
                self.last_sign_time = current_time
            elif sign == "nothing":
                pass  # Do nothing, explicitly.
            else:  # A-Z or other signs.
                self.message_entry.insert("end", sign)
                self.last_sign_time = current_time

            cv2.imshow("Mochi Sign Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.stop_sign_detection()
        print("Sign detection stopped.")

    def destroy(self):
        self.stop_sign_detection()
        super().destroy()

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()