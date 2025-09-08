# gui_stego.py
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import stego_tool
import os
import random
import smtplib
from email.message import EmailMessage

# -------- GLOBAL (in-memory) password used for encryption ----------
CURRENT_PASSWORD = None

# -------- OTP related globals --------
OTP_STORE = None
OTP_EMAIL = "ilmanaaz3006@gmail.com"
SMTP_HOST = "localhost"
SMTP_PORT = 1025

# -------------------------------------------------------------------
def send_otp():
    """Generate and send OTP to OTP_EMAIL via localhost SMTP."""
    global OTP_STORE
    OTP_STORE = str(random.randint(100000, 999999))
    try:
        msg = EmailMessage()
        msg["Subject"] = "Your StegoTool OTP"
        msg["From"] = "server@localhost"
        msg["To"] = OTP_EMAIL
        msg.set_content(f"Your OTP is: {OTP_STORE}")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.send_message(msg)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send OTP:\n{e}")
        return False

def forgot_password():
    """Trigger OTP + ask user to enter code and new password."""
    if not send_otp():
        return
    otp = simpledialog.askstring(
        "OTP Verification",
        "An OTP has been sent to your email.\nEnter the OTP here:"
    )
    if not otp:
        return
    if otp.strip() != OTP_STORE:
        messagebox.showerror("Invalid OTP", "The OTP you entered is incorrect.")
        return
    # correct OTP
    new_pwd = simpledialog.askstring(
        "Reset Password",
        "Enter a new password (min 6 chars):",
        show="*"
    )
    if not new_pwd or len(new_pwd.strip()) < 6:
        messagebox.showerror(
            "Invalid",
            "Password must be at least 6 characters."
        )
        return
    # set password
    global CURRENT_PASSWORD
    CURRENT_PASSWORD = new_pwd.strip()
    messagebox.showinfo("Success", "Password has been reset successfully.")

# -------------------------------------------------------------------

root = tk.Tk()
root.title("Steganography Tool")

cover_var = tk.StringVar(value=os.path.join(os.getcwd(), "kali-linux.png"))
payload_var = tk.StringVar()
out_var = tk.StringVar(value=os.path.join(os.getcwd(), "stego_output.png"))

def choose_cover():
    p = filedialog.askopenfilename(
        filetypes=[("PNG/BMP", "*.png;*.bmp"), ("All","*.*")]
    )
    if p: cover_var.set(p)

def choose_payload():
    p = filedialog.askopenfilename()
    if p: payload_var.set(p)

def choose_out():
    p = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG","*.png"), ("BMP","*.bmp")]
    )
    if p: out_var.set(p)

# ---------------------------------------------------------------
def embed():
    global CURRENT_PASSWORD
    cover = cover_var.get()
    payload = payload_var.get()
    outpath = out_var.get()

    if not (cover and payload and outpath):
        messagebox.showerror("Missing", "Please select cover, payload & output.")
        return

    # Ask password (use existing if already set)
    if not CURRENT_PASSWORD:
        pwd = simpledialog.askstring(
            "Set Password",
            "Set a password (min 6 characters):",
            show="*"
        )
        if not pwd or len(pwd.strip()) < 6:
            messagebox.showerror("Invalid", "Password must be at least 6 characters.")
            return
        CURRENT_PASSWORD = pwd.strip()

    try:
        stego_tool.embed_file_cli(
            cover, outpath, payload, password=CURRENT_PASSWORD
        )
        messagebox.showinfo("Done", f"Stego image created:\n{outpath}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------------------------------------------------------
def extract():
    global CURRENT_PASSWORD
    stego = filedialog.askopenfilename(
        filetypes=[("PNG/BMP","*.png;*.bmp"),("All","*.*")]
    )
    if not stego:
        return
    outdir = filedialog.askdirectory()
    if not outdir:
        return

    # Ask password before extraction
    pwd = simpledialog.askstring(
        "Password Required",
        "Enter password:",
        show="*"
    )
    if not pwd or len(pwd.strip()) < 6:
        messagebox.showerror("Invalid", "Password must be at least 6 characters.")
        return

    # Validate
    if CURRENT_PASSWORD and pwd.strip() != CURRENT_PASSWORD:
        messagebox.showerror("Wrong Password", "The password is incorrect.")
        return

    try:
        out = stego_tool.extract_file_cli(
            stego, out_dir=outdir, password=pwd.strip()
        )
        messagebox.showinfo("Extracted", f"Payload saved to:\n{out}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------------------------------------------------------

# UI Layout
frame = tk.Frame(root, pady=10, padx=10)
frame.pack()

# Section: Cover
tk.Label(frame, text="Cover Image:", font=("Arial",12,"bold")).grid(row=0,column=0,sticky="w")
tk.Entry(frame, textvariable=cover_var, width=60).grid(row=0,column=1)
tk.Button(frame, text="Browse", command=choose_cover).grid(row=0,column=2,padx=4)

# Section: Payload
tk.Label(frame, text="Payload File:", font=("Arial",12,"bold")).grid(row=1,column=0,sticky="w")
tk.Entry(frame, textvariable=payload_var, width=60).grid(row=1,column=1)
tk.Button(frame, text="Browse", command=choose_payload).grid(row=1,column=2,padx=4)

# Section: Output
tk.Label(frame, text="Output Stego Image:", font=("Arial",12,"bold")).grid(row=2,column=0,sticky="w")
tk.Entry(frame, textvariable=out_var, width=60).grid(row=2,column=1)
tk.Button(frame, text="Save As", command=choose_out).grid(row=2,column=2,padx=4)

# Buttons
btn_frame = tk.Frame(frame,pady=10)
btn_frame.grid(row=3,column=1)

tk.Button(btn_frame, text="Embed (Hide)", width=15, command=embed).grid(row=0,column=0,padx=5)
tk.Button(btn_frame, text="Extract (Unhide)", width=15, command=extract).grid(row=0,column=1,padx=5)
tk.Button(frame, text="Forgot Password", fg="blue", command=forgot_password).grid(row=4,column=1,pady=5,sticky="e")

root.mainloop()
