#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatic Mail Responder - Secure Email Automation System
Copyright (c) 2025 Apiwish Anutarvanichkul. All rights reserved.

This software is licensed under the Apache License 2.0.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author: Apiwish Anutarvanichkul
Email: apiwish.boon@gmail.com
Version: 3.0.2
"""

import imaplib
import smtplib
import email
import email.utils
import tkinter as tk
from tkinter import ttk, messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import re
import webbrowser

# Global credentials (set after login)
EMAIL_ADDRESS = None
EMAIL_PASSWORD = None

# --- Greeting Templates with HTML ---
GREETING_TEMPLATES = {
    "Friendly 🌈": """Hi {name}! 🎉<br>
Just wanted to drop in and say hello! Hope you're having an amazing day.<br><br>

""",

    "Professional 📄": """Greetings {name},<br>
Thank you for contacting us. We appreciate your time.<br><br>

""",

    "Tech Nerd 🤖": """[SYSTEM ONLINE] Greetings, {name} 🤖<br>
<code>$ ssh connection@established</code><br>
Quantum entanglement confirmed. Handshake protocol: SUCCESS ✓<br>
All systems nominal. Ready for data exchange...<br><br>

""",

    "Marketing ✨": """Hey {name}! ✨<br>
We've got exciting updates just for you!<br><br>

""",

    "Casual ☕": """What's up {name}? ☕<br>
Just checking in! Hope everything's going well on your end.<br><br>

""",

    "Formal Business 💼": """Dear {name},<br>
I hope this message finds you well. I am writing to extend my professional greetings.<br><br>

""",

    "Enthusiastic 🚀": """HELLO {name}!! 🚀<br>
Super excited to connect with you! Let's make something awesome happen!<br><br>

""",

    "Minimalist 📝": """Hi {name},<br>
Thanks for reaching out.<br><br>

""",

    "Creative Writer 📚": """Dear {name},<br>
As the ink flows upon this digital parchment, I extend warm greetings to you on this fine day.<br><br>

""",

    "Seasonal - Winter ❄️": """Hello {name}! ❄️<br>
Wishing you a cozy and wonderful winter day! Stay warm!<br><br>

""",

    "Seasonal - Summer ☀️": """Hey {name}! ☀️<br>
Hope you're enjoying the sunshine! Sending bright summer vibes your way!<br><br>

""",

    "Motivational 💪": """Hey {name}! 💪<br>
You're doing amazing! Keep up the great work and remember - you've got this!<br><br>

""",

    "Funny 😄": """Yo {name}! 😄<br>
*Dramatically enters inbox* Hello there! Just sliding into your emails like a pro.<br><br>

""",

    "Wellness 🧘": """Namaste {name}, 🧘<br>
Sending you peaceful vibes and positive energy. Hope you're taking care of yourself today!<br><br>

""",

    "Gamer 🎮": """Hey {name}! 🎮<br>
Player 1 has entered the chat! Ready to level up our conversation?<br><br>

""",

    "Foodie 🍕": """Hi {name}! 🍕<br>
Hope you're having a delicious day! Just wanted to say hello (and maybe grab coffee sometime?)<br><br>

""",

    "Academic 🎓": """Dear {name}, 🎓<br>
I hope this correspondence finds you in good academic standing. Best regards from our institution.<br><br>

""",

    "Party Mode 🎊": """HEYYY {name}!!! 🎊🎉🥳<br>
Let's celebrate! Just wanted to send some party vibes your way!<br><br>

""",

    "Mysterious 🌙": """Greetings {name}... 🌙<br>
The stars have aligned for this message to reach you. What secrets shall we discuss?<br><br>

""",

    "Nostalgic 📼": """Hey {name}! 📼<br>
Remember the good old days? Just wanted to reconnect and say hi!<br><br>

""",

    "Sci-Fi Commander 🛸": """Commander {name}, 🛸<br>
<strong>[INCOMING TRANSMISSION]</strong><br>
This is Starship Alpha-7. We've detected your signal. Requesting permission to engage communications. Over.<br><br>

""",

    "Cyberpunk Hacker 💻": """&gt;&gt; ACCESS GRANTED: {name} 💻<br>
<code>root@mainframe:~# echo "Hello from the grid"</code><br>
Firewall bypassed. Connection encrypted. Your data is safe with me, choom. 🔐<br><br>

""",

    "AI Assistant 🤖": """[AI] Hello {name}! 🤖<br>
