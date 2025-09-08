# ELEVATELABS-CYBERSECURITY-INTERNSHIP-FINAL-PROJECTS

-----------------------------------------------------------------------------------------------------------

🔐 Steganography Tool with Secure GUI
📌 Project Overview

This project is a GUI-based steganography tool that allows users to hide and extract secret files inside images. It enhances traditional steganography with password protection, OTP-based password recovery, and user-friendly GUI design.

Developed as part of the Cybersecurity Internship at Elevatte Labs, this project demonstrates the practical application of information hiding, cryptography, and secure authentication techniques in real-world scenarios.

🎯 Objectives

Implement secure file hiding using image steganography.

Provide an interactive GUI for ease of use.

Add password protection with validation rules.

Provide error handling for wrong passwords.

Implement Forgot Password feature with OTP via email.

Demonstrate cybersecurity best practices for safe data handling.
<img width="876" height="513" alt="image" src="https://github.com/user-attachments/assets/7621f00c-562b-43df-8b9a-5bc3cdd91a60" />

⚙️ Features

✅ Embed files into cover images (PNG, BMP supported).
✅ Extract hidden files from stego images.
✅ Password protection (minimum 6 characters).
✅ Wrong password detection with error message.
✅ Forgot password option with OTP verification via email.
✅ Interactive GUI built using Python tkinter.
✅ Modular code with stego_tool.py for core functions and gui_stego.py for GUI.

🖼️ GUI Demo

Main Window: Choose cover image, payload, and output file.

Embed Button: Hide payload securely.

Extract Button: Reveal hidden data.

Forgot Password: Request OTP → Reset password.

(Insert screenshots here after testing your app.)

🛠️ Tech Stack

Programming Language: Python 3.x

Libraries Used:

tkinter (GUI)

smtplib, email.message (OTP email service)

random (OTP generation)

os & filedialog (file handling)

📂 Project Structure
steganography-tool/
│── gui_stego.py        # GUI frontend (Tkinter)
│── stego_tool.py       # Core steganography functions
│── requirements.txt    # Dependencies
│── README.md           # Project report & documentation
│── /screenshots        # Screenshots of GUI (optional)

🚀 Installation & Usage
1️⃣ Clone Repository
git clone https://github.com/<your-username>/steganography-tool.git
cd steganography-tool

2️⃣ Install Requirements
pip install -r requirements.txt

3️⃣ Start Local SMTP Server (for OTP)
pip install aiosmtpd
python -m aiosmtpd -n -l localhost:1025

4️⃣ Run GUI
python gui_stego.py

🔑 Workflow
Embedding Process

Select cover image (PNG/BMP).

Select payload file (any format).

Set password (min 6 chars).

Tool generates stego image with hidden payload.

Extraction Process

Select stego image.

Enter password.

If correct → extract payload file.

If wrong → show Wrong Password message.

Forgot Password (OTP Recovery)

Click Forgot Password.

OTP sent to ilmanaaz3006@gmail.com
 (via localhost SMTP).

Enter OTP → reset password.

🔒 Security Highlights

Password-protected steganography to prevent unauthorized extraction.

OTP-based recovery mechanism ensures authentication.

Input validation prevents weak passwords.

Error handling for wrong attempts.

📚 Learning Outcomes

Practical understanding of steganography techniques.

Implementation of password authentication and recovery.

Designing a secure GUI for cybersecurity applications.

Knowledge of SMTP, OTP, and Python security libraries.

📅 Internship Information

Organization: Elevatte Labs

Domain: Cybersecurity Internship

Intern: Ilma Naaz

Project Title: Secure Steganography Tool with GUI and OTP Recovery

📌 Future Enhancements

AES-based payload encryption before embedding.

Support for JPEG images with DCT steganography.

Cloud-based OTP service instead of localhost SMTP.

Logging & monitoring of user attempts.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
_______________________________________________________________________________________REPORT FILE FOR FINAL PROJECT_____________________________________________________________________________________________________________________________
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🔐 Steganography Tool with Secure GUI and OTP Recovery
1. Introduction

In the modern digital era, data security is one of the most crucial challenges faced by individuals and organizations. Sensitive files such as documents, images, and confidential reports require strong protection mechanisms to prevent unauthorized access. One of the lesser-known but highly effective techniques for secure communication is steganography, the art of hiding data inside multimedia files in such a way that its very existence remains secret.

