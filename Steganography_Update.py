import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

selected_image_path = ""

def select_image():
    global selected_image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        selected_image_path = file_path
        load_preview(file_path, label_image_preview)

def select_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_output_folder.delete(0, tk.END)
        entry_output_folder.insert(0, folder_path)

def encrypt_message():
    image_path = entry_image_path.get()
    message = entry_message.get("1.0", tk.END).strip()
    password = entry_password.get()
    output_folder = entry_output_folder.get()
    
    
    if not image_path or not message or not password or not output_folder:
        messagebox.showerror("Error", "Please select an image, enter message, password, and output folder")
        return
    
    img = cv2.imread(image_path)
    d = {chr(i): i for i in range(255)}
    n, m, z = 0, 0, 0
    
    full_message = password + message  # Embed password in image for verification
    for i in range(len(full_message)):
        img[n, m, z] = d[full_message[i]]
        n = (n + 1) 
        m = (m + 1) 
        z = (z + 1) % 3
    
    encrypted_path = os.path.join(output_folder, "encrypted_image.png")
    cv2.imwrite(encrypted_path, img)
    messagebox.showinfo("Success", "Message encrypted successfully! Encrypted image saved.")
    load_preview(encrypted_path, label_encrypted_preview)

def request_password():
    if not selected_image_path:
        messagebox.showerror("Error", "Please select an image first!")
        return
    
    password_window = tk.Toplevel(root)
    password_window.title("Enter Decryption Password")
    
    tk.Label(password_window, text="Enter Password:").pack(pady=5)
    entry_decrypt_password = tk.Entry(password_window, show="*", width=30)
    entry_decrypt_password.pack(pady=5)
    
    def submit_password():
        password = entry_decrypt_password.get()
        password_window.destroy()
        decrypt_message(selected_image_path, password)
    
    tk.Button(password_window, text="Submit", command=submit_password).pack(pady=5)

def decrypt_message(image_path, password):
    img = cv2.imread(image_path)
    d = {i: chr(i) for i in range(255)}
    
    extracted_message = ""
    n, m, z = 0, 0, 0
    # print(len(extracted_message),'\n')
    for _ in range(100):  # Assuming max 100 character message
        extracted_message += d[img[n, m, z]]
        n = (n + 1) 
        m = (m + 1) 
        z = (z + 1) % 3

    # print(len(extracted_message),'\n')
    if extracted_message.startswith(password):
        decrypted_text = extracted_message[len(password):50]
        entry_decrypted.delete("1.0", tk.END)
        entry_decrypted.insert(tk.END, decrypted_text)
    else:
        messagebox.showerror("Error", "Incorrect password. Decryption failed.")
        entry_decrypted.delete("1.0", tk.END)  # Clear text box if wrong password

def load_preview(image_path, label):
    img = Image.open(image_path)
    img = img.resize((150, 150), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk

root = tk.Tk()
root.title("Image Steganography")
root.geometry("600x500")
root.config(bg="#001F3F")

# Title Label
tk.Label(root, text="Image Steganography", font=("Times New Roman", 24, "bold"), bg="#001F3F", fg="#FF6600").pack(pady=20)

frame = tk.Frame(root, padx=10, pady=10, bg="#001F3F")
frame.pack(pady=10)

tk.Label(frame, text="Select Image:", font=("Times New Roman", 12), bg="#001F3F", fg="white").grid(row=0, column=0, padx=5, pady=5)
entry_image_path = tk.Entry(frame, width=40)
entry_image_path.grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame, text="Browse", command=select_image, bg="#FF6600", font=("Times New Roman", 10), fg="white").grid(row=0, column=2, padx=5, pady=5)

tk.Label(frame, text="Select Output Folder:", font=("Times New Roman", 12), bg="#001F3F", fg="white").grid(row=1, column=0, padx=5, pady=5)
entry_output_folder = tk.Entry(frame, width=40)
entry_output_folder.grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame, text="Browse", command=select_output_folder, bg="#FF6600", font=("Times New Roman", 10), fg="white").grid(row=1, column=2, padx=5, pady=5)

tk.Label(frame, text="Enter Secret Message:", font=("Times New Roman", 12), bg="#001F3F", fg="white").grid(row=2, column=0, padx=5, pady=5)
entry_message = tk.Text(frame, height=3, width=30)
entry_message.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Password:", font=("Times New Roman", 12), bg="#001F3F", fg="white").grid(row=3, column=0, padx=5, pady=5)
entry_password = tk.Entry(frame, show="*", width=30)
entry_password.grid(row=3, column=1, padx=5, pady=5)

tk.Button(frame, text="Encrypt & Save", command=encrypt_message, bg="#FF6600", font=("Times New Roman", 10), fg="white").grid(row=4, column=1, pady=10)

label_image_preview = tk.Label(root, bg="#001F3F")
label_image_preview.pack()

label_encrypted_preview = tk.Label(root, bg="#001F3F")
label_encrypted_preview.pack()

tk.Label(root, text="Decrypted Message:", font=("Times New Roman", 12), bg="#001F3F", fg="white").pack()
entry_decrypted = tk.Text(root, height=3, width=50)
entry_decrypted.pack()

tk.Button(root, text="Decrypt Image", command=request_password, bg="#FF6600", font=("Times New Roman", 10), fg="white").pack(pady=10)

root.mainloop()