<em>*beep boop*</em> Human detected! My neural networks are pleased to make your acquaintance.<br>
Friendship algorithm: ACTIVATED ✓<br><br>

""",

    "Time Traveler ⏰": """Greetings {name} from [REDACTED], ⏰<br>
The temporal coordinates aligned perfectly for this message. According to my calculations, now is the perfect time to say hello across the space-time continuum!<br><br>

""",

    "Matrix Style 🕶️": """Wake up, {name}... 🕶️<br>
<code style="color:#00ff00;">The Matrix has you...</code><br>
Just kidding! But seriously, I'm reaching out to connect. Red pill or blue pill? 💊<br><br>

""",

    "Space Explorer 🌌": """Captain {name}, 🌌<br>
Mission Control here. We've successfully established contact from Earth. The cosmos is vast, but our connection transcends light-years. Safe travels, explorer!<br><br>

""",

    "Robot Engineer 🔧": """[BEEP BOOP] Hello {name}! 🔧<br>
Running diagnostics... Friendliness module: 100% ✓<br>
Humor subroutine: ONLINE ✓<br>
Excitement level: MAXIMUM ✓<br>
All systems ready for interaction!<br><br>

"""
}

AUTO_REPLY_HTML = """\
<!DOCTYPE html>
<html>
  <body style="margin:0; padding:0; 
               background: linear-gradient(to bottom right, #ffc0cb, #add8e6); 
               font-family:Inter, Arial, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:80px;">
      <tr>
        <td align="center">
          <table width="90%" cellpadding="20" cellspacing="0"
                 style="max-width:500px; 
                        background:rgba(255,255,255,0.95); 
                        border-radius:15px;
                        box-shadow: 0 0 20px rgba(255, 192, 203, 0.6), 
                                    0 0 40px rgba(173, 216, 230, 0.5);">
            <tr>
              <td style="font-size:16px; color:#333;">
                Hi there! 👋<br><br>
                Thank you so much for reaching out. This is an automatic reply just to let you know that I received your email.<br><br>
                I'm currently unavailable and may not be able to respond immediately. However, I will make sure to read your message and get back to you as soon as I'm back online.<br><br>
                📞 If urgent, please call: <strong>000-000-0000</strong><br><br>
                While you wait for my reply, check out my projects! 🌟<br>
                <a href="https://notarickroll.page.gd/" target="_blank">Not a Rickroll</a><br>
                <a href="https://boon123.pythonanywhere.com/" target="_blank">My PythonAnywhere Projects</a><br><br>
                Best regards,<br><br>
                <hr style="margin:20px 0; border:1px solid #ddd;">
                <p style="font-size:12px; color:gray; line-height:1.5;">
                  Please note that this is an automated message sent from the system administrator 
                  (<a href='mailto:example@gmail.com'>example@gmail.com</a>).<br>
                  No further action is required.
                </p>
              </td>
            </tr>
          </table>
          <p style="font-size:13px; color:#999; margin-top:40px;">
            © 2025 APIWISH ANUTARAVANICHKUL. All rights reserved.<br>
          </p>
        </td>
      </tr>
    </table>
  </body>
</html>
"""

# Track replied emails to avoid duplicates
replied_to = set()

# Auto-responder state
is_running = False
check_interval_ms = 60000  # 60 seconds

# --- Login Dialog ---
class LoginDialog:
    def __init__(self, parent):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("🔐 Login to Email Account")
        self.dialog.geometry("450x450")
        self.dialog.configure(bg="#1e1e1e")
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Title
        tk.Label(
            self.dialog, 
            text="Email Account Login", 
            font=("Arial", 18, "bold"), 
            bg="#1e1e1e", 
            fg="#1abc9c"
        ).pack(pady=20)
        
        # Frame for inputs
        input_frame = tk.Frame(self.dialog, bg="#1e1e1e")
        input_frame.pack(pady=10, padx=40, fill="x")
        
        # Email input
        tk.Label(
            input_frame, 
            text="Email Address:", 
            font=("Arial", 11), 
            bg="#1e1e1e", 
            fg="#fff"
        ).grid(row=0, column=0, sticky="w", pady=5)
        
        self.email_entry = tk.Entry(
            input_frame, 
            width=35, 
            bg="#2c2c2c", 
            fg="#fff", 
            insertbackground="#fff",
            font=("Arial", 10)
        )
        self.email_entry.grid(row=1, column=0, pady=5)
        self.email_entry.focus()
        
        # Password input
        tk.Label(
            input_frame, 
            text="App Password:", 
            font=("Arial", 11), 
            bg="#1e1e1e", 
            fg="#fff"
        ).grid(row=2, column=0, sticky="w", pady=5)
        
        self.password_entry = tk.Entry(
            input_frame, 
            width=35, 
            bg="#2c2c2c", 
            fg="#fff", 
            insertbackground="#fff",
            show="●",
            font=("Arial", 10)
        )
        self.password_entry.grid(row=3, column=0, pady=5)
        
        # Show/Hide password
        self.show_password_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            input_frame,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password,
            bg="#1e1e1e",
            fg="#aaa",
            selectcolor="#2c2c2c",
            activebackground="#1e1e1e",
            activeforeground="#fff"
        ).grid(row=4, column=0, sticky="w", pady=2)
        
        # Info label with hyperlink
        info_frame = tk.Frame(self.dialog, bg="#1e1e1e")
        info_frame.pack(pady=5)
        
        tk.Label(
            info_frame,
            text="💡 Use Gmail App Password, not your regular password",
            font=("Arial", 9),
            bg="#1e1e1e",
            fg="#f39c12"
        ).pack()
        
        # Clickable link for app password help
        help_link = tk.Label(
            info_frame,
            text="Don't have an App Password? Click here for instructions",
            font=("Arial", 8, "underline"),
            bg="#1e1e1e",
            fg="#3498db",
            cursor="hand2"
        )
        help_link.pack(pady=3)
        help_link.bind("<Button-1>", lambda e: self.open_app_password_help())
        
        # Buttons
        button_frame = tk.Frame(self.dialog, bg="#1e1e1e", bd=2)
        button_frame.pack(pady=15)
        
        tk.Button(
            button_frame,
            text="Login",
            command=self.on_login,
            bg="#1abc9c",
            fg="#000000",
            font=("Arial", 11, "bold"),
            width=12,
            cursor="hand2",
            relief="raised",
            bd=3
        ).grid(row=0, column=0, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=self.on_cancel,
            bg="#e74c3c",
            fg="#000000",
            font=("Arial", 11, "bold"),
            width=12,
            cursor="hand2",
            relief="raised",
            bd=3
        ).grid(row=0, column=1, padx=5)
        
        # Bind Enter key
        self.dialog.bind("<Return>", lambda e: self.on_login())
        self.dialog.bind("<Escape>", lambda e: self.on_cancel())
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
    
    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="●")
    
    def open_app_password_help(self):
        """Open Google's App Password help page in default browser"""
        webbrowser.open("https://funny-cartoon.my.canva.site/app-pasword-help")
    
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def on_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password!")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address!")
            return
        
        # Test credentials
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as smtp:
                smtp.login(email, password)
            
            self.result = (email, password)
            self.dialog.destroy()
        except smtplib.SMTPAuthenticationError:
            messagebox.showerror(
                "Authentication Failed", 
                "Invalid email or password!\n\nMake sure you're using a Gmail App Password."
            )
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server:\n{str(e)}")
    
    def on_cancel(self):
        self.dialog.destroy()
    
    def show(self):
        self.dialog.wait_window()
        return self.result

