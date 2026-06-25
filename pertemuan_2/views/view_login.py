import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from controller.controller_auth import AuthController


class LoginView:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.auth = AuthController()

        self.root.title("Login - Sistem Absensi")
        self.root.geometry("400x350")

        frame = ttk.Frame(self.root, padding=30)
        frame.pack(fill=BOTH, expand=True)

        ttk.Label(frame, text="SISTEM ABSENSI", font=("Helvetica", 18, "bold"),
                  bootstyle=INFO).pack(pady=(0, 5))
        ttk.Label(frame, text="Silakan login untuk melanjutkan",
                  font=("Helvetica", 10), bootstyle=SECONDARY).pack(pady=(0, 20))

        ttk.Label(frame, text="Username", font=("Helvetica", 10),
                  bootstyle=LIGHT).pack(anchor=W)
        self.entry_username = ttk.Entry(frame, font=("Helvetica", 11))
        self.entry_username.pack(fill=X, pady=(0, 10))
        self.entry_username.focus()

        ttk.Label(frame, text="Password", font=("Helvetica", 10),
                  bootstyle=LIGHT).pack(anchor=W)
        self.entry_password = ttk.Entry(frame, show="*", font=("Helvetica", 11))
        self.entry_password.pack(fill=X, pady=(0, 5))

        self.label_error = ttk.Label(frame, text="", font=("Helvetica", 9),
                                     bootstyle=DANGER)
        self.label_error.pack(pady=(0, 5))

        self.btn_login = ttk.Button(frame, text="Login", bootstyle=INFO,
                                    command=self._handle_login)
        self.btn_login.pack(fill=X, pady=(10, 0))

        self.root.bind("<Return>", lambda e: self._handle_login())

    def _handle_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()
        result = self.auth.login(username, password)
        if result['success']:
            self.on_login_success(result['user'])
        else:
            self.label_error.config(text=result['message'])
