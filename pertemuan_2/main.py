import logging
import ttkbootstrap as ttk
from database import init_database, insert_default_data
from views.view_login import LoginView
from views.view_mahasiswa_dashboard import MahasiswaDashboard
from views.view_dosen_dashboard import DosenDashboard

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class AbsensiApp:
    def __init__(self):
        self.root = ttk.Window(themename='superhero')
        self.root.resizable(True, True)
        self.root.minsize(800, 600)

        try:
            init_database()
            insert_default_data()
            logger.info("Database siap")
        except Exception as e:
            logger.critical("Gagal inisialisasi database: %s", e, exc_info=True)
            raise

        self.show_login()

    def show_login(self):
        self.clear_window()
        LoginView(self.root, self.on_login_success)

    def on_login_success(self, user):
        self.clear_window()
        if user['role'] == 'mahasiswa':
            MahasiswaDashboard(self.root, user, self.show_login)
        elif user['role'] == 'dosen':
            DosenDashboard(self.root, user, self.show_login)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AbsensiApp()
    app.run()