# --- Main Application ---
class AutoMailResponder:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Mail Center – Dark Mode V.3.0.2")
        self.root.geometry("750x850")
        self.root.configure(bg="#121212")
        
        # Show login dialog
        credentials = LoginDialog(root).show()
        
        if not credentials:
            messagebox.showwarning("Login Required", "You must login to use this application.")
            root.destroy()
            return
        
        global EMAIL_ADDRESS, EMAIL_PASSWORD
        EMAIL_ADDRESS, EMAIL_PASSWORD = credentials
        
        self.build_ui()
        
    def build_ui(self):
        # Header with logged in user
        header_frame = tk.Frame(self.root, bg="#1e1e1e", height=60)
        header_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            header_frame,
            text=f"🔐 Logged in as: {EMAIL_ADDRESS}",
            font=("Arial", 11),
            bg="#1e1e1e",
            fg="#1abc9c"
        ).pack(side="left", padx=20, pady=15)
        
        tk.Button(
            header_frame,
            text="Logout",
            command=self.logout,
            bg="#e74c3c",
            fg="#000000",
            font=("Arial", 9, "bold"),
            cursor="hand2",
            relief="raised",
            bd=2
        ).pack(side="right", padx=20, pady=15)
        
        # Auto-responder controls
        control_frame = tk.Frame(self.root, bg="#121212")
        control_frame.pack(pady=10)
        
        self.status_label = tk.Label(
            control_frame,
            text="⏸ Auto-Responder: STOPPED",
            font=("Arial", 14, "bold"),
            bg="#121212",
            fg="#e74c3c"
        )
        self.status_label.pack()
        
        self.toggle_btn = tk.Button(
            control_frame,
            text="▶ Start Auto-Responder",
            command=self.toggle_auto_responder,
            bg="#27ae60",
            fg="#000000",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            width=25,
            relief="raised",
            bd=3
        )
        self.toggle_btn.pack(pady=10)
        
        # Latest Email Replied
        tk.Label(
            self.root,
            text="Latest Email Replied:",
            font=("Arial", 12),
            bg="#121212",
            fg="#fff"
        ).pack()
        
        self.latest_email_var = tk.StringVar(value="No replies yet")
        tk.Label(
            self.root,
            textvariable=self.latest_email_var,
            font=("Arial", 14, "bold"),
            fg="#1abc9c",
            bg="#121212"
        ).pack()
        
        # Log box
        tk.Label(
            self.root,
            text="System Log:",
            font=("Arial", 12),
            bg="#121212",
            fg="#fff"
        ).pack(pady=5)
        
        self.log_box = tk.Text(
            self.root,
            height=10,
            width=90,
            bg="#1e1e1e",
            fg="#eee",
            insertbackground="#fff"
        )
        self.log_box.pack(padx=10, pady=5)
        
        # Greeting section
        tk.Label(
            self.root,
            text="Send Greeting Email",
            font=("Arial", 16, "bold"),
            bg="#121212",
            fg="#fff"
        ).pack(pady=15)
        
        # Recipient Name
        tk.Label(
            self.root,
            text="Recipient Name:",
            font=("Arial", 11),
            bg="#121212",
            fg="#fff"
        ).pack()
        
        self.recipient_name_input = tk.Entry(
            self.root,
            width=50,
            bg="#1e1e1e",
            fg="#fff",
            insertbackground="#fff"
        )
        self.recipient_name_input.pack(pady=5)
        
        # Recipient Email
        tk.Label(
            self.root,
            text="Recipient Email:",
            font=("Arial", 11),
            bg="#121212",
            fg="#fff"
        ).pack()
        
        self.greeting_email_input = tk.Entry(
            self.root,
            width=50,
            bg="#1e1e1e",
            fg="#fff",
            insertbackground="#fff"
        )
        self.greeting_email_input.pack(pady=5)
        
        # Template Selector
        tk.Label(
            self.root,
            text="Select Template:",
            font=("Arial", 11),
            bg="#121212",
            fg="#fff"
        ).pack()
        
        self.greeting_template_var = tk.StringVar(value=list(GREETING_TEMPLATES.keys())[0])
        ttk.Combobox(
            self.root,
            textvariable=self.greeting_template_var,
            values=list(GREETING_TEMPLATES.keys()),
            width=48
        ).pack(pady=5)
        
        # Preview
        tk.Label(
            self.root,
            text="Preview:",
            font=("Arial", 11),
            bg="#121212",
            fg="#fff"
        ).pack()
        
        self.preview_box = tk.Text(
            self.root,
            height=6,
            width=90,
            bg="#2c2c2c",
            fg="#fff",
            insertbackground="#fff"
        )
        self.preview_box.pack(padx=10, pady=5)
        self.preview_box.config(state='disabled')
        
        # Send Button
        tk.Button(
            self.root,
            text="📧 Send Greeting Email",
            command=self.send_greeting,
            bg="#1abc9c",
            fg="#000000",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            relief="raised",
            bd=3
        ).pack(pady=10)
        
        # Bind preview update
        self.recipient_name_input.bind("<KeyRelease>", self.update_preview)
        self.greeting_template_var.trace_add("write", self.update_preview)
        
        # Initialize preview
        self.update_preview()
        
        # Initial log
        self.push_log("✓ Login successful")
        self.push_log("Ready to use. Start auto-responder when ready.")
    
    def push_log(self, text):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_box.insert(tk.END, f"{timestamp} | {text}\n")
        self.log_box.see(tk.END)
    
    def toggle_auto_responder(self):
        global is_running
        is_running = not is_running
        
        if is_running:
            self.status_label.config(text="▶ Auto-Responder: RUNNING", fg="#27ae60")
            self.toggle_btn.config(text="⏸ Stop Auto-Responder", bg="#e74c3c", fg="#000000")
            self.push_log("▶ Auto-responder started")
            self.schedule_check()
        else:
            self.status_label.config(text="⏸ Auto-Responder: STOPPED", fg="#e74c3c")
            self.toggle_btn.config(text="▶ Start Auto-Responder", bg="#27ae60", fg="#000000")
            self.push_log("⏸ Auto-responder stopped")
    
    def schedule_check(self):
        if is_running:
            self.push_log("🔍 Checking inbox…")
            self.check_inbox()
            self.root.after(check_interval_ms, self.schedule_check)
    
    def check_inbox(self):
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com", timeout=10)
            mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            mail.select("inbox")
            status, data = mail.search(None, "UNSEEN")
            
            if status != 'OK':
                self.push_log(f"⚠ IMAP search failed: {status}")
                mail.logout()
                return
            
            id_list = data[0].split()
            if not id_list:
                self.push_log("📭 No new messages")
                mail.logout()
                return
            
            for eid in id_list:
                try:
                    status, msg_data = mail.fetch(eid, "(RFC822)")
                    if status != 'OK':
                        self.push_log(f"⚠ Failed to fetch id {eid}")
                        continue
                    
                    raw_msg = email.message_from_bytes(msg_data[0][1])
                    sender_hdr = raw_msg.get("From", "")
                    sender_email = email.utils.parseaddr(sender_hdr)[1]
                    
                    if sender_email:
                        self.send_auto_reply(sender_email)
                    else:
                        self.push_log(f"⚠ Could not parse sender from: {sender_hdr}")
                    
                    mail.store(eid, '+FLAGS', '\\Seen')
                except Exception as e:
                    self.push_log(f"⚠ Error processing message: {e}")
            
            mail.close()
            mail.logout()
        except Exception as e:
            self.push_log(f"❌ Inbox error: {e}")
    
    def send_auto_reply(self, to_address):
        global replied_to
        
        if to_address in replied_to:
            self.push_log(f"⏭ Already replied to {to_address}")
            return
        
        msg = MIMEMultipart("alternative")
        msg['Subject'] = "Auto Reply"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_address
        
        plain_text = ("Hi,\n\nThanks for your message – this is an automated reply "
                     "to confirm we've received it.\n\nBest,\nA.Apiwish")
        
        msg.attach(MIMEText(plain_text, "plain"))
        msg.attach(MIMEText(AUTO_REPLY_HTML, "html"))
        
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            
            replied_to.add(to_address)
            self.latest_email_var.set(to_address)
            self.push_log(f"✓ Auto-reply sent to {to_address}")
        except Exception as e:
            self.push_log(f"❌ ERROR auto-reply to {to_address}: {e}")
    
    def send_greeting(self):
        to_addr = self.greeting_email_input.get().strip()
        if not to_addr:
            messagebox.showerror("Error", "Please enter recipient email!")
            return
        
        recipient_name = self.recipient_name_input.get().strip() or "there"
        template_name = self.greeting_template_var.get()
        html_content = GREETING_TEMPLATES[template_name].format(name=recipient_name)
        plain_content = re.sub(r'<[^>]+>', '', html_content.replace("<br>", "\n"))
        
        msg = MIMEMultipart("alternative")
        msg['Subject'] = "Greeting from A.Apiwish"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_addr
        
        msg.attach(MIMEText(plain_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))
        
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            self.push_log(f"✓ Greeting sent to {to_addr} ({recipient_name})")
            messagebox.showinfo("Success", f"Greeting email sent to {to_addr}!")
        except Exception as e:
            self.push_log(f"❌ ERROR sending greeting: {e}")
            messagebox.showerror("Error", f"Failed to send email:\n{str(e)}")
    
    def update_preview(self, *args):
        recipient_name = self.recipient_name_input.get() or "there"
        template_name = self.greeting_template_var.get()
        preview_content = GREETING_TEMPLATES[template_name].format(name=recipient_name)
        
        self.preview_box.config(state='normal')
        self.preview_box.delete('1.0', tk.END)
        self.preview_box.insert(tk.END, preview_content)
        self.preview_box.config(state='disabled')
    
    def logout(self):
        global is_running
        if is_running:
            if not messagebox.askyesno("Confirm Logout", "Auto-responder is still running. Logout anyway?"):
                return
        
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()

# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AutoMailResponder(root)
    root.mainloop()