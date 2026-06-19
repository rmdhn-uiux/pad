import tkinter as tk
from tkinter import messagebox

# ==================== FUNGSI & LOGIKA ====================

def salin_data():
    """Fungsi interaktif untuk menyalin data akademik ke clipboard."""
    text_data = (
        f"Nama Lengkap: {biodata['Nama Lengkap']}\n"
        f"NIM: {biodata['NIM']}\n"
        f"Program Studi: {biodata['Program Studi']}\n"
        f"Alamat: {biodata['Alamat']}\n"
        f"Email: {biodata['Email']}\n"
        f"--- Statistik ---\n"
        f"IPK: 3.85 | Semester: 6 | SKS Kumulatif: 114"
    )
    root.clipboard_clear()
    root.clipboard_append(text_data)
    
    # Kustomisasi dialog sukses agar terlihat profesional
    messagebox.showinfo("Sistem Informasi", "Profil akademik berhasil disalin ke clipboard!")

# ==================== STRUKTUR UTAMA WINDOW ====================

root = tk.Tk()
root.title("SIAKAD - Dashboard Profil Mahasiswa")
root.geometry("880x520")
root.configure(bg="#F1F5F9")  # Background utama Slate 100
root.resizable(False, False)   # Mengunci ukuran window agar layout presisi

# Data Pasangan Key, Value, dan Ikon untuk Biodata Utama
biodata = {
    "Nama Lengkap": "Ramadhan Anton Pratama",
    "NIM": "23250017",
    "Program Studi": "Sistem Informasi",
    "Alamat": "Tangerang Selatan, Banten",
    "Email": "ramadhananton@example.com"
}

icons = {
    "Nama Lengkap": "👤 ",
    "NIM": "🆔 ",
    "Program Studi": "🎓 ",
    "Alamat": "📍 ",
    "Email": "✉️ "
}

# ==================== SIDEBAR KIRI (PROFILE SUMMARY) ====================

sidebar = tk.Frame(root, bg="#0F172A", width=240)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

# Avatar Lingkaran Elegan (Menggunakan Canvas)
avatar_canvas = tk.Canvas(sidebar, width=90, height=90, bg="#0F172A", bd=0, highlightthickness=0)
avatar_canvas.pack(pady=(50, 15))
# Membuat lingkaran luar (Border Ring) dan Lingkaran Dalam
avatar_canvas.create_oval(5, 5, 85, 85, fill="#1E293B", outline="#38BDF8", width=2)
avatar_canvas.create_text(45, 45, text="RA", fill="#38BDF8", font=("Segoe UI", 22, "bold"))

# Label Nama Pengguna di Sidebar
lbl_side_name = tk.Label(
    sidebar, 
    text="Ramadhan A. P.", 
    font=("Segoe UI", 12, "bold"), 
    fg="#F8FAFC", 
    bg="#0F172A"
)
lbl_side_name.pack()

# Badge Status Mahasiswa Aktif (Modern Pill Badge)
status_badge = tk.Label(
    sidebar, 
    text="● MAHASISWA AKTIF", 
    font=("Segoe UI", 8, "bold"), 
    fg="#38BDF8", 
    bg="#1E293B",
    padx=12,
    pady=5
)
status_badge.pack(pady=(10, 0))

# Footer Sederhana di Bagian Bawah Sidebar
lbl_footer = tk.Label(
    sidebar, 
    text="SIAKAD v2.5.0 © 2026", 
    font=("Segoe UI", 8), 
    fg="#64748B", 
    bg="#0F172A"
)
lbl_footer.pack(side="bottom", pady=20)


# ==================== MAIN CONTENT AREA (KANAN) ====================

main_content = tk.Frame(root, bg="#F1F5F9", padx=30, pady=25)
main_content.pack(side="right", fill="both", expand=True)

# --- BAGIAN 1: HEADER DASHBOARD ---
header_frame = tk.Frame(main_content, bg="#F1F5F9")
header_frame.pack(fill="x", pady=(0, 20))

lbl_header_title = tk.Label(
    header_frame, 
    text="Dashboard Akademik", 
    font=("Segoe UI", 18, "bold"), 
    fg="#0F172A", 
    bg="#F1F5F9"
)
lbl_header_title.pack(anchor="w")

lbl_header_subtitle = tk.Label(
    header_frame, 
    text="Selamat datang kembali di portal informasi akademik Anda.", 
    font=("Segoe UI", 9), 
    fg="#64748B", 
    bg="#F1F5F9"
)
lbl_header_subtitle.pack(anchor="w", pady=(2, 0))


