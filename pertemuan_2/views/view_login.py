import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from controller.controller_auth import AuthController


class LoginView:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.auth = AuthController()

        self.root.title("Login - Sistem Absensi")
        
        # Center the window on screen
        self.root.update_idletasks()
        width = 400
        height = 420
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)  # Make login window fixed size for clean layout

        # Outer container with padding
        frame = ttk.Frame(self.root, padding=35)
        frame.pack(fill=BOTH, expand=True)

        # Header Icon & Title
        ttk.Label(frame, text="🔐", font=("Segoe UI", 36), anchor=CENTER).pack(pady=(0, 5))
        ttk.Label(frame, text="SISTEM ABSENSI", font=("Segoe UI", 18, "bold"),
                  bootstyle=INFO, anchor=CENTER).pack(pady=(0, 2))
        ttk.Label(frame, text="Silakan masuk untuk melanjutkan",
                  font=("Segoe UI", 10), bootstyle=SECONDARY, anchor=CENTER).pack(pady=(0, 25))

        # Username Input
        ttk.Label(frame, text="👤 Username", font=("Segoe UI", 10, "bold"),
                  bootstyle=LIGHT).pack(anchor=W, pady=(0, 5))
        self.entry_username = ttk.Entry(frame, font=("Segoe UI", 11))
        self.entry_username.pack(fill=X, pady=(0, 15))
        self.entry_username.focus()

        # Password Input
        ttk.Label(frame, text="🔒 Password", font=("Segoe UI", 10, "bold"),
                  bootstyle=LIGHT).pack(anchor=W, pady=(0, 5))
        self.entry_password = ttk.Entry(frame, show="*", font=("Segoe UI", 11))
        self.entry_password.pack(fill=X, pady=(0, 5))

        # Error Message Label
        self.label_error = ttk.Label(frame, text="", font=("Segoe UI", 9),
                                     bootstyle=DANGER)
        self.label_error.pack(pady=(0, 10))

        # Login Button
        self.btn_login = ttk.Button(frame, text="Masuk ➔", bootstyle=INFO,
                                    command=self._handle_login)
        self.btn_login.pack(fill=X, ipady=5)

        self.root.bind("<Return>", lambda e: self._handle_login())

    def _handle_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()
        result = self.auth.login(username, password)
        if result['success']:
            self.on_login_success(result['user'])
        else:
            self.label_error.config(text=result['message'])

