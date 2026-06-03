"""
============================================================
  AMAZON AI + INFORMATION SECURITY SYSTEM  v2.0
  AI Advancements + IS Project  |  Python / Tkinter
============================================================
  REQUIREMENTS:
      pip install pandas scikit-learn requests

  FEATURES:
    - SHA-256 password hashing
    - MD5 blockchain chaining (data integrity)
    - TF-IDF + Cosine Similarity recommender
    - AI Research panel (timeline + live AI Q&A)
    - Full IS dashboard (CIA Triad)
    - Security audit log
    - Demo dataset (no CSV needed)
============================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import hashlib
import time
import os
import threading
import json

# ── optional imports ──────────────────────────────────────
try:
    import pandas as pd
    PANDAS_OK = True
except ImportError:
    PANDAS_OK = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_OK = True
except ImportError:
    SKLEARN_OK = False

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

# ══════════════════════════════════════════════════════════
#  COLOUR PALETTE  (dark cyber theme)
# ══════════════════════════════════════════════════════════
C = {
    "bg":      "#0a0e1a",
    "bg2":     "#111827",
    "bg3":     "#1a2236",
    "card":    "#141c2e",
    "border":  "#1e3a5f",
    "accent":  "#63b3ed",
    "accent2": "#76e4f7",
    "green":   "#68d391",
    "red":     "#fc8181",
    "amber":   "#f6ad55",
    "purple":  "#b794f4",
    "text":    "#e2e8f0",
    "text2":   "#94a3b8",
    "text3":   "#64748b",
    "white":   "#ffffff",
}

FONTS = {
    "title":   ("Courier New", 18, "bold"),
    "heading": ("Courier New", 13, "bold"),
    "body":    ("Segoe UI",    11),
    "small":   ("Segoe UI",    10),
    "mono":    ("Courier New", 10),
    "mono_s":  ("Courier New",  9),
    "btn":     ("Segoe UI",    11, "bold"),
}

# ══════════════════════════════════════════════════════════
#  SECURITY BACKEND
# ══════════════════════════════════════════════════════════
USERS = {"admin": hashlib.sha256("1234".encode()).hexdigest()}

security_log  = []   # list of (timestamp, event, level)
blockchain    = []   # list of block dicts
search_count  = 0
products_data = []   # list of {"name":…, "description":…}
sim_matrix    = None
current_user  = None
session_key   = None


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def md5hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def now_str() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def add_log(event: str, level: str = "INFO"):
    security_log.append((now_str(), event, level))


def add_block(data: str):
    prev = blockchain[-1]["hash"] if blockchain else "0" * 32
    blk = {
        "index":     len(blockchain) + 1,
        "timestamp": now_str(),
        "data":      data,
        "prev_hash": prev,
        "hash":      md5hash(data + prev + str(time.time())),
    }
    blockchain.append(blk)


# ══════════════════════════════════════════════════════════
#  DEMO DATASET
# ══════════════════════════════════════════════════════════
DEMO_PRODUCTS = [
    ("Samsung Galaxy S24",       "smartphone android 5G camera flagship mobile"),
    ("iPhone 15 Pro",            "smartphone apple iOS 5G camera flagship mobile premium"),
    ("Google Pixel 8",           "smartphone android google camera AI mobile photography"),
    ("OnePlus 12",               "smartphone android fast charging flagship performance"),
    ("MacBook Pro M3",           "laptop apple silicon professional performance portable"),
    ("Dell XPS 15",              "laptop windows intel professional performance portable"),
    ("ThinkPad X1 Carbon",       "laptop windows business professional lightweight"),
    ("HP Spectre x360",          "laptop windows convertible touchscreen portable premium"),
    ("iPad Pro 12.9",            "tablet apple stylus productivity professional display"),
    ("Samsung Galaxy Tab S9",    "tablet android stylus productivity display AMOLED"),
    ("Sony WH-1000XM5",          "headphones wireless noise cancelling premium audio"),
    ("Bose QuietComfort 45",     "headphones wireless noise cancelling premium comfort"),
    ("Apple AirPods Pro",        "earbuds wireless noise cancelling apple premium"),
    ("Sony WF-1000XM5",          "earbuds wireless noise cancelling premium audio compact"),
    ("Logitech MX Master 3",     "mouse wireless ergonomic productivity professional"),
    ("Apple Magic Mouse",        "mouse wireless apple trackpad gesture professional"),
    ("Mechanical Keyboard Blue", "keyboard mechanical gaming typing tactile switches"),
    ("Logitech G915",            "keyboard wireless mechanical gaming low profile RGB"),
    ("LG 27UK850 4K Monitor",    "monitor 4K UHD display professional USB-C HDR"),
    ("Dell U2722D 27",           "monitor 4K display professional USB-C IPS panel"),
    ("Samsung T7 SSD",           "storage portable SSD USB fast transfer data"),
    ("WD Elements 4TB",          "storage portable HDD USB backup data large"),
    ("Anker PowerBank 20000",    "power bank portable battery charging USB large"),
    ("Belkin 3-in-1 Charger",    "charger wireless multi-device apple watch AirPods"),
    ("GoPro Hero 12",            "camera action waterproof 4K adventure sports video"),
    ("DJI Mini 4 Pro",           "drone camera 4K aerial photography lightweight compact"),
    ("Canon EOS R6",             "camera mirrorless full frame photography professional"),
    ("Sony Alpha A7IV",          "camera mirrorless full frame photography professional video"),
    ("Amazon Echo Show 10",      "smart display alexa home assistant screen speaker"),
    ("Google Nest Hub Max",      "smart display google home assistant screen speaker"),
    ("Amazon Fire TV Stick 4K",  "streaming media player TV 4K HDR Dolby Vision"),
    ("Chromecast with Google TV","streaming media player TV 4K HDR google assistant"),
    ("Roku Streaming Stick 4K",  "streaming media player TV 4K HDR roku channel"),
    ("Fitbit Charge 6",          "fitness tracker wearable health heart rate GPS"),
    ("Apple Watch Series 9",     "smartwatch apple health fitness GPS premium wearable"),
    ("Samsung Galaxy Watch 6",   "smartwatch android health fitness GPS wearable"),
    ("Garmin Fenix 7",           "smartwatch GPS outdoor fitness premium rugged"),
    ("ASUS ROG Gaming Laptop",   "laptop gaming performance GPU RGB high refresh"),
    ("Alienware m18",            "laptop gaming performance GPU desktop replacement"),
    ("Razer Blade 16",           "laptop gaming performance premium OLED display RGB"),
    ("Xbox Series X",            "gaming console microsoft 4K performance ray tracing"),
    ("PlayStation 5",            "gaming console sony 4K performance ray tracing SSD"),
    ("Nintendo Switch OLED",     "gaming console nintendo portable hybrid handheld"),
    ("Logitech C920 Webcam",     "webcam HD 1080p video streaming conferencing USB"),
    ("Elgato Facecam",           "webcam 4K streaming content creator video USB"),
    ("Jabra Evolve2 85",         "headset wireless business professional noise cancel"),
    ("Blue Yeti Microphone",     "microphone USB studio recording podcast streaming"),
    ("RODE NT-USB",              "microphone USB studio recording podcast streaming"),
    ("Anker USB-C Hub 10-in-1",  "hub USB-C ports HDMI SD card reader docking"),
    ("Elgato Stream Deck MK.2",  "controller streaming keys customizable macro shortcuts"),
]

AI_TIMELINE = [
    ("1956", "Birth of AI",         "Dartmouth Conference coins 'Artificial Intelligence'"),
    ("1969", "Perceptron",          "Minsky & Papert prove perceptron limitations"),
    ("1986", "Backpropagation",     "Rumelhart, Hinton & Williams publish neural net training"),
    ("1997", "Amazon Recommends",   "Item-to-item collaborative filtering deployed at scale"),
    ("2001", "TF-IDF Standard",     "Content-based filtering using term frequency vectors"),
    ("2006", "Deep Belief Nets",    "Hinton's deep learning renaissance begins"),
    ("2012", "AlexNet",             "CNNs win ImageNet — deep learning goes mainstream"),
    ("2014", "GANs",                "Goodfellow introduces Generative Adversarial Networks"),
    ("2017", "Transformers",        "'Attention Is All You Need' — foundation of LLMs"),
    ("2020", "GPT-3",               "175B parameter language model shows emergent abilities"),
    ("2022", "ChatGPT",             "OpenAI launches ChatGPT — 100M users in 60 days"),
    ("2023", "Claude / GPT-4",      "Multimodal AI assistants reach mainstream adoption"),
    ("2024", "AI Everywhere",       "AI agents, code assistants, real-time recommendation"),
]

IS_TIMELINE = [
    ("1977", "RSA Encryption",      "Rivest, Shamir, Adleman — public-key cryptography"),
    ("1993", "MD5 Hash",            "Ronald Rivest's 128-bit message digest algorithm"),
    ("2001", "SHA-256",             "NIST standardizes 256-bit Secure Hash Algorithm"),
    ("2004", "MD5 Broken",          "Wang & Yu demonstrate MD5 collision attacks"),
    ("2008", "Blockchain",          "Satoshi Nakamoto chains SHA-256 blocks in Bitcoin"),
    ("2013", "Zero-Trust",          "BeyondCorp: never trust, always verify architecture"),
    ("2018", "GDPR",                "EU mandates data protection and breach notification"),
    ("2024", "AI-Powered IS",       "ML anomaly detection & real-time threat intelligence"),
]

IS_CONCEPTS = [
    ("Confidentiality", C["green"],  "SHA-256 hashing prevents plaintext password exposure"),
    ("Integrity",       C["accent"], "MD5 blockchain chaining detects any data tampering"),
    ("Availability",    C["purple"], "Session-based access control with activity tracking"),
    ("Authentication",  C["amber"],  "Credential verification with unique session tokens"),
    ("Non-repudiation", C["red"],    "Immutable append-only audit log with timestamps"),
    ("Authorization",   C["accent2"],"Role-based user access to all system modules"),
]

RESEARCH_CACHE = {
    "tfidf": (
        "TF-IDF (Term Frequency-Inverse Document Frequency)\n\n"
        "• TF  = how often a word appears in ONE document\n"
        "• IDF = how RARE the word is across ALL documents\n"
        "• Score = TF × IDF  —  rare + frequent words score highest\n\n"
        "Cosine Similarity:\n"
        "• Each product → high-dimensional TF-IDF vector\n"
        "• Cosine of angle between vectors = similarity score\n"
        "• Score 1.0 = identical, 0.0 = completely different\n\n"
        "This system: vectorizes all products, then finds the\n"
        "5 nearest neighbours by cosine distance."
    ),
    "blockchain": (
        "Blockchain for Data Integrity (IS Application)\n\n"
        "• Each BLOCK contains: index, timestamp, event data,\n"
        "  previous_hash, current_hash\n"
        "• current_hash = MD5(event_data + previous_hash)\n"
        "• Changing ANY block invalidates all blocks after it\n"
        "• Genesis block has previous_hash = '000...000'\n\n"
        "IS Benefits:\n"
        "• Tamper-evidence  • Audit trail integrity\n"
        "• Non-repudiation  • Digital forensics support"
    ),
    "sha": (
        "SHA-256 vs MD5 — Security Comparison\n\n"
        "SHA-256:\n"
        "• Output: 256 bits (64 hex chars)\n"
        "• Status: SECURE  — used in Bitcoin, TLS, passwords\n"
        "• Collision resistance: computationally infeasible\n\n"
        "MD5:\n"
        "• Output: 128 bits (32 hex chars)\n"
        "• Status: BROKEN for security (collisions found 2004)\n"
        "• Only safe for: non-security checksums\n\n"
        "Rule: Use SHA-256 or bcrypt for passwords. NEVER MD5."
    ),
    "cia": (
        "The CIA Triad — Core IS Framework\n\n"
        "C — Confidentiality\n"
        "  Protect data from unauthorized access.\n"
        "  Implemented via: SHA-256 hashing, encryption\n\n"
        "I — Integrity\n"
        "  Ensure data is not tampered with.\n"
        "  Implemented via: MD5 blockchain chaining\n\n"
        "A — Availability\n"
        "  Ensure authorized users can access the system.\n"
        "  Implemented via: session tokens, access control\n\n"
        "This project demonstrates ALL THREE principles."
    ),
}


# ══════════════════════════════════════════════════════════
#  HELPER WIDGETS
# ══════════════════════════════════════════════════════════
def styled_frame(parent, bg=None, **kw):
    return tk.Frame(parent, bg=bg or C["bg"], **kw)


def styled_label(parent, text, font=None, fg=None, bg=None, **kw):
    return tk.Label(
        parent, text=text,
        font=font or FONTS["body"],
        fg=fg or C["text"],
        bg=bg or C["bg"],
        **kw
    )


def styled_button(parent, text, command, color=None, fg=None, width=18):
    btn = tk.Button(
        parent, text=text, command=command,
        font=FONTS["btn"],
        bg=color or C["accent"],
        fg=fg or C["bg"],
        activebackground=C["accent2"],
        activeforeground=C["bg"],
        relief="flat", bd=0,
        padx=12, pady=6,
        width=width, cursor="hand2",
    )
    return btn


def separator(parent, color=None):
    return tk.Frame(parent, bg=color or C["border"], height=1)


def section_header(parent, title, subtitle=""):
    f = styled_frame(parent, bg=C["bg2"])
    f.pack(fill="x", padx=0, pady=(0, 2))
    styled_label(f, title, font=FONTS["heading"],
                 fg=C["accent"], bg=C["bg2"]).pack(anchor="w", padx=14, pady=(10, 0))
    if subtitle:
        styled_label(f, subtitle, font=FONTS["small"],
                     fg=C["text2"], bg=C["bg2"]).pack(anchor="w", padx=14, pady=(0, 8))
    separator(f, C["border"]).pack(fill="x")
    return f


# ══════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Amazon AI + Information Security System v2.0")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(bg=C["bg"])
        self.resizable(True, True)

        add_block("SYSTEM_INIT | Amazon AI+IS System v2.0 started")
        add_log("SYSTEM STARTED", "INFO")

        self._build_login()

    # ── LOGIN ───────────────────────────────────────────
    def _build_login(self):
        self.login_frame = styled_frame(self, bg=C["bg"])
        self.login_frame.place(relx=.5, rely=.5, anchor="center")

        # card
        card = styled_frame(self.login_frame, bg=C["card"])
        card.pack(padx=20, pady=20)

        tk.Frame(card, bg=C["accent"], height=3).pack(fill="x")

        inner = styled_frame(card, bg=C["card"])
        inner.pack(padx=40, pady=30)

        styled_label(inner, "🔐  SECURE ACCESS PORTAL",
                     font=("Courier New", 16, "bold"),
                     fg=C["accent"], bg=C["card"]).pack(pady=(0, 4))
        styled_label(inner, "Amazon AI + Information Security System v2.0",
                     font=FONTS["small"], fg=C["text2"], bg=C["card"]).pack(pady=(0, 24))

        for label, attr, show in [("Username", "e_user", ""), ("Password", "e_pass", "*")]:
            styled_label(inner, label, font=("Segoe UI", 9, "bold"),
                         fg=C["text2"], bg=C["card"]).pack(anchor="w")
            e = tk.Entry(inner, show=show, font=FONTS["body"],
                         bg=C["bg3"], fg=C["text"],
                         insertbackground=C["accent"],
                         relief="flat", bd=0, width=28)
            e.pack(pady=(2, 12), ipady=6)
            setattr(self, attr, e)

        self.e_user.insert(0, "admin")
        self.e_pass.insert(0, "1234")
        self.e_pass.bind("<Return>", lambda _: self._do_login())

        styled_button(inner, "  Authenticate  →", self._do_login,
                      color=C["accent"], width=24).pack(pady=(4, 0))

        self.login_err = styled_label(inner, "", font=FONTS["small"],
                                      fg=C["red"], bg=C["card"])
        self.login_err.pack(pady=(8, 0))

        styled_label(inner, "Default:  admin  /  1234   |   SHA-256 encrypted",
                     font=FONTS["small"], fg=C["text3"], bg=C["card"]).pack(pady=(12, 0))

    def _do_login(self):
        global current_user, session_key
        u = self.e_user.get().strip()
        p = sha256(self.e_pass.get())
        if u in USERS and USERS[u] == p:
            current_user = u
            session_key  = md5hash(u + str(time.time()))
            add_log(f"LOGIN SUCCESS | user:{u} | session:{session_key[:10]}...", "SUCCESS")
            add_block(f"LOGIN | user:{u} | session:{session_key[:10]}")
            self.login_frame.destroy()
            self._build_main()
        else:
            add_log(f"LOGIN FAIL | user:{u}", "ERROR")
            self.login_err.config(text="✗  Invalid credentials. Access denied.")

    # ── MAIN LAYOUT ─────────────────────────────────────
    def _build_main(self):
        # header
        hdr = styled_frame(self, bg=C["bg2"])
        hdr.pack(fill="x")
        tk.Frame(hdr, bg=C["accent"], height=2).pack(fill="x")
        hdr_inner = styled_frame(hdr, bg=C["bg2"])
        hdr_inner.pack(fill="x", padx=16, pady=8)
        styled_label(hdr_inner, "🤖  AMAZON  AI + IS  SYSTEM",
                     font=("Courier New", 13, "bold"),
                     fg=C["accent"], bg=C["bg2"]).pack(side="left")
        self.clock_lbl = styled_label(hdr_inner, "", font=FONTS["mono"],
                                      fg=C["text2"], bg=C["bg2"])
        self.clock_lbl.pack(side="right")
        styled_label(hdr_inner, f"● {current_user.upper()}",
                     font=FONTS["mono"], fg=C["green"], bg=C["bg2"]).pack(side="right", padx=16)
        self._tick()

        # body: sidebar + notebook
        body = styled_frame(self, bg=C["bg"])
        body.pack(fill="both", expand=True)

        sidebar = self._build_sidebar(body)
        sidebar.pack(side="left", fill="y")
        tk.Frame(body, bg=C["border"], width=1).pack(side="left", fill="y")

        self.nb = ttk.Notebook(body)
        self._style_notebook()
        self.nb.pack(side="left", fill="both", expand=True)

        # tabs
        self.tabs = {}
        for name, builder in [
            ("Dashboard",    self._tab_dashboard),
            ("AI Recommender", self._tab_recommender),
            ("AI Research",  self._tab_research),
            ("IS Security",  self._tab_security),
            ("Blockchain",   self._tab_blockchain),
        ]:
            f = styled_frame(self.nb, bg=C["bg"])
            builder(f)
            self.nb.add(f, text=f"  {name}  ")
            self.tabs[name] = f

    def _style_notebook(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",
                        background=C["bg2"], borderwidth=0, tabmargins=[0, 4, 0, 0])
        style.configure("TNotebook.Tab",
                        background=C["bg2"], foreground=C["text2"],
                        font=("Segoe UI", 10), padding=[14, 6])
        style.map("TNotebook.Tab",
                  background=[("selected", C["bg"])],
                  foreground=[("selected", C["accent"])])

    def _build_sidebar(self, parent):
        sb = styled_frame(parent, bg=C["bg2"], width=180)
        sb.pack_propagate(False)

        styled_label(sb, "NAVIGATION", font=("Segoe UI", 8, "bold"),
                     fg=C["text3"], bg=C["bg2"]).pack(anchor="w", padx=14, pady=(16, 4))

        menu = [
            ("📊", "Dashboard"),
            ("🤖", "AI Recommender"),
            ("🔬", "AI Research"),
            ("🔐", "IS Security"),
            ("⛓️",  "Blockchain"),
        ]
        for icon, name in menu:
            btn = tk.Button(sb, text=f"  {icon}  {name}", anchor="w",
                            font=FONTS["small"],
                            bg=C["bg2"], fg=C["text2"],
                            activebackground=C["bg3"],
                            activeforeground=C["accent"],
                            relief="flat", bd=0, padx=8, pady=7,
                            cursor="hand2",
                            command=lambda n=name: self._goto_tab(n))
            btn.pack(fill="x", padx=6)

        separator(sb, C["border"]).pack(fill="x", padx=10, pady=12)

        # stats mini
        self.sb_stat_lbl = styled_label(sb, "", font=FONTS["mono_s"],
                                        fg=C["text2"], bg=C["bg2"],
                                        justify="left")
        self.sb_stat_lbl.pack(anchor="w", padx=14)
        self._refresh_sb_stats()

        separator(sb, C["border"]).pack(fill="x", padx=10, pady=12)

        styled_button(sb, "  Logout", self._logout,
                      color=C["red"], fg=C["white"], width=14).pack(padx=14, pady=4)
        return sb

    def _refresh_sb_stats(self):
        self.sb_stat_lbl.config(text=(
            f"Products : {len(products_data)}\n"
            f"Searches : {search_count}\n"
            f"Log events: {len(security_log)}\n"
            f"Blocks   : {len(blockchain)}"
        ))
        self.after(2000, self._refresh_sb_stats)

    def _goto_tab(self, name):
        for i, (n, _) in enumerate([
            ("Dashboard", None), ("AI Recommender", None),
            ("AI Research", None), ("IS Security", None), ("Blockchain", None)
        ]):
            if n == name:
                self.nb.select(i)
                return

    def _tick(self):
        self.clock_lbl.config(text=time.strftime("  %Y-%m-%d  %H:%M:%S  "))
        self.after(1000, self._tick)

    def _logout(self):
        add_log(f"LOGOUT | user:{current_user}", "WARNING")
        self.destroy()
        App().mainloop()

    # ══════════════════════════════════════════════════
    #  TAB — DASHBOARD
    # ══════════════════════════════════════════════════
    def _tab_dashboard(self, parent):
        section_header(parent,
                       "System Dashboard",
                       "Real-time AI + Information Security Overview")

        scroll = tk.Canvas(parent, bg=C["bg"], highlightthickness=0)
        scroll.pack(fill="both", expand=True, padx=0, pady=0)
        vsb = tk.Scrollbar(parent, orient="vertical", command=scroll.yview)
        scroll.configure(yscrollcommand=vsb.set)

        inner = styled_frame(scroll, bg=C["bg"])
        scroll.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: scroll.configure(
            scrollregion=scroll.bbox("all")))

        # stat cards
        stats_f = styled_frame(inner, bg=C["bg"])
        stats_f.pack(fill="x", padx=16, pady=16)
        stats = [
            ("Products Loaded",  "0",  C["accent"],  "TF-IDF indexed",    "stat_prod"),
            ("Searches Run",     "0",  C["green"],   "Cosine similarity", "stat_srch"),
            ("Security Events",  "1",  C["amber"],   "Logged & hashed",   "stat_evts"),
            ("Blockchain Blocks","1",  C["purple"],  "Immutable ledger",  "stat_blks"),
        ]
        self.stat_labels = {}
        for col, (title, val, color, sub, key) in enumerate(stats):
            card = tk.Frame(stats_f, bg=C["card"],
                            highlightbackground=C["border"],
                            highlightthickness=1)
            card.grid(row=0, column=col, padx=6, pady=0, sticky="nsew")
            stats_f.columnconfigure(col, weight=1)
            tk.Frame(card, bg=color, height=2).pack(fill="x")
            styled_label(card, title, font=("Segoe UI", 9),
                         fg=C["text2"], bg=C["card"]).pack(anchor="w", padx=12, pady=(10, 0))
            lbl = styled_label(card, val, font=("Courier New", 22, "bold"),
                               fg=color, bg=C["card"])
            lbl.pack(anchor="w", padx=12)
            styled_label(card, sub, font=FONTS["small"],
                         fg=C["text3"], bg=C["card"]).pack(anchor="w", padx=12, pady=(0, 10))
            self.stat_labels[key] = lbl

        self._update_dash_stats()

        # architecture
        arch_f = styled_frame(inner, bg=C["bg"])
        arch_f.pack(fill="x", padx=16, pady=(8, 4))

        left = tk.Frame(arch_f, bg=C["card"],
                        highlightbackground=C["border"], highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))
        tk.Frame(left, bg=C["accent"], height=2).pack(fill="x")
        styled_label(left, "System Architecture",
                     font=FONTS["heading"], fg=C["accent"], bg=C["card"]).pack(
                         anchor="w", padx=12, pady=(8, 4))
        archs = [
            ("🧠", "NLP Engine",    "TF-IDF Vectorizer"),
            ("📐", "Similarity",    "Cosine Similarity Matrix"),
            ("🔒", "Auth",          "SHA-256 Password Hash"),
            ("⛓️",  "Integrity",    "MD5 Blockchain Chain"),
            ("📋", "Audit",         "Append-only Security Log"),
        ]
        for icon, name, detail in archs:
            row = styled_frame(left, bg=C["card"])
            row.pack(fill="x", padx=12, pady=2)
            styled_label(row, f"{icon} ", font=FONTS["body"],
                         fg=C["text"], bg=C["card"]).pack(side="left")
            styled_label(row, f"{name}: ", font=("Segoe UI", 10, "bold"),
                         fg=C["text"], bg=C["card"]).pack(side="left")
            styled_label(row, detail, font=FONTS["small"],
                         fg=C["text2"], bg=C["card"]).pack(side="left")

        # threat
        right = tk.Frame(arch_f, bg=C["card"],
                         highlightbackground=C["border"], highlightthickness=1)
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))
        tk.Frame(right, bg=C["accent"], height=2).pack(fill="x")
        styled_label(right, "Threat Level Monitor",
                     font=FONTS["heading"], fg=C["accent"], bg=C["card"]).pack(
                         anchor="w", padx=12, pady=(8, 4))
        threats = [
            ("Brute Force Risk", 12,  C["green"]),
            ("Data Integrity",   95,  C["green"]),
            ("Session Health",   88,  C["accent"]),
            ("Audit Trail",      100, C["green"]),
        ]
        for label, pct, color in threats:
            tf = styled_frame(right, bg=C["card"])
            tf.pack(fill="x", padx=12, pady=4)
            row = styled_frame(tf, bg=C["card"])
            row.pack(fill="x")
            styled_label(row, label, font=FONTS["small"],
                         fg=C["text2"], bg=C["card"]).pack(side="left")
            pval = "Secure" if pct >= 90 else ("Active" if pct >= 70 else "Low")
            styled_label(row, pval, font=FONTS["small"],
                         fg=color, bg=C["card"]).pack(side="right")
            bar_bg = tk.Frame(tf, bg=C["bg3"], height=6)
            bar_bg.pack(fill="x")
            tk.Frame(bar_bg, bg=color, height=6,
                     width=int(bar_bg.winfo_reqwidth() * pct / 100)).pack(side="left")

        # quick actions
        qa = tk.Frame(inner, bg=C["card"],
                      highlightbackground=C["border"], highlightthickness=1)
        qa.pack(fill="x", padx=16, pady=(8, 16))
        tk.Frame(qa, bg=C["accent"], height=2).pack(fill="x")
        styled_label(qa, "Quick Actions",
                     font=FONTS["heading"], fg=C["accent"], bg=C["card"]).pack(
                         anchor="w", padx=12, pady=(8, 6))
        btn_row = styled_frame(qa, bg=C["card"])
        btn_row.pack(fill="x", padx=12, pady=(0, 12))
        for text, tab in [
            ("🤖 AI Recommender", "AI Recommender"),
            ("🔬 Research",       "AI Research"),
            ("🔐 IS Security",    "IS Security"),
            ("⛓️ Blockchain",     "Blockchain"),
        ]:
            styled_button(btn_row, text, lambda t=tab: self._goto_tab(t),
                          color=C["bg3"], fg=C["accent"], width=16).pack(side="left", padx=4)

    def _update_dash_stats(self):
        if hasattr(self, "stat_labels"):
            self.stat_labels["stat_prod"].config(text=str(len(products_data)))
            self.stat_labels["stat_srch"].config(text=str(search_count))
            self.stat_labels["stat_evts"].config(text=str(len(security_log)))
            self.stat_labels["stat_blks"].config(text=str(len(blockchain)))
        self.after(2000, self._update_dash_stats)

    # ══════════════════════════════════════════════════
    #  TAB — AI RECOMMENDER
    # ══════════════════════════════════════════════════
    def _tab_recommender(self, parent):
        section_header(parent,
                       "AI Product Recommender",
                       "TF-IDF Vectorization + Cosine Similarity Engine")

        body = styled_frame(parent, bg=C["bg"])
        body.pack(fill="both", expand=True, padx=16, pady=12)

        # load buttons
        btn_f = styled_frame(body, bg=C["bg"])
        btn_f.pack(fill="x", pady=(0, 12))
        styled_button(btn_f, "📂 Load CSV File", self._load_csv,
                      color=C["bg3"], fg=C["accent"]).pack(side="left", padx=(0, 8))
        styled_button(btn_f, "⚡ Load Demo (50 Products)", self._load_demo,
                      color=C["accent"]).pack(side="left")
        self.rec_status = styled_label(btn_f, "No data loaded",
                                       font=FONTS["small"], fg=C["text3"], bg=C["bg"])
        self.rec_status.pack(side="left", padx=16)

        separator(body, C["border"]).pack(fill="x", pady=8)

        # search
        styled_label(body, "Search  →  Find Similar Products",
                     font=FONTS["heading"], fg=C["accent"], bg=C["bg"]).pack(anchor="w")
        styled_label(body, "Enter any product name to find the 5 most similar items",
                     font=FONTS["small"], fg=C["text2"], bg=C["bg"]).pack(anchor="w", pady=(2, 8))

        sf = styled_frame(body, bg=C["bg"])
        sf.pack(fill="x", pady=(0, 8))
        self.search_var = tk.StringVar()
        tk.Entry(sf, textvariable=self.search_var,
                 font=FONTS["body"],
                 bg=C["bg3"], fg=C["text"],
                 insertbackground=C["accent"],
                 relief="flat", bd=0, width=45).pack(side="left", ipady=7, padx=(0, 8))
        styled_button(sf, "🔍 Search", self._do_search).pack(side="left")
        self.search_var.trace_add("write", lambda *_: None)

        # results
        res_frame = tk.Frame(body, bg=C["card"],
                             highlightbackground=C["border"], highlightthickness=1)
        res_frame.pack(fill="both", expand=True, pady=(4, 0))
        tk.Frame(res_frame, bg=C["accent"], height=2).pack(fill="x")

        self.res_header = styled_label(res_frame, "Results will appear here",
                                       font=FONTS["small"], fg=C["text2"], bg=C["card"])
        self.res_header.pack(anchor="w", padx=12, pady=(8, 4))

        self.res_list = tk.Frame(res_frame, bg=C["card"])
        self.res_list.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def _load_demo(self):
        global products_data, sim_matrix
        products_data = [{"name": n, "description": d} for n, d in DEMO_PRODUCTS]
        self._compute_tfidf()
        add_log(f"DEMO DATASET LOADED | {len(products_data)} products", "INFO")
        add_block(f"DEMO_DATA | {len(products_data)} products loaded")
        self.rec_status.config(
            text=f"✓ {len(products_data)} products loaded & vectorized",
            fg=C["green"])
        messagebox.showinfo("Dataset Loaded",
                            f"Demo dataset loaded!\n{len(products_data)} Amazon-style products\nTF-IDF matrix computed.")

    def _load_csv(self):
        global products_data, sim_matrix
        if not PANDAS_OK:
            messagebox.showerror("Missing Library",
                                 "pandas not installed.\nRun: pip install pandas")
            return
        path = filedialog.askopenfilename(
            title="Select CSV", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        try:
            df = pd.read_csv(path)
            if "name" not in df.columns:
                messagebox.showerror("Error", "CSV must have a 'name' column")
                return
            if "description" not in df.columns:
                df["description"] = df["name"]
            products_data = df[["name", "description"]].dropna(
                subset=["name"]).to_dict("records")
            self._compute_tfidf()
            add_log(f"CSV LOADED | {path} | {len(products_data)} rows", "INFO")
            add_block(f"CSV_LOAD | {os.path.basename(path)} | {len(products_data)} rows")
            self.rec_status.config(
                text=f"✓ {len(products_data)} products from {os.path.basename(path)}",
                fg=C["green"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _compute_tfidf(self):
        global sim_matrix
        if not SKLEARN_OK:
            return
        docs = [p.get("description", p["name"]) for p in products_data]
        tf = TfidfVectorizer()
        sim_matrix = cosine_similarity(tf.fit_transform(docs))

    def _do_search(self):
        global search_count
        if not products_data:
            messagebox.showwarning("No Data", "Load a dataset first!")
            return
        q = self.search_var.get().lower().strip()
        if not q:
            return
        names = [p["name"].lower() for p in products_data]
        matches = [i for i, n in enumerate(names) if q in n]
        if not matches:
            messagebox.showinfo("Not Found",
                                f"'{q}' not found in dataset.\nTry a different search term.")
            return
        idx = matches[0]

        # clear old results
        for w in self.res_list.winfo_children():
            w.destroy()

        if sim_matrix is not None and SKLEARN_OK:
            scores = sorted(enumerate(sim_matrix[idx]),
                            key=lambda x: x[1], reverse=True)
            recs = [(products_data[i]["name"], s)
                    for i, s in scores if i != idx][:5]
        else:
            # fallback: keyword match
            q_words = set(products_data[idx].get("description", "").split())
            scored = []
            for i, p in enumerate(products_data):
                if i == idx:
                    continue
                w = set(p.get("description", "").split())
                scored.append((p["name"], len(q_words & w) / max(len(q_words | w), 1)))
            recs = sorted(scored, key=lambda x: x[1], reverse=True)[:5]

        matched = products_data[idx]["name"]
        self.res_header.config(
            text=f"Top 5 recommendations for: '{matched}'",
            fg=C["accent"])

        for rank, (name, score) in enumerate(recs, 1):
            row = styled_frame(self.res_list, bg=C["bg3"])
            row.pack(fill="x", pady=3)
            tk.Frame(row, bg=C["accent"], width=3).pack(side="left", fill="y")

            styled_label(row, f"#{rank}", font=FONTS["mono"],
                         fg=C["text3"], bg=C["bg3"]).pack(side="left", padx=(10, 6))
            styled_label(row, name, font=("Segoe UI", 11),
                         fg=C["text"], bg=C["bg3"]).pack(side="left", fill="x", expand=True)
            pct = f"{score*100:.1f}%"
            styled_label(row, pct, font=FONTS["mono"],
                         fg=C["accent"], bg=C["bg3"]).pack(side="right", padx=10)

            # bar
            bar_bg = tk.Frame(row, bg=C["bg"], height=4, width=120)
            bar_bg.pack(side="right", padx=(0, 8))
            bar_bg.pack_propagate(False)
            tk.Frame(bar_bg, bg=C["accent"],
                     width=int(120 * score), height=4).pack(side="left")

        search_count += 1
        add_log(f'SEARCH | query:"{q}" | match:"{matched}" | results:5', "INFO")

    # ══════════════════════════════════════════════════
    #  TAB — AI RESEARCH
    # ══════════════════════════════════════════════════
    def _tab_research(self, parent):
        section_header(parent,
                       "AI Advancements Research",
                       "History of AI + Information Security Technology")

        # paned: left=timelines, right=Q&A
        pane = tk.PanedWindow(parent, orient="horizontal",
                              bg=C["bg"], sashwidth=4,
                              sashrelief="flat")
        pane.pack(fill="both", expand=True, padx=12, pady=8)

        # LEFT — timelines
        left_frame = styled_frame(pane, bg=C["bg"])
        pane.add(left_frame, minsize=380)

        nb2 = ttk.Notebook(left_frame)
        nb2.pack(fill="both", expand=True)

        for tab_title, timeline in [
            ("AI Timeline", AI_TIMELINE),
            ("IS Timeline", IS_TIMELINE),
        ]:
            tf = styled_frame(nb2, bg=C["bg"])
            nb2.add(tf, text=f"  {tab_title}  ")
            canvas = tk.Canvas(tf, bg=C["bg"], highlightthickness=0)
            canvas.pack(side="left", fill="both", expand=True)
            sb2 = tk.Scrollbar(tf, orient="vertical", command=canvas.yview)
            sb2.pack(side="right", fill="y")
            canvas.configure(yscrollcommand=sb2.set)
            inner2 = styled_frame(canvas, bg=C["bg"])
            canvas.create_window((0, 0), window=inner2, anchor="nw")
            inner2.bind("<Configure>", lambda e, c=canvas: c.configure(
                scrollregion=c.bbox("all")))
            for year, title, desc in timeline:
                row = styled_frame(inner2, bg=C["bg"])
                row.pack(fill="x", padx=14, pady=4)
                # dot + line
                dot_f = styled_frame(row, bg=C["bg"])
                dot_f.pack(side="left")
                tk.Canvas(dot_f, width=18, height=18,
                           bg=C["bg"], highlightthickness=0).pack()
                txt_f = styled_frame(row, bg=C["card"])
                txt_f.pack(side="left", fill="x", expand=True)
                tk.Frame(txt_f, bg=C["accent"], height=1).pack(fill="x")
                r2 = styled_frame(txt_f, bg=C["card"])
                r2.pack(fill="x", padx=10, pady=4)
                styled_label(r2, year, font=FONTS["mono"],
                             fg=C["accent"], bg=C["card"]).pack(side="left")
                styled_label(r2, f"  {title}", font=("Segoe UI", 10, "bold"),
                             fg=C["text"], bg=C["card"]).pack(side="left")
                styled_label(txt_f, desc, font=FONTS["small"],
                             fg=C["text2"], bg=C["card"],
                             wraplength=320, justify="left").pack(
                                 anchor="w", padx=10, pady=(0, 6))

        # RIGHT — Q&A
        right_frame = styled_frame(pane, bg=C["bg"])
        pane.add(right_frame, minsize=320)

        styled_label(right_frame, "🔬  AI Research Assistant",
                     font=FONTS["heading"], fg=C["accent"], bg=C["bg"]).pack(
                         anchor="w", padx=8, pady=(0, 4))
        styled_label(right_frame, "Click a topic or type your own question",
                     font=FONTS["small"], fg=C["text2"], bg=C["bg"]).pack(
                         anchor="w", padx=8, pady=(0, 8))

        topics = [
            ("TF-IDF Explained",  "tfidf",      "Explain TF-IDF and cosine similarity in simple terms"),
            ("Blockchain + IS",   "blockchain",  "How does blockchain ensure data integrity in IS systems?"),
            ("SHA-256 vs MD5",    "sha",         "Compare SHA-256 vs MD5 for security applications"),
            ("CIA Triad",         "cia",         "Explain the CIA Triad with examples from this system"),
        ]

        pill_row = styled_frame(right_frame, bg=C["bg"])
        pill_row.pack(fill="x", padx=8, pady=(0, 8))
        for label, key, question in topics:
            tk.Button(pill_row,
                      text=label,
                      font=FONTS["small"],
                      bg=C["bg3"], fg=C["accent"],
                      activebackground=C["border"],
                      activeforeground=C["accent2"],
                      relief="flat", bd=0, padx=10, pady=4,
                      cursor="hand2",
                      command=lambda k=key, q=question: self._show_research(k, q)
                      ).pack(side="left", padx=2, pady=2)

        qf = styled_frame(right_frame, bg=C["bg"])
        qf.pack(fill="x", padx=8, pady=(0, 8))
        self.research_var = tk.StringVar()
        tk.Entry(qf, textvariable=self.research_var,
                 font=FONTS["body"],
                 bg=C["bg3"], fg=C["text"],
                 insertbackground=C["accent"],
                 relief="flat", bd=0).pack(side="left", fill="x", expand=True, ipady=6)
        styled_button(qf, "Ask",
                      lambda: self._show_research(None, self.research_var.get()),
                      width=6).pack(side="left", padx=(6, 0))

        self.research_out = scrolledtext.ScrolledText(
            right_frame, font=FONTS["mono_s"],
            bg=C["bg3"], fg=C["text"],
            insertbackground=C["accent"],
            relief="flat", bd=0,
            wrap="word", state="disabled")
        self.research_out.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def _show_research(self, key, question):
        text = ""
        if key and key in RESEARCH_CACHE:
            text = RESEARCH_CACHE[key]
        else:
            # try requests for live answer
            if REQUESTS_OK and question:
                text = self._ask_ai(question)
            else:
                # auto-detect from question
                q_low = (question or "").lower()
                if "tfidf" in q_low or "cosine" in q_low or "tf" in q_low:
                    text = RESEARCH_CACHE["tfidf"]
                elif "blockchain" in q_low:
                    text = RESEARCH_CACHE["blockchain"]
                elif "sha" in q_low or "md5" in q_low:
                    text = RESEARCH_CACHE["sha"]
                elif "cia" in q_low:
                    text = RESEARCH_CACHE["cia"]
                else:
                    text = (
                        "This system implements these IS concepts:\n\n"
                        "1. TF-IDF vectorization for AI recommendations\n"
                        "2. Cosine similarity for semantic matching\n"
                        "3. SHA-256 for password confidentiality\n"
                        "4. MD5 blockchain chaining for data integrity\n"
                        "5. Session tokens for authentication\n"
                        "6. Append-only audit logs for non-repudiation\n\n"
                        "Together these cover the full CIA Triad:\n"
                        "Confidentiality · Integrity · Availability"
                    )

        self.research_out.config(state="normal")
        self.research_out.delete("1.0", "end")
        self.research_out.insert("1.0", text)
        self.research_out.config(state="disabled")
        add_log(f'RESEARCH QUERY | "{(question or key or "")[:40]}..."', "INFO")

    def _ask_ai(self, question):
        try:
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 500,
                    "system": (
                        "You are an expert in AI advancements and Information Security. "
                        "Give concise, educational answers in 150-200 words. "
                        "Use plain text with bullet points. No markdown formatting."
                    ),
                    "messages": [{"role": "user", "content": question}],
                },
                headers={"Content-Type": "application/json"},
                timeout=15,
            )
            data = resp.json()
            for block in data.get("content", []):
                if block.get("type") == "text":
                    return block["text"]
        except Exception as e:
            pass
        return f"(AI API unavailable — showing cached answer)\n\n{RESEARCH_CACHE.get('cia', '')}"

    # ══════════════════════════════════════════════════
    #  TAB — IS SECURITY
    # ══════════════════════════════════════════════════
    def _tab_security(self, parent):
        section_header(parent,
                       "Information Security Dashboard",
                       "Session Management · Audit Logs · CIA Triad · Cryptography")

        canvas = tk.Canvas(parent, bg=C["bg"], highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        vsb = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        vsb.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=vsb.set)
        inner = styled_frame(canvas, bg=C["bg"])
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        # session + hash
        top = styled_frame(inner, bg=C["bg"])
        top.pack(fill="x", padx=16, pady=10)

        sess = tk.Frame(top, bg=C["card"],
                        highlightbackground=C["border"], highlightthickness=1)
        sess.pack(side="left", fill="both", expand=True, padx=(0, 6))
        tk.Frame(sess, bg=C["green"], height=2).pack(fill="x")
        styled_label(sess, "🔑  Active Session",
                     font=FONTS["heading"], fg=C["green"], bg=C["card"]).pack(
                         anchor="w", padx=12, pady=(8, 4))
        for label, val in [
            ("Session Token (MD5):", session_key or "—"),
            ("Authenticated User:", f"{current_user} ✓" if current_user else "—"),
            ("Login Time:", now_str()),
        ]:
            rf = styled_frame(sess, bg=C["card"])
            rf.pack(fill="x", padx=12, pady=2)
            styled_label(rf, label, font=("Segoe UI", 9),
                         fg=C["text2"], bg=C["card"]).pack(anchor="w")
            styled_label(rf, val, font=FONTS["mono_s"],
                         fg=C["accent2"], bg=C["card"],
                         wraplength=300, justify="left").pack(anchor="w")

        pw = tk.Frame(top, bg=C["card"],
                      highlightbackground=C["border"], highlightthickness=1)
        pw.pack(side="left", fill="both", expand=True, padx=(6, 0))
        tk.Frame(pw, bg=C["accent"], height=2).pack(fill="x")
        styled_label(pw, "🔒  Password Security (SHA-256)",
                     font=FONTS["heading"], fg=C["accent"], bg=C["card"]).pack(
                         anchor="w", padx=12, pady=(8, 4))
        styled_label(pw, "Stored hash of 'admin':",
                     font=FONTS["small"], fg=C["text2"], bg=C["card"]).pack(
                         anchor="w", padx=12)
        pw_hash = sha256("1234")
        styled_label(pw, pw_hash[:32] + "\n" + pw_hash[32:],
                     font=FONTS["mono_s"], fg=C["accent2"], bg=C["card"],
                     wraplength=300, justify="left").pack(
                         anchor="w", padx=12, pady=(2, 4))
        styled_label(pw, "Algorithm: SHA-256 · 256-bit · One-way · Collision-resistant",
                     font=FONTS["small"], fg=C["text2"], bg=C["card"]).pack(
                         anchor="w", padx=12, pady=(0, 10))

        # CIA Triad
        cia = tk.Frame(inner, bg=C["card"],
                       highlightbackground=C["border"], highlightthickness=1)
        cia.pack(fill="x", padx=16, pady=4)
        tk.Frame(cia, bg=C["purple"], height=2).pack(fill="x")
        styled_label(cia, "🛡️  IS Concepts Implemented (CIA Triad & Beyond)",
                     font=FONTS["heading"], fg=C["purple"], bg=C["card"]).pack(
                         anchor="w", padx=12, pady=(8, 8))
        grid = styled_frame(cia, bg=C["card"])
        grid.pack(fill="x", padx=12, pady=(0, 12))
        for i, (concept, color, detail) in enumerate(IS_CONCEPTS):
            cell = styled_frame(grid, bg=C["bg3"])
            cell.grid(row=i//3, column=i%3, padx=4, pady=4, sticky="nsew")
            grid.columnconfigure(i%3, weight=1)
            tk.Frame(cell, bg=color, width=3).pack(side="left", fill="y")
            cf = styled_frame(cell, bg=C["bg3"])
            cf.pack(fill="both", expand=True, padx=8, pady=6)
            styled_label(cf, concept, font=("Segoe UI", 10, "bold"),
                         fg=color, bg=C["bg3"]).pack(anchor="w")
            styled_label(cf, detail, font=FONTS["small"],
                         fg=C["text2"], bg=C["bg3"],
                         wraplength=200, justify="left").pack(anchor="w")

        # audit log
        log_card = tk.Frame(inner, bg=C["card"],
                            highlightbackground=C["border"], highlightthickness=1)
        log_card.pack(fill="x", padx=16, pady=(4, 16))
        tk.Frame(log_card, bg=C["amber"], height=2).pack(fill="x")
        lh = styled_frame(log_card, bg=C["card"])
        lh.pack(fill="x", padx=12, pady=(8, 4))
        styled_label(lh, "📋  Security Audit Log",
                     font=FONTS["heading"], fg=C["amber"], bg=C["card"]).pack(side="left")
        styled_button(lh, "+ Simulate Event", self._sim_event,
                      color=C["bg3"], fg=C["amber"], width=16).pack(side="right")

        self.log_text = tk.Text(log_card, font=FONTS["mono_s"],
                                bg=C["bg3"], fg=C["text"],
                                relief="flat", bd=0, height=10,
                                state="disabled")
        self.log_text.pack(fill="x", padx=12, pady=(0, 12))
        self.log_text.tag_config("SUCCESS", foreground=C["green"])
        self.log_text.tag_config("ERROR",   foreground=C["red"])
        self.log_text.tag_config("WARNING", foreground=C["amber"])
        self.log_text.tag_config("INFO",    foreground=C["accent"])
        self._refresh_log()

    def _refresh_log(self):
        if hasattr(self, "log_text"):
            self.log_text.config(state="normal")
            self.log_text.delete("1.0", "end")
            for ts, event, level in reversed(security_log):
                self.log_text.insert("end", f"[{ts}]  ", "INFO")
                self.log_text.insert("end", f"{event}\n", level)
            self.log_text.config(state="disabled")
        self.after(2000, self._refresh_log)

    def _sim_event(self):
        import random
        events = [
            ("PORT SCAN DETECTED | ip:192.168.1.105 | blocked", "WARNING"),
            ("FAILED LOGIN | user:attacker | attempts:3",       "ERROR"),
            ("FILE ACCESS | path:/data/products.csv | read",    "INFO"),
            ("SESSION REFRESH | token rotated",                  "SUCCESS"),
            ("DATA EXPORT | rows:50 | user:admin",              "WARNING"),
        ]
        ev, lvl = random.choice(events)
        add_log(ev, lvl)
        add_block(ev)

    # ══════════════════════════════════════════════════
    #  TAB — BLOCKCHAIN
    # ══════════════════════════════════════════════════
    def _tab_blockchain(self, parent):
        section_header(parent,
                       "Blockchain Integrity Ledger",
                       "MD5-Chained tamper-evident data audit trail")

        top_f = styled_frame(parent, bg=C["bg"])
        top_f.pack(fill="x", padx=16, pady=8)
        styled_label(top_f,
                     "Each block = MD5(event_data + previous_hash)  "
                     "→  Changing any block breaks the chain",
                     font=FONTS["small"], fg=C["text2"], bg=C["bg"]).pack(side="left")
        styled_button(top_f, "+ Add Block", self._add_test_block,
                      color=C["bg3"], fg=C["accent"], width=12).pack(side="right")

        canvas = tk.Canvas(parent, bg=C["bg"], highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=16)
        vsb = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        vsb.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=vsb.set)
        self.chain_inner = styled_frame(canvas, bg=C["bg"])
        canvas.create_window((0, 0), window=self.chain_inner, anchor="nw")
        self.chain_inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        self._render_chain()

    def _render_chain(self):
        for w in self.chain_inner.winfo_children():
            w.destroy()
        for blk in reversed(blockchain):
            card = tk.Frame(self.chain_inner, bg=C["card"],
                            highlightbackground=C["border"], highlightthickness=1)
            card.pack(fill="x", pady=4)
            hdr = styled_frame(card, bg=C["card"])
            hdr.pack(fill="x", padx=12, pady=(8, 2))
            styled_label(hdr, f"Block #{blk['index']}",
                         font=("Courier New", 11, "bold"),
                         fg=C["amber"], bg=C["card"]).pack(side="left")
            styled_label(hdr, f"  {blk['timestamp']}",
                         font=FONTS["mono_s"], fg=C["text3"], bg=C["card"]).pack(side="left")
            styled_label(hdr, "✓ VALID",
                         font=FONTS["small"], fg=C["green"], bg=C["card"]).pack(side="right")

            styled_label(card, f"DATA:  {blk['data'][:70]}",
                         font=FONTS["mono_s"], fg=C["text"], bg=C["card"]).pack(
                             anchor="w", padx=12)
            styled_label(card, f"HASH:  {blk['hash']}",
                         font=FONTS["mono_s"], fg=C["accent2"], bg=C["card"]).pack(
                             anchor="w", padx=12)
            styled_label(card, f"PREV:  {blk['prev_hash']}",
                         font=FONTS["mono_s"], fg=C["text3"], bg=C["card"]).pack(
                             anchor="w", padx=12, pady=(0, 8))

    def _add_test_block(self):
        import random
        events = [
            "SEARCH | user:admin | query:laptop",
            "RECOMMENDATION | product:iPhone | results:5",
            "SECURITY_CHECK | integrity:OK",
            "USER_ACTION | tab:research | viewed",
            "DATA_VERIFY | hash:verified | status:clean",
        ]
        data = random.choice(events)
        add_block(data)
        add_log(f"BLOCK ADDED | #{len(blockchain)} | {data[:40]}", "INFO")
        self._render_chain()


# ══════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════
def check_dependencies():
    missing = []
    if not PANDAS_OK:
        missing.append("pandas")
    if not SKLEARN_OK:
        missing.append("scikit-learn")
    if missing:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning(
            "Optional Libraries Missing",
            f"Install for full features:\n\npip install {' '.join(missing)}\n\n"
            "The app will still run with the demo dataset."
        )
        root.destroy()


if __name__ == "__main__":
    check_dependencies()
    app = App()
    app.mainloop()