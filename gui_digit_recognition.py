from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image
import numpy as np
import matplotlib.pyplot as plt
model = load_model('mnist.keras')

def predict_digit(img):
    img = img.resize((28,28))
    img = img.convert("L")
    img = np.array(img)
    img = 255 - img
    img = img / 255.0
    img = img.reshape(1, 28, 28, 1)
    
    
    plt.imshow(img[0, :, :, 0], cmap='gray')
    plt.show()


    res = model.predict(img)[0]
    print("Predicted probabilities:", res)
    confidence = max(res)
    predicted_digit = np.argmax(res)

    if confidence > 0.8:  
        print("Predicted digit:", predicted_digit, "with confidence:", confidence)
        return predicted_digit, confidence
    else:
        print("Not confident enough")
        return "Not confident enough", confidence


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.x = self.y = 0
        
        self.canvas = tk.Canvas(self, width = 300, height=300, bg = "white", cursor = "cross")
        self.label = tk.Label(self, text = "Draw...", font = ("Helvetica", 48))
        self.classify_btn = tk.Button(self, text = "recognise", command = self.classify_handwriting)
        self.button_clear = tk.Button(self, text = "clear", command = self.clear_all)
        
        self.canvas.grid(row=0, column=0, pady=2, sticky=W)
        self.label.grid(row=0, column=1, pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=0, column=0, pady=2)
        
        self.canvas.bind("<B1-Motion>", self.draw_lines)
    
    def clear_all(self):
        self.canvas.delete("all")
        
    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)
        a,b,c,d = rect
        rect = (a+4, b+4, c-4, d-4)
        im = ImageGrab.grab(rect)
        
        digit, acc = predict_digit(im)
        result_text = self.label.configure(text = str(digit)+', '+ str(int(acc*100))+'%')
        if acc < 0.7:  
            suggestion_text = " - Suggestions: " + ", ".join([f"{s[0]} ({int(s[1] * 100)}%)" for s in suggestions])
            result_text += suggestion_text
        
        self.label.configure(text=result_text)
        
    def draw_lines(self, event):
            self.x = event.x
            self.y = event.y
            r=8
            self.canvas.create_oval(self.x-r, self.y-r, self.x+r, self.y+r, fill='black')

app = App()
mainloop()