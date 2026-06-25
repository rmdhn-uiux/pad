import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from datetime import date
from controller.controller_auth import AuthController
from controller.controller_absensi import AbsensiController


class MahasiswaDashboard:
    def __init__(self, root, user, on_logout):
        self.root = root
        self.user = user
        self.on_logout = on_logout
        self.auth = AuthController()
        self.auth.set_user(user)
        self.absensi_ctrl = AbsensiController()

        self.root.title(f"Sistem Absensi - {user['nama']}")
        
        # Center the window on screen and increase width slightly for better table layout
        self.root.update_idletasks()
        width = 900
        height = 650
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(True, True)

        self._build_header()
        self._build_tabs()

    def _build_header(self):
        header = ttk.Frame(self.root, padding=(25, 15))
        header.pack(fill=X)

        info_frame = ttk.Frame(header)
        info_frame.pack(side=LEFT)

        ttk.Label(info_frame, text=f"👋 Selamat Datang, {self.user['nama']}",
                  font=("Segoe UI", 16, "bold"), bootstyle=INFO).pack(anchor=W)
        ttk.Label(info_frame,
                  text=f"👤 @{self.user['username']}  |  🔑 {self.user['role'].title()}",
                  font=("Segoe UI", 10), bootstyle=SECONDARY).pack(anchor=W, pady=(2, 0))

        ttk.Button(header, text="🚪 Logout", bootstyle="danger-outline",
                   command=self._handle_logout).pack(side=RIGHT, ipady=3)
        
        # Divider line
        ttk.Separator(self.root, orient=HORIZONTAL).pack(fill=X, padx=25, pady=(0, 10))

    def _build_tabs(self):
        notebook = ttk.Notebook(self.root, bootstyle=INFO)
        notebook.pack(fill=BOTH, expand=True, padx=25, pady=(0, 20))

        tab_absen = ttk.Frame(notebook, padding=20)
        notebook.add(tab_absen, text=" 📅  Absensi Harian ")
        self._build_tab_absen(tab_absen)

        tab_riwayat = ttk.Frame(notebook, padding=20)
        notebook.add(tab_riwayat, text=" 📜  Riwayat Kehadiran ")
        self._build_tab_riwayat(tab_riwayat)

    def _build_tab_absen(self, parent):
        card = ttk.Frame(parent, bootstyle=INFO, padding=20)
        card.pack(fill=X, pady=10)

        ttk.Label(card, text="Absensi Hari Ini",
                  font=("Segoe UI", 14, "bold"), bootstyle=LIGHT).pack(anchor=W, pady=(0, 10))

        self.today_frame = ttk.Frame(card)
        self.today_frame.pack(fill=X, pady=10)

        self.label_tanggal = ttk.Label(self.today_frame,
                                       text=f"📅 Tanggal: {date.today().isoformat()}",
                                       font=("Segoe UI", 11))
        self.label_tanggal.pack(anchor=W, pady=3)

        self.label_status = ttk.Label(self.today_frame,
                                      text="Status: 🔴 Belum absen",
                                      font=("Segoe UI", 11, "bold"), bootstyle=WARNING)
        self.label_status.pack(anchor=W, pady=3)

        self.label_jam_masuk = ttk.Label(self.today_frame, text="📥 Jam Masuk: -",
                                         font=("Segoe UI", 11))
        self.label_jam_masuk.pack(anchor=W, pady=3)

        self.label_jam_pulang = ttk.Label(self.today_frame, text="📤 Jam Pulang: -",
                                          font=("Segoe UI", 11))
        self.label_jam_pulang.pack(anchor=W, pady=3)

        btn_frame = ttk.Frame(card)
        btn_frame.pack(fill=X, pady=(15, 5))

        self.btn_masuk = ttk.Button(btn_frame, text="📥 Absen Masuk",
                                    bootstyle=SUCCESS, width=20,
                                    command=self._absen_masuk)
        self.btn_masuk.pack(side=LEFT, padx=(0, 15), ipady=4)

        self.btn_pulang = ttk.Button(btn_frame, text="📤 Absen Pulang",
                                     bootstyle=WARNING, width=20,
                                     command=self._absen_pulang)
        self.btn_pulang.pack(side=LEFT, ipady=4)

        self.label_info = ttk.Label(card, text="", font=("Segoe UI", 10))
        self.label_info.pack(anchor=W, pady=(10, 0))

        self._refresh_status()

    def _build_tab_riwayat(self, parent):
        ttk.Label(parent, text="Riwayat Absensi",
                  font=("Segoe UI", 14, "bold"), bootstyle=INFO).pack(anchor=W, pady=(0, 15))

        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=X, pady=(0, 15))

        ttk.Label(search_frame, text="🔍 Cari Data:").pack(side=LEFT, padx=(0, 5))
        self.entry_cari = ttk.Entry(search_frame, width=30, font=("Segoe UI", 10))
        self.entry_cari.pack(side=LEFT, padx=(0, 10))
        ttk.Button(search_frame, text="Cari", bootstyle=INFO,
                   command=self._cari_riwayat).pack(side=LEFT, ipady=1)

        self.riwayat_cols = [{"text": "📅 Tanggal", "stretch": False},
                             {"text": "📥 Jam Masuk", "stretch": False},
                             {"text": "📤 Jam Pulang", "stretch": False},
                             {"text": "📋 Status", "stretch": False},
                             {"text": "📝 Keterangan", "stretch": True}]

        self.table_riwayat = Tableview(
            parent, autoalign=True,
            coldata=self.riwayat_cols, rowdata=[],
            paginated=True, searchable=False, bootstyle=INFO
        )
        self.table_riwayat.pack(fill=BOTH, expand=True)

        self._refresh_riwayat()

    def _refresh_status(self):
        r = self.absensi_ctrl.cek_absen_hari_ini(self.user['id'])
        if r.get('sudah_absen') and r.get('data'):
            data = r['data']
            status_str = data['status'].lower()
            status_emoji = "🟢" if status_str == "hadir" else "🟡" if status_str == "izin" else "🔵" if status_str == "sakit" else "⚫"
            self.label_status.config(text=f"Status: {status_emoji} {data['status'].title()}",
                                     bootstyle=SUCCESS if data['status'] == 'hadir' else WARNING)
            self.label_jam_masuk.config(text=f"📥 Jam Masuk: {data.get('jam_masuk', '-')}")
            self.label_jam_pulang.config(text=f"📤 Jam Pulang: {data.get('jam_pulang', '-')}")
            self.btn_masuk.config(state=DISABLED)
            self.btn_pulang.config(state=DISABLED if data.get('jam_pulang') else NORMAL)
        else:
            self.label_status.config(text="Status: 🔴 Belum absen", bootstyle=WARNING)
            self.label_jam_masuk.config(text="📥 Jam Masuk: -")
            self.label_jam_pulang.config(text="📤 Jam Pulang: -")
            self.btn_masuk.config(state=NORMAL)
            self.btn_pulang.config(state=DISABLED)

    def _absen_masuk(self):
        r = self.absensi_ctrl.absen_masuk(self.user['id'])
        if r['success']:
            self.label_info.config(text="🎉 Absen masuk berhasil!", bootstyle=SUCCESS)
        else:
            self.label_info.config(text=f"❌ {r['message']}", bootstyle=DANGER)
        self._refresh_status()
        self._refresh_riwayat()
        self.root.after(3000, lambda: self.label_info.config(text=""))

    def _absen_pulang(self):
        r = self.absensi_ctrl.absen_pulang(self.user['id'])
        if r['success']:
            self.label_info.config(text="🎉 Absen pulang berhasil!", bootstyle=SUCCESS)
        else:
            self.label_info.config(text=f"❌ {r['message']}", bootstyle=DANGER)
        self._refresh_status()
        self._refresh_riwayat()
        self.root.after(3000, lambda: self.label_info.config(text=""))

    def _cari_riwayat(self):
        keyword = self.entry_cari.get().strip()
        if keyword:
            r = self.absensi_ctrl.riwayat_absensi(user_id=self.user['id'])
            rows = r.get('data', [])
            rows = [row for row in rows if keyword.lower() in str(row.values()).lower()]
        else:
            r = self.absensi_ctrl.riwayat_absensi(user_id=self.user['id'])
            rows = r.get('data', [])
        self._populate_table(rows)

    def _refresh_riwayat(self):
        r = self.absensi_ctrl.riwayat_absensi(user_id=self.user['id'])
        self._populate_table(r.get('data', []))

    def _populate_table(self, rows):
        data = []
        for row in rows:
            status_str = row['status'].lower()
            status_emoji = "🟢" if status_str == "hadir" else "🟡" if status_str == "izin" else "🔵" if status_str == "sakit" else "⚫"
            data.append((
                row['tanggal'],
                row.get('jam_masuk') or '-',
                row.get('jam_pulang') or '-',
                f"{status_emoji} {row['status'].title()}",
                row.get('keterangan') or '-'
            ))
        self.table_riwayat.build_table_data(self.riwayat_cols, data)

    def _handle_logout(self):
        self.auth.logout()
        self.on_logout()