# --- BAGIAN 2: STATISTIK MINI CARDS (IPK, SEMESTER, SKS) ---
stats_container = tk.Frame(main_content, bg="#F1F5F9")
stats_container.pack(fill="x", pady=(0, 20))

# Data struktur untuk Kartu Statistik: (Judul, Nilai, Warna Aksend)
stats_data = [
    ("Indeks Prestasi Kumulatif", "3.85", "📈"),
    ("Semester Berjalan", "06", "📅"),
    ("Total SKS Diambil", "114 SKS", "📝")
]

for title, val, ico in stats_data:
    # Frame Utama Mini Card (Simulasi Shadow via Border Ringan)
    card_stat = tk.Frame(stats_container, bg="#FFFFFF", highlightbackground="#E2E8F0", highlightthickness=1)
    card_stat.pack(side="left", fill="both", expand=True, padx=(0, 15))
    
    # Aksentuasi Garis Vertikal Primer di Sisi Kiri Kartu
    accent_bar = tk.Frame(card_stat, bg="#2563EB", width=4)
    accent_bar.pack(side="left", fill="y")
    
    # Kontainer Teks di Dalam Kartu
    stat_inner = tk.Frame(card_stat, bg="#FFFFFF", padx=15, pady=12)
    stat_inner.pack(side="left", fill="both", expand=True)
    
    lbl_stat_title = tk.Label(stat_inner, text=title, font=("Segoe UI", 8, "bold"), fg="#64748B", bg="#FFFFFF")
    lbl_stat_title.pack(anchor="w")
    
    # Nilai Statistik + Ikon Pendukung
    lbl_stat_val = tk.Label(stat_inner, text=f"{ico} {val}", font=("Segoe UI", 14, "bold"), fg="#0F172A", bg="#FFFFFF")
    lbl_stat_val.pack(anchor="w", pady=(4, 0))


# --- BAGIAN 3: CARD INFORMASI UTAMA (BIODATA DETAIL) ---
info_card = tk.Frame(main_content, bg="#FFFFFF", highlightbackground="#E2E8F0", highlightthickness=1, padx=25, pady=25)
info_card.pack(fill="both", expand=True)

lbl_card_title = tk.Label(
    info_card, 
    text="Informasi Detail Mahasiswa", 
    font=("Segoe UI", 12, "bold"), 
    fg="#0F172A", 
    bg="#FFFFFF"
)
lbl_card_title.pack(anchor="w", pady=(0, 15))

# Grid Frame untuk Menyeimbangkan Tata Letak Data
grid_frame = tk.Frame(info_card, bg="#FFFFFF")
grid_frame.pack(fill="x", anchor="w")

for i, (key, value) in enumerate(biodata.items()):
    # Gabungkan Ikon dengan Nama Atribut
    display_key = f"{icons[key]}{key}"
    
    lbl_field_key = tk.Label(
        grid_frame, 
        text=display_key, 
        font=("Segoe UI", 10, "bold"), 
        fg="#64748B", 
        bg="#FFFFFF"
    )
    lbl_field_key.grid(row=i, column=0, sticky="w", pady=8)

    lbl_separator = tk.Label(
        grid_frame, 
        text=":", 
        font=("Segoe UI", 10), 
        fg="#CBD5E1", 
        bg="#FFFFFF"
    )
    lbl_separator.grid(row=i, column=1, sticky="w", padx=15, pady=8)

    lbl_field_val = tk.Label(
        grid_frame, 
        text=value, 
        font=("Segoe UI", 10), 
        fg="#334155", 
        bg="#FFFFFF"
    )
    lbl_field_val.grid(row=i, column=2, sticky="w", pady=8)


# --- BAGIAN 4: TOMBOL AKSI INTERAKTIF ---
btn_salin = tk.Button(
    info_card,
    text="✨ Salin Ringkasan Profil",
    font=("Segoe UI", 9, "bold"),
    bg="#2563EB",  # Warna Primer
    fg="white",
    activebackground="#1D4ED8",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    padx=18,
    pady=8,
    command=salin_data
)
btn_salin.pack(side="bottom", anchor="e", pady=(15, 0))

# Efek Animasi Hover (Mengubah Intensitas Biru Saat Kursor Mendekat)
def on_btn_enter(e):
    btn_salin.config(bg="#1D4ED8")

def on_btn_leave(e):
    btn_salin.config(bg="#2563EB")

btn_salin.bind("<Enter>", on_btn_enter)
btn_salin.bind("<Leave>", on_btn_leave)

# Menjalankan Siklus Aplikasi
root.mainloop()