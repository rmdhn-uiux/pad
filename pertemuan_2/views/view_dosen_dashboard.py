import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox
from datetime import date
from tkinter import filedialog
from controller.controller_auth import AuthController
from controller.controller_absensi import AbsensiController
from controller.controller_report import ReportController


class DosenDashboard:
    def __init__(self, root, user, on_logout):
        self.root = root
        self.user = user
        self.on_logout = on_logout
        self.auth = AuthController()
        self.auth.set_user(user)
        self.absensi_ctrl = AbsensiController()
        self.report_ctrl = ReportController()

        self.root.title(f"Sistem Absensi - Dosen: {user['nama']}")
        
        # Center the window and set larger dimensions for dashboard view
        self.root.update_idletasks()
        width = 1100
        height = 750
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

        ttk.Label(info_frame, text="👨‍🏫 Dashboard Dosen",
                  font=("Segoe UI", 16, "bold"), bootstyle=INFO).pack(anchor=W)
        ttk.Label(info_frame,
                  text=f"👤 {self.user['nama']}  |  🔑 @{self.user['username']}",
                  font=("Segoe UI", 10), bootstyle=SECONDARY).pack(anchor=W, pady=(2, 0))

        ttk.Button(header, text="🚪 Logout", bootstyle="danger-outline",
                   command=self._handle_logout).pack(side=RIGHT, ipady=3)
        
        # Divider line
        ttk.Separator(self.root, orient=HORIZONTAL).pack(fill=X, padx=25, pady=(0, 10))

    def _build_tabs(self):
        notebook = ttk.Notebook(self.root, bootstyle=INFO)
        notebook.pack(fill=BOTH, expand=True, padx=25, pady=(0, 20))

        tab_mahasiswa = ttk.Frame(notebook, padding=20)
        notebook.add(tab_mahasiswa, text=" 🎓  Daftar Mahasiswa ")
        self._build_tab_mahasiswa(tab_mahasiswa)

        tab_monitoring = ttk.Frame(notebook, padding=20)
        notebook.add(tab_monitoring, text=" 🖥️  Monitoring Absensi ")
        self._build_tab_monitoring(tab_monitoring)

        tab_laporan = ttk.Frame(notebook, padding=20)
        notebook.add(tab_laporan, text=" 📊  Laporan Kehadiran ")
        self._build_tab_laporan(tab_laporan)

    # ---- TAB MAHASISWA ----
    def _build_tab_mahasiswa(self, parent):
        ttk.Label(parent, text="Daftar Mahasiswa",
                  font=("Segoe UI", 14, "bold"), bootstyle=INFO).pack(anchor=W, pady=(0, 15))

        self.mhs_cols = [{"text": "🆔 ID", "stretch": False},
                         {"text": "👤 Nama Mahasiswa", "stretch": True},
                         {"text": "👤 Username", "stretch": False},
                         {"text": "📊 Total Absen", "stretch": False},
                         {"text": "🟢 Hadir", "stretch": False},
                         {"text": "🟡 Izin", "stretch": False},
                         {"text": "🔵 Sakit", "stretch": False},
                         {"text": "🔴 Alpha", "stretch": False}]

        self.table_mahasiswa = Tableview(
            parent, autoalign=True, coldata=self.mhs_cols, rowdata=[],
            paginated=True, searchable=True, bootstyle=INFO
        )
        self.table_mahasiswa.pack(fill=BOTH, expand=True)

        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=X, pady=(15, 0))

        ttk.Button(btn_frame, text="🔄 Refresh Data", bootstyle=INFO,
                   command=self._refresh_mahasiswa).pack(side=LEFT, padx=(0, 10), ipady=3)
        ttk.Button(btn_frame, text="📈 Export Excel", bootstyle=SUCCESS,
                   command=self._export_mahasiswa_excel).pack(side=LEFT, ipady=3)

        self._refresh_mahasiswa()

    def _refresh_mahasiswa(self):
        r = self.absensi_ctrl.rekap_semua_mahasiswa()
        rows = r.get('data', [])
        self._mahasiswa_data = rows
        data = [
            (
                row['id'], row['nama'], row['username'],
                row['total_absen'], row['hadir'], row['izin'],
                row['sakit'], row['alpha']
            )
            for row in rows
        ]
        self.table_mahasiswa.build_table_data(self.mhs_cols, data)

    def _export_mahasiswa_excel(self):
        if not hasattr(self, '_mahasiswa_data') or not self._mahasiswa_data:
            Messagebox.show_warning("Tidak ada data",
                                    "Tampilkan data mahasiswa terlebih dahulu")
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if filename:
            r = self.report_ctrl.export_excel(self._mahasiswa_data, filename)
            if r['success']:
                Messagebox.show_info("Berhasil", r['message'])
            else:
                Messagebox.show_error("Error", r['message'])

    # ---- TAB MONITORING ----
    def _build_tab_monitoring(self, parent):
        ttk.Label(parent, text="Monitoring Absensi",
                  font=("Segoe UI", 14, "bold"), bootstyle=INFO).pack(anchor=W, pady=(0, 15))

        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=X, pady=(0, 15))

        ttk.Label(filter_frame, text="📅 Tanggal:").pack(side=LEFT, padx=(0, 5))
        self.entry_tanggal = ttk.Entry(filter_frame, width=15, font=("Segoe UI", 10))
        self.entry_tanggal.insert(0, date.today().isoformat())
        self.entry_tanggal.pack(side=LEFT, padx=(0, 15))

        ttk.Label(filter_frame, text="👤 Mahasiswa:").pack(side=LEFT, padx=(10, 5))
        self.entry_filter_nama = ttk.Entry(filter_frame, width=20, font=("Segoe UI", 10))
        self.entry_filter_nama.pack(side=LEFT, padx=(0, 15))

        ttk.Button(filter_frame, text="Cari", bootstyle=INFO,
                   command=self._cari_monitoring).pack(side=LEFT, padx=(0, 10), ipady=2)
        ttk.Button(filter_frame, text="Reset", bootstyle=SECONDARY,
                   command=self._refresh_monitoring).pack(side=LEFT, ipady=2)

        self.mon_cols = [{"text": "🆔 ID", "stretch": False},
                         {"text": "👤 Nama", "stretch": True},
                         {"text": "📅 Tanggal", "stretch": False},
                         {"text": "📥 Jam Masuk", "stretch": False},
                         {"text": "📤 Jam Pulang", "stretch": False},
                         {"text": "📋 Status", "stretch": False},
                         {"text": "📝 Keterangan", "stretch": True}]

        self.table_monitoring = Tableview(
            parent, autoalign=True, coldata=self.mon_cols, rowdata=[],
            paginated=True, searchable=False, bootstyle=INFO
        )
        self.table_monitoring.pack(fill=BOTH, expand=True)

        self._refresh_monitoring()

    def _cari_monitoring(self):
        keyword = self.entry_filter_nama.get().strip()
        r = self.absensi_ctrl.riwayat_absensi()
        rows = r.get('data', [])
        if keyword:
            rows = [row for row in rows
                    if keyword.lower() in row.get('user_nama', '').lower()]
        self._populate_monitoring(rows)

    def _refresh_monitoring(self):
        r = self.absensi_ctrl.riwayat_absensi()
        self._populate_monitoring(r.get('data', []))

    def _populate_monitoring(self, rows):
        data = []
        for row in rows:
            status_str = row['status'].lower()
            status_emoji = "🟢" if status_str == "hadir" else "🟡" if status_str == "izin" else "🔵" if status_str == "sakit" else "⚫"
            data.append((
                row['id'], row['user_nama'], row['tanggal'],
                row.get('jam_masuk') or '-', row.get('jam_pulang') or '-',
                f"{status_emoji} {row['status'].title()}", row.get('keterangan') or '-'
            ))
        self.table_monitoring.build_table_data(self.mon_cols, data)

    # ---- TAB LAPORAN ----
    def _build_tab_laporan(self, parent):
        ttk.Label(parent, text="Laporan Absensi",
                  font=("Segoe UI", 14, "bold"), bootstyle=INFO).pack(anchor=W, pady=(0, 15))

        notebook = ttk.Notebook(parent, bootstyle=SECONDARY)
        notebook.pack(fill=BOTH, expand=True)

        tab_harian = ttk.Frame(notebook, padding=15)
        notebook.add(tab_harian, text=" 📅 Laporan Harian ")
        self._build_laporan_harian(tab_harian)

        tab_bulanan = ttk.Frame(notebook, padding=15)
        notebook.add(tab_bulanan, text=" 📅 Laporan Bulanan ")
        self._build_laporan_bulanan(tab_bulanan)

    def _build_laporan_harian(self, parent):
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=X, pady=(0, 15))

        ttk.Label(filter_frame, text="📅 Tanggal:").pack(side=LEFT, padx=(0, 5))
        self.lap_entry_tgl = ttk.Entry(filter_frame, width=15, font=("Segoe UI", 10))
        self.lap_entry_tgl.insert(0, date.today().isoformat())
        self.lap_entry_tgl.pack(side=LEFT, padx=(0, 15))

        ttk.Button(filter_frame, text="👁️ Tampilkan", bootstyle=INFO,
                   command=self._tampilkan_laporan_harian).pack(side=LEFT, padx=(0, 10), ipady=2)
        ttk.Button(filter_frame, text="📈 Export Excel", bootstyle=SUCCESS,
                   command=lambda: self._export_data('harian', 'excel')).pack(
                       side=LEFT, padx=(0, 5), ipady=2)
        ttk.Button(filter_frame, text="📄 Export PDF", bootstyle=DANGER,
                   command=lambda: self._export_data('harian', 'pdf')).pack(side=LEFT, ipady=2)

        self.lap_harian_stat = ttk.Frame(parent)
        self.lap_harian_stat.pack(fill=X, pady=(0, 15))
        self.lap_harian_stat_label = ttk.Label(self.lap_harian_stat, text="",
                                                font=("Segoe UI", 10, "bold"), bootstyle=INFO)
        self.lap_harian_stat_label.pack(anchor=W)

        self.lap_harian_cols = [{"text": "👤 Nama Mahasiswa", "stretch": True},
                                {"text": "📥 Jam Masuk", "stretch": False},
                                {"text": "📤 Jam Pulang", "stretch": False},
                                {"text": "📋 Status", "stretch": False},
                                {"text": "📝 Keterangan", "stretch": True}]

        self.table_lap_harian = Tableview(
            parent, autoalign=True, coldata=self.lap_harian_cols, rowdata=[],
            paginated=True, searchable=False, bootstyle=INFO
        )
        self.table_lap_harian.pack(fill=BOTH, expand=True)

    def _build_laporan_bulanan(self, parent):
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=X, pady=(0, 15))

        now = date.today()
        ttk.Label(filter_frame, text="📅 Bulan:").pack(side=LEFT, padx=(0, 5))
        self.lap_bulan_bulan = ttk.Combobox(filter_frame, values=list(range(1, 13)),
                                            width=5, state="readonly", font=("Segoe UI", 10))
        self.lap_bulan_bulan.set(now.month)
        self.lap_bulan_bulan.pack(side=LEFT, padx=(0, 15))

        ttk.Label(filter_frame, text="📅 Tahun:").pack(side=LEFT, padx=(0, 5))
        self.lap_bulan_tahun = ttk.Combobox(
            filter_frame, values=list(range(now.year - 5, now.year + 2)),
            width=6, state="readonly", font=("Segoe UI", 10))
        self.lap_bulan_tahun.set(now.year)
        self.lap_bulan_tahun.pack(side=LEFT, padx=(0, 15))

        ttk.Button(filter_frame, text="👁️ Tampilkan", bootstyle=INFO,
                   command=self._tampilkan_laporan_bulanan).pack(side=LEFT, padx=(0, 10), ipady=2)
        ttk.Button(filter_frame, text="📈 Export Excel", bootstyle=SUCCESS,
                   command=lambda: self._export_data('bulanan', 'excel')).pack(
                       side=LEFT, padx=(0, 5), ipady=2)
        ttk.Button(filter_frame, text="📄 Export PDF", bootstyle=DANGER,
                   command=lambda: self._export_data('bulanan', 'pdf')).pack(side=LEFT, ipady=2)

        self.lap_bulanan_cols = [{"text": "👤 Nama Mahasiswa", "stretch": True},
                                 {"text": "👤 Username", "stretch": False},
                                 {"text": "📅 Total Hari", "stretch": False},
                                 {"text": "🟢 Hadir", "stretch": False},
                                 {"text": "🟡 Izin", "stretch": False},
                                 {"text": "🔵 Sakit", "stretch": False},
                                 {"text": "🔴 Alpha", "stretch": False}]

        self.table_lap_bulanan = Tableview(
            parent, autoalign=True, coldata=self.lap_bulanan_cols, rowdata=[],
            paginated=True, searchable=False, bootstyle=INFO
        )
        self.table_lap_bulanan.pack(fill=BOTH, expand=True)

    def _tampilkan_laporan_harian(self):
        tgl = self.lap_entry_tgl.get().strip()
        r = self.report_ctrl.laporan_harian(tgl)
        if not r['success']:
            Messagebox.show_error("Error", r['message'])
            return

        stat = r['statistik']
        text = (f"📊 Statistik Harian:  Total: {stat['total']}  |  🟢 Hadir: {stat['hadir']}  |  "
                f"🟡 Izin: {stat['izin']}  |  🔵 Sakit: {stat['sakit']}  |  "
                f"🔴 Alpha: {stat['alpha']}")
        self.lap_harian_stat_label.config(text=text)
        self._lap_harian_data = r['data']

        data = []
        for row in r['data']:
            status_str = row['status'].lower()
            status_emoji = "🟢" if status_str == "hadir" else "🟡" if status_str == "izin" else "🔵" if status_str == "sakit" else "⚫"
            data.append((
                row['mahasiswa'],
                row.get('jam_masuk') or '-',
                row.get('jam_pulang') or '-',
                f"{status_emoji} {row['status'].title()}",
                row.get('keterangan') or '-'
            ))
        self.table_lap_harian.build_table_data(self.lap_harian_cols, data)

    def _tampilkan_laporan_bulanan(self):
        bulan = int(self.lap_bulan_bulan.get())
        tahun = int(self.lap_bulan_tahun.get())
        r = self.report_ctrl.laporan_bulanan(bulan, tahun)
        if not r['success']:
            Messagebox.show_error("Error", r['message'])
            return

        self._lap_bulanan_data = r['data']
        data = [
            (
                row['nama'], row['username'],
                row['total_hari'], row['hadir'],
                row['izin'], row['sakit'], row['alpha']
            )
            for row in r['data']
        ]
        self.table_lap_bulanan.build_table_data(self.lap_bulanan_cols, data)

    def _export_data(self, report_type: str, fmt: str):
        if report_type == 'harian':
            data_attr = '_lap_harian_data'
            title_prefix = f"Laporan Harian - {self.lap_entry_tgl.get().strip()}"
        else:
            data_attr = '_lap_bulanan_data'
            title_prefix = (f"Laporan Bulanan - "
                            f"{self.lap_bulan_bulan.get()}/{self.lap_bulan_tahun.get()}")

        if not hasattr(self, data_attr) or not getattr(self, data_attr):
            Messagebox.show_warning("Tidak ada data",
                                    "Tampilkan laporan terlebih dahulu")
            return

        ext = 'xlsx' if fmt == 'excel' else 'pdf'
        filename = filedialog.asksaveasfilename(
            defaultextension=f".{ext}",
            filetypes=[(f"{fmt.upper()} files", f"*.{ext}")]
        )
        if not filename:
            return

        data = getattr(self, data_attr)
        if fmt == 'excel':
            r = self.report_ctrl.export_excel(data, filename)
        else:
            r = self.report_ctrl.export_pdf(data, filename, title_prefix)

        if r['success']:
            Messagebox.show_info("Berhasil", r['message'])
        else:
            Messagebox.show_error("Error", r['message'])

    def _handle_logout(self):
        self.auth.logout()
        self.on_logout()

