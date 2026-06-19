import tkinter as tk
from tkinter import messagebox

class DashboardAkademik(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # ==================== KONFIGURASI UTAMA ====================
        self.title("SIAKAD - Dashboard Profil Mahasiswa")
        self.geometry("920x540")
        self.configure(bg="#F1F5F9")
        self.resizable(False, False)
        
        # Otomatis membuat window muncul di tengah layar
        self.center_window()
        
        # Data Mock Aplikasi
        self.biodata = {
            "Nama Lengkap": "Ramadhan Anton Pratama",
            "NIM": "23250017",
            "Program Studi": "Sistem Informasi",
            "Alamat": "Tangerang Selatan, Banten",
            "Email": "ramadhananton@example.com"
        }
        
        self.icons = {
            "Nama Lengkap": "👤 ", "NIM": "🆔 ", "Program Studi": "🎓 ", 
            "Alamat": "📍 ", "Email": "✉️ "
        }
        
        # Inisialisasi Pembentukan Komponen UI
        self.create_sidebar()
        self.create_main_content()

    def center_window(self):
        """Menghitung koordinat layar agar window muncul di tengah secara presisi."""
        self.update_idletasks()
        width = 920
        height = 540
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    # ==================== SIDEBAR COMPONENT ====================
    def create_sidebar(self):
        sidebar = tk.Frame(self, bg="#0F172A", width=240)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Avatar Canvas
        avatar = tk.Canvas(sidebar, width=90, height=90, bg="#0F172A", bd=0, highlightthickness=0)
        avatar.pack(pady=(50, 15))
        avatar.create_oval(5, 5, 85, 85, fill="#1E293B", outline="#38BDF8", width=2)
        avatar.create_text(45, 45, text="RA", fill="#38BDF8", font=("Segoe UI", 22, "bold"))

        # Nama & Status
        tk.Label(sidebar, text="Ramadhan A. P.", font=("Segoe UI", 12, "bold"), fg="#F8FAFC", bg="#0F172A").pack()
        
        status_badge = tk.Label(
            sidebar, text="● MAHASISWA AKTIF", font=("Segoe UI", 8, "bold"),
            fg="#38BDF8", bg="#1E293B", padx=12, pady=5
        )
        status_badge.pack(pady=(10, 0))

        # Footer Aplikasi
        tk.Label(sidebar, text="SIAKAD v2.6.0 © 2026", font=("Segoe UI", 8), fg="#64748B", bg="#0F172A").pack(side="bottom", pady=20)

    # ==================== MAIN WORKSPACE ====================
    def create_main_content(self):
        self.main_content = tk.Frame(self, bg="#F1F5F9", padx=30, pady=25)
        self.main_content.pack(side="right", fill="both", expand=True)

        self.draw_header()
        self.draw_stats()
        self.draw_bottom_sections()

    def draw_header(self):
        header_frame = tk.Frame(self.main_content, bg="#F1F5F9")
        header_frame.pack(fill="x", pady=(0, 20))

        tk.Label(header_frame, text="Dashboard Akademik", font=("Segoe UI", 18, "bold"), fg="#0F172A", bg="#F1F5F9").pack(anchor="w")
        tk.Label(header_frame, text="Selamat datang kembali di portal informasi akademik Anda.", font=("Segoe UI", 9), fg="#64748B", bg="#F1F5F9").pack(anchor="w", pady=(2, 0))

    def draw_stats(self):
        stats_container = tk.Frame(self.main_content, bg="#F1F5F9")
        stats_container.pack(fill="x", pady=(0, 20))

        stats_data = [
            ("Indeks Prestasi Kumulatif", "3.85", "📈"),
            ("Semester Berjalan", "06", "📅"),
            ("Total SKS Diambil", "114 SKS", "📝")
        ]

        for title, val, ico in stats_data:
            card_stat = tk.Frame(stats_container, bg="#FFFFFF", highlightbackground="#E2E8F0", highlightthickness=1)
            card_stat.pack(side="left", fill="both", expand=True, padx=(0, 15))
            
            # Accent bar
            tk.Frame(card_stat, bg="#2563EB", width=4).pack(side="left", fill="y")
            
            stat_inner = tk.Frame(card_stat, bg="#FFFFFF", padx=15, pady=12)
            stat_inner.pack(side="left", fill="both", expand=True)
            
            tk.Label(stat_inner, text=title, font=("Segoe UI", 8, "bold"), fg="#64748B", bg="#FFFFFF").pack(anchor="w")
            tk.Label(stat_inner, text=f"{ico} {val}", font=("Segoe UI", 14, "bold"), fg="#0F172A", bg="#FFFFFF").pack(anchor="w", pady=(4, 0))

    def draw_bottom_sections(self):
        """Membagi area bawah menjadi tata letak 2 kolom (Biodata & Pengumuman)."""
        bottom_container = tk.Frame(self.main_content, bg="#F1F5F9")
        bottom_container.pack(fill="both", expand=True)

        # --- KOLOM KIRI: CARD BIODATA (65% Width) ---
        info_card = tk.Frame(bottom_container, bg="#FFFFFF", highlightbackground="#E2E8F0", highlightthickness=1, padx=20, pady=20)
        info_card.pack(side="left", fill="both", expand=True, padx=(0, 15))

        tk.Label(info_card, text="Informasi Detail Mahasiswa", font=("Segoe UI", 11, "bold"), fg="#0F172A", bg="#FFFFFF").pack(anchor="w", pady=(0, 10))

        grid_frame = tk.Frame(info_card, bg="#FFFFFF")
        grid_frame.pack(fill="x", anchor="w")

        for i, (key, value) in enumerate(self.biodata.items()):
            tk.Label(grid_frame, text=f"{self.icons[key]}{key}", font=("Segoe UI", 9, "bold"), fg="#64748B", bg="#FFFFFF").grid(row=i, column=0, sticky="w", pady=6)
            tk.Label(grid_frame, text=":", font=("Segoe UI", 9), fg="#CBD5E1", bg="#FFFFFF").grid(row=i, column=1, sticky="w", padx=10, pady=6)
            tk.Label(grid_frame, text=value, font=("Segoe UI", 9), fg="#334155", bg="#FFFFFF").grid(row=i, column=2, sticky="w", pady=6)

        # Tombol Salin
        self.btn_salin = tk.Button(
            info_card, text="✨ Salin Profil", font=("Segoe UI", 8, "bold"),
            bg="#2563EB", fg="white", bd=0, cursor="hand2", padx=12, pady=6,
            command=self.salin_data
        )
        self.btn_salin.pack(side="bottom", anchor="e", pady=(10, 0))
        self.btn_salin.bind("<Enter>", lambda e: self.btn_salin.config(bg="#1D4ED8"))
        self.btn_salin.bind("<Leave>", lambda e: self.btn_salin.config(bg="#2563EB"))


        # --- KOLOM KANAN: CARD JADWAL & PENGUMUMAN (35% Width) ---
        side_card = tk.Frame(bottom_container, bg="#FFFFFF", highlightbackground="#E2E8F0", highlightthickness=1, padx=20, pady=20, width=260)
        side_card.pack(side="right", fill="both")
        side_card.pack_propagate(False)

        tk.Label(side_card, text="🔔 info & Pengumuman", font=("Segoe UI", 11, "bold"), fg="#0F172A", bg="#FFFFFF").pack(anchor="w", pady=(0, 12))

        announcements = [
            ("KRS Semester Genap", "⚠️ Batas akhir 30 Juni 2026"),
            ("Ujian Akhir Semester", "📅 Pelaksanaan Berita Acara"),
            ("Bimbingan Tugas Akhir", "📝 Sesi sinkronisasi berkas")
        ]

        for topic, desc in announcements:
            item_frame = tk.Frame(side_card, bg="#F8FAFC", padx=8, pady=6, highlightbackground="#F1F5F9", highlightthickness=1)
            item_frame.pack(fill="x", pady=4)
            tk.Label(item_frame, text=topic, font=("Segoe UI", 9, "bold"), fg="#334155", bg="#F8FAFC").pack(anchor="w")
            tk.Label(item_frame, text=desc, font=("Segoe UI", 8), fg="#64748B", bg="#F8FAFC").pack(anchor="w", pady=(2, 0))

    # ==================== LOGIC ACTIONS ====================
    def salin_data(self):
        text_data = (
            f"Nama Lengkap: {self.biodata['Nama Lengkap']}\n"
            f"NIM: {self.biodata['NIM']}\n"
            f"Program Studi: {self.biodata['Program Studi']}\n"
            f"Alamat: {self.biodata['Alamat']}\n"
            f"Email: {self.biodata['Email']}\n"
            f"--- Akumulasi ---\n"
            f"IPK: 3.85 | Semester: 6"
        )
        self.clipboard_clear()
        self.clipboard_append(text_data)
        messagebox.showinfo("Sistem Informasi", "Profil akademik berhasil disalin ke clipboard!")

if __name__ == "__main__":
    app = DashboardAkademik()
    app.mainloop()