This project, developed as part of the Cybersecurity Internship at Elevatte Labs, focuses on implementing a GUI-based steganography tool with password protection and OTP-based password recovery. The project combines concepts of information hiding, authentication, and cryptography-inspired password mechanisms to provide a secure, user-friendly system for safeguarding sensitive information.

2. Objectives

The primary objectives of this project are:

To implement a graphical user interface (GUI) that makes steganography accessible to non-technical users.

To design a password-protected embedding and extraction system that prevents unauthorized access.

To ensure robust authentication by implementing a forgot password mechanism using OTP (One-Time Password) via email.

To demonstrate secure data handling practices suitable for real-world cybersecurity applications.

To fulfill the internship requirement by applying theoretical cybersecurity knowledge to a practical project.

3. Features Implemented
3.1 Steganography Functions

Hides arbitrary files (payload) inside cover images (PNG/BMP).

Allows extraction of payload from stego images using the correct password.

3.2 Security Enhancements

Password Protection: Minimum 6-character password required for embedding and extraction.

Wrong Password Handling: If an incorrect password is entered, the system displays a warning message and prevents extraction.

Forgot Password Mechanism: Sends an OTP to the registered email address (ilmanaaz3006@gmail.com) using a local SMTP server.

OTP Verification: Resets the password securely after successful OTP validation.

3.3 GUI Design

Developed using Python tkinter.

Clean and interactive layout with buttons for embedding, extracting, and password recovery.

File selection dialogs for cover image, payload, and output file.

Informative pop-up messages for success, error, and invalid inputs.

4. Technology Stack

Programming Language: Python 3.x

Libraries Used:

tkinter → GUI development

smtplib, email.message → OTP email delivery

random → OTP generation

os, filedialog → File handling

Core Implementation:

stego_tool.py: Core steganography logic

gui_stego.py: GUI and user interaction

5. Workflow
5.1 Embedding (Hiding Data)

User selects a cover image and a payload file.

The system prompts for a password (minimum 6 characters).

Payload is embedded into the cover image, producing a stego image.

Stego image is saved at the specified output path.

5.2 Extraction (Revealing Data)

User selects the stego image and enters a password.

If the password matches the one used during embedding, the payload is successfully extracted.

If the password is incorrect, the tool displays a Wrong Password error.

5.3 Forgot Password (OTP Recovery)

User clicks Forgot Password.

An OTP is generated and sent to the registered email (ilmanaaz3006@gmail.com) via a local SMTP server (localhost:1025).

User enters the OTP in the GUI.

On successful verification, the system allows the user to set a new password.

6. Security Considerations

This project integrates cybersecurity principles into steganography by:

Preventing unauthorized extraction through password authentication.

Enforcing password complexity by requiring a minimum length.

Adding an OTP-based recovery mechanism to simulate real-world multi-factor authentication.

Ensuring that passwords are not stored permanently (handled in memory only).

7. Learning Outcomes

Through this project, the following outcomes were achieved:

Practical implementation of steganography techniques in Python.

Enhanced understanding of secure authentication mechanisms.

Experience with GUI development for security tools.

Hands-on practice with SMTP servers and OTP-based verification.

Insight into combining cybersecurity concepts with real-world applications.

8. Future Enhancements

While the project meets its internship goals, there are several possible improvements for the future:

AES Encryption: Encrypt payload files before embedding for added security.

Support for JPEG images: Extend beyond PNG/BMP using DCT steganography.

Cloud-based OTP service: Replace localhost SMTP with Gmail API or Twilio SendGrid.

Logging and Monitoring: Track attempts and generate security reports.

Dark-Theme GUI: Improve user experience with modern interface design.

9. Conclusion

This project successfully demonstrates the integration of steganography with cybersecurity practices through a secure and interactive GUI-based tool. By incorporating password protection, OTP recovery, and error handling, the tool goes beyond basic steganography and highlights how secure design principles can be applied to data hiding techniques.

As part of the Elevatte Labs Cybersecurity Internship, this project not only provided valuable technical learning but also strengthened problem-solving, secure coding, and software design skills. The tool can serve as a foundation for more advanced security applications, contributing towards the development of safer digital communication methods.
