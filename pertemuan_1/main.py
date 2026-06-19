import tkinter as tk
from tkinter import messagebox

def salin_data():
    """Fungsi untuk menyalin data ke clipboard"""
    text_data = (
        f"Nama: {biodata['Nama Lengkap']}\n"
        f"NIM: {biodata['NIM']}\n"
        f"Program Studi: {biodata['Program Studi']}\n"
        f"Alamat: {biodata['Alamat']}\n"
        f"Email: {biodata['Email']}"
    )
    root.clipboard_clear()
    root.clipboard_append(text_data)
    messagebox.showinfo("Sukses", "Biodata berhasil disalin!")

# Inisialisasi Window
root = tk.Tk()
root.title("Dashboard Profile Mahasiswa")
root.geometry("650x360")
root.configure(bg="#F8FAFC")
root.resizable(False, False)  # Mengunci ukuran jendela agar tetap rapi

# ==================== PANEL KIRI (SIDEBAR PROFILE) ====================
panel_kiri = tk.Frame(root, bg="#0F172A", width=200)
panel_kiri.pack(side="left", fill="y")
panel_kiri.pack_propagate(False) # Mengunci ukuran panel kiri

# Avatar Lingkaran Menggunakan Canvas (Inisialisasi Nama)
avatar = tk.Canvas(panel_kiri, width=80, height=80, bg="#0F172A", bd=0, highlightthickness=0)
avatar.pack(pady=(45, 15))
avatar.create_oval(5, 5, 75, 75, fill="#2563EB", outline="") # Lingkaran Biru
avatar.create_text(40, 40, text="RA", fill="white", font=("Segoe UI", 18, "bold")) # Inisial

# Nama Singkat di Sidebar
lbl_short_name = tk.Label(
    panel_kiri, 
    text="Ramadhan A.", 
    font=("Segoe UI", 12, "bold"), 
    fg="#F8FAFC", 
    bg="#0F172A"
)
lbl_short_name.pack()

# Tag Status (Badge)
lbl_status = tk.Label(
    panel_kiri, 
    text="MAHASISWA AKTIF", 
    font=("Segoe UI", 8, "bold"), 
    fg="#38BDF8", 
    bg="#1E293B",
    padx=10,
    pady=4
)
lbl_status.pack(pady=(8, 0))


# ==================== PANEL KANAN (DATA UTAMA) ====================
panel_kanan = tk.Frame(root, bg="#FFFFFF", padx=35, pady=35)
panel_kanan.pack(side="right", fill="both", expand=True)

# Judul Bagian
lbl_title = tk.Label(
    panel_kanan, 
    text="Informasi Akademik", 
    font=("Segoe UI", 16, "bold"), 
    fg="#0F172A", 
    bg="#FFFFFF"
)
lbl_title.pack(anchor="w", pady=(0, 20))

# Kontainer Grid Data
grid_frame = tk.Frame(panel_kanan, bg="#FFFFFF")
grid_frame.pack(fill="x", anchor="w")

# Data Pasangan Key dan Value
biodata = {
    "Nama Lengkap": "Ramadhan Anton Pratama",
    "NIM": "23250017",
    "Program Studi": "Teknik Informatika",
    "Alamat": "Bandung, Jawa Barat",
    "Email": "ramadhananton@example.com"
}

# Perulangan untuk menyusun label secara otomatis dan presisi
for i, (key, value) in enumerate(biodata.items()):
    # Label Judul Data (Kiri)
    lbl_key = tk.Label(
        grid_frame, 
        text=key, 
        font=("Segoe UI", 10, "bold"), 
        fg="#64748B", 
        bg="#FFFFFF"
    )
    lbl_key.grid(row=i, column=0, sticky="w", pady=6)

    # Label Isi Data (Kanan)
    lbl_val = tk.Label(
        grid_frame, 
        text=value, 
        font=("Segoe UI", 10), 
        fg="#334155", 
        bg="#FFFFFF"
    )
    lbl_val.grid(row=i, column=1, sticky="w", padx=(25, 0), pady=6)

# Tombol Aksi Modern (Salin Data)
btn_salin = tk.Button(
    panel_kanan,
    text="Salin Biodata",
    font=("Segoe UI", 9, "bold"),
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    padx=15,
    pady=8,
    command=salin_data
)
btn_salin.pack(side="bottom", anchor="e")

# Efek Hover untuk Tombol (Berubah warna saat kursor masuk/keluar)
def on_enter(e):
    btn_salin.config(bg="#1D4ED8")

def on_leave(e):
    btn_salin.config(bg="#2563EB")

btn_salin.bind("<Enter>", on_enter)
btn_salin.bind("<Leave>", on_leave)

root.mainloop()