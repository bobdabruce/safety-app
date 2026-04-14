#!/usr/bin/env python3
"""
SafetyNomad Floating Notes
- root Tk() = the notes panel (macOS window with traffic lights)
- coin = small borderless Toplevel shown when collapsed
- Floats above all apps | visible on all Spaces
"""

import tkinter as tk
import urllib.request
import json, os, sys, threading

API_URL    = "http://localhost:8000/api/notes"
SAVE_DELAY = 1200
LOCK_FILE  = "/tmp/safetynomad_notes.lock"

def check_single_instance():
    if os.path.exists(LOCK_FILE):
        try:
            pid = int(open(LOCK_FILE).read().strip())
            os.kill(pid, 0)
            sys.exit(0)
        except (ProcessLookupError, ValueError):
            pass
    open(LOCK_FILE, "w").write(str(os.getpid()))

def remove_lock():
    try: os.remove(LOCK_FILE)
    except FileNotFoundError: pass


class FloatingNotes:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📝 Notes")
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.85)
        self.root.resizable(True, True)
        self.root.configure(bg="#16213e")

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self._exp_w, self._exp_h = 320, 400
        self.root.geometry(f"{self._exp_w}x{self._exp_h}+{sw-340}+{sh-self._exp_h-90}")

        self._save_timer = None
        self._last_saved = ""
        self._our_bundle = self._get_bundle_id()

        self._build_panel()
        self._build_coin()
        self._load_notes()
        self._apply_all_spaces()          # all-spaces (PyObjC only — no level change)

        self.root.protocol("WM_DELETE_WINDOW", self._collapse)
        self.root.mainloop()

    def _get_bundle_id(self):
        try:
            from AppKit import NSRunningApplication
            app = NSRunningApplication.runningApplicationWithProcessIdentifier_(os.getpid())
            return app.bundleIdentifier()
        except Exception:
            return "org.python.python"

    # ── Float above all apps + all Spaces ────────────────────────────────────
    def _set_level(self):
        """Force our windows above everything including Adobe."""
        try:
            from AppKit import NSApplication, NSScreenSaverWindowLevel
            BEHAVIOR = (1 << 0) | (1 << 7)  # CanJoinAllSpaces | FullScreenAuxiliary
            ns_app  = NSApplication.sharedApplication()
            windows = ns_app.windows()
            print(f"[notes] _set_level: {len(windows)} windows", flush=True)
            for w in windows:
                w.setLevel_(NSScreenSaverWindowLevel)  # 1000 — top of the stack
                w.setCollectionBehavior_(BEHAVIOR)
                w.setHidesOnDeactivate_(False)
                w.orderFrontRegardless()
        except Exception as e:
            print(f"[notes] _set_level error: {e}", flush=True)

    def _apply_all_spaces(self):
        self.root.after(600,  self._set_level)
        self.root.after(2000, self._set_level)

    # ── Panel content ─────────────────────────────────────────────────────────
    def _build_panel(self):
        status_bar = tk.Frame(self.root, bg="#0f3460", height=22)
        status_bar.pack(fill="x")
        status_bar.pack_propagate(False)
        self.status_lbl = tk.Label(status_bar, text="", bg="#0f3460", fg="#64748b",
                                   font=("Helvetica Neue", 9))
        self.status_lbl.pack(side="left", padx=10)

        self.text = tk.Text(
            self.root, bg="#1a1a2e", fg="#e2e8f0",
            insertbackground="#e94560", font=("Helvetica Neue", 12),
            wrap="word", relief="flat", padx=10, pady=8, borderwidth=0,
            selectbackground="#3b82f6", selectforeground="white",
        )
        self.text.pack(fill="both", expand=True, padx=2, pady=2)
        self.text.bind("<KeyRelease>", self._on_type)

        bot = tk.Frame(self.root, bg="#0f3460", height=20)
        bot.pack(fill="x")
        bot.pack_propagate(False)
        rz = tk.Label(bot, text="◢  resize", bg="#0f3460", fg="#64748b",
                      cursor="arrow", font=("Helvetica Neue", 9))
        rz.pack(side="right", padx=6)
        rz.bind("<Button-1>",  self._resize_start)
        rz.bind("<B1-Motion>", self._resize_move)

    # ── Coin ──────────────────────────────────────────────────────────────────
    def _build_coin(self):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        self.coin = tk.Toplevel(self.root)
        self.coin.overrideredirect(True)
        self.coin.attributes("-topmost", True)
        self.coin.attributes("-alpha", 0.92)
        self.coin.configure(bg="#f59e0b")
        self.coin.geometry(f"60x60+{sw-76}+{sh-120}")
        self.coin.withdraw()

        lbl = tk.Label(self.coin, text="📝", bg="#f59e0b",
                       font=("Helvetica Neue", 28), cursor="hand2")
        lbl.pack(expand=True)

        self._coin_drag = False
        self._coin_sx = self._coin_sy = 0
        for w in (lbl, self.coin):
            w.bind("<Button-1>",        self._coin_down)
            w.bind("<B1-Motion>",       self._coin_move)
            w.bind("<ButtonRelease-1>", self._coin_up)

    def _coin_down(self, e):
        self._coin_drag = False
        self._coin_sx, self._coin_sy = e.x_root, e.y_root
        self._cdx = e.x_root - self.coin.winfo_x()
        self._cdy = e.y_root - self.coin.winfo_y()

    def _coin_move(self, e):
        if abs(e.x_root - self._coin_sx) > 5 or abs(e.y_root - self._coin_sy) > 5:
            self._coin_drag = True
        if self._coin_drag:
            self.coin.geometry(f"+{e.x_root-self._cdx}+{e.y_root-self._cdy}")

    def _coin_up(self, e):
        if not self._coin_drag:
            self._expand()

    # ── Collapse / Expand ─────────────────────────────────────────────────────
    def _collapse(self):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self._exp_w = self.root.winfo_width()
        self._exp_h = self.root.winfo_height()
        self.root.withdraw()
        self.coin.geometry(f"60x60+{sw-76}+{sh-120}")
        self.coin.deiconify()
        self.coin.attributes("-topmost", True)
        self.coin.lift()

    def _expand(self):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x  = sw - self._exp_w - 20
        y  = sh - self._exp_h - 90
        self.coin.withdraw()
        self.root.geometry(f"{self._exp_w}x{self._exp_h}+{x}+{y}")
        self.root.deiconify()
        self.root.attributes("-topmost", True)
        self.root.lift()
        self.text.focus_set()
        self.root.after(100, self._set_level)   # re-apply level after deiconify resets it

    # ── Resize ────────────────────────────────────────────────────────────────
    def _resize_start(self, e):
        self._rw = self.root.winfo_width()
        self._rh = self.root.winfo_height()
        self._rx, self._ry = e.x_root, e.y_root

    def _resize_move(self, e):
        nw = max(220, self._rw + e.x_root - self._rx)
        nh = max(150, self._rh + e.y_root - self._ry)
        self.root.geometry(f"{nw}x{nh}+{self.root.winfo_x()}+{self.root.winfo_y()}")

    # ── Notes sync ────────────────────────────────────────────────────────────
    def _load_notes(self):
        def fetch():
            try:
                with urllib.request.urlopen(API_URL, timeout=3) as r:
                    content = json.loads(r.read()).get("content", "")
                self._last_saved = content
                self.root.after(0, lambda: self._set_text(content))
            except Exception:
                self.root.after(0, lambda: self._set_status("⚠ offline"))
        threading.Thread(target=fetch, daemon=True).start()

    def _set_text(self, content):
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", content)

    def _on_type(self, _=None):
        if self._save_timer:
            self.root.after_cancel(self._save_timer)
        self._set_status("…")
        self._save_timer = self.root.after(SAVE_DELAY, self._save_notes)

    def _save_notes(self):
        content = self.text.get("1.0", tk.END)
        if content == self._last_saved:
            self._set_status("")
            return
        def post():
            try:
                req = urllib.request.Request(API_URL,
                    data=json.dumps({"content": content}).encode(),
                    headers={"Content-Type": "application/json"}, method="POST")
                urllib.request.urlopen(req, timeout=3)
                self._last_saved = content
                self.root.after(0, lambda: self._set_status("saved ✓"))
                self.root.after(2200, lambda: self._set_status(""))
            except Exception:
                self.root.after(0, lambda: self._set_status("⚠ save failed"))
        threading.Thread(target=post, daemon=True).start()

    def _set_status(self, msg):
        self.status_lbl.config(text=f"  {msg}")


if __name__ == "__main__":
    check_single_instance()
    FloatingNotes()
