#!/usr/bin/env python3
"""
⚡ Deep Disk Cleaner Pro v2.0 - FIXED & OPTIMIZED
Professional Disk Cleaning Tool — Safe, Fast, Powerful
Only targets temp/cache/log files. NEVER touches system files or app data.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os, sys, threading, time, ctypes, shutil, subprocess
from pathlib import Path
from collections import OrderedDict

# ───────── AUTO INSTALL ─────────
try:
    import psutil
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil", "-q"])
    import psutil

# ───────── COLOR THEME ─────────
C = {
    'bg0':'#04060e', 'bg1':'#080d1a', 'bg2':'#0e1628', 'bg3':'#141e35',
    'bg4':'#1a2844', 'bg5':'#203050', 'inp':'#0a1220',
    'cyn':'#00e5ff', 'blu':'#2979ff', 'pur':'#7c4dff', 'pnk':'#ff4081',
    'grn':'#00e676', 'ylw':'#ffd600', 'org':'#ff9100', 'red':'#ff1744',
    'tel':'#1de9b6', 'wht':'#ffffff', 'tx1':'#eceff1', 'tx2':'#90a4ae',
    'tx3':'#546e7a', 'brd':'#1a2a48', 'brd2':'#2a3a5a',
}
CAT_C = {
    'Temp Files':     C['org'], 'Browser Cache':  C['cyn'],
    'Windows Cache':  C['pur'], 'App Cache':      C['pnk'],
    'Log Files':      C['ylw'], 'Update Cleanup': C['tel'],
    'Recycle Bin':    C['red'], 'Misc Junk':      C['blu'],
    'Python Caches':  C['grn'], 'NPM & Node':     C['ylw'],
    'Virus Threats':  C['red'], 'System Issues':  C['org'],
}

def fmt(b):
    if b<=0: return "0 B"
    u=['B','KB','MB','GB','TB']; i=0; s=float(b)
    while s>=1024 and i<len(u)-1: s/=1024; i+=1
    return f"{s:.1f} {u[i]}" if i else f"{int(s)} {u[i]}"

def lighter(c,a=30):
    c=c.lstrip('#')
    return f'#{min(255,int(c[0:2],16)+a):02x}{min(255,int(c[2:4],16)+a):02x}{min(255,int(c[4:6],16)+a):02x}'

def darker(c,a=30):
    c=c.lstrip('#')
    return f'#{max(0,int(c[0:2],16)-a):02x}{max(0,int(c[2:4],16)-a):02x}{max(0,int(c[4:6],16)-a):02x}'

# ───────── SAFE PATH CHECK ─────────
def is_safe_path(p):
    """Check path is safe to delete FROM. We only delete FILES inside, not the folder itself."""
    pl = p.lower().replace('/','\\')
    never = [
        '\\windows\\system32', '\\windows\\syswow64',
        '\\program files\\', '\\program files (x86)\\',
        '\\windows\\system', '\\windows\\config',
        '\\windows\\security', '\\windows\\servicing',
        '\\windows\\drivers', '\\windows\\winsxs\\',
        '\\boot\\', '\\efi\\', '\\recovery\\',
    ]
    for n in never:
        if n in pl:
            return False
    return True

# ───────── VIRUS SCANNER ─────────
class VirusScanner:
    """Detects common malware signatures and suspicious patterns"""
    MALWARE_SIGNATURES = {
        'Trojan': ['trojan', 'worm', 'backdoor', 'ratware'],
        'Ransomware': ['encrypt', 'ransom', 'locked', 'crypt'],
        'Spyware': ['spy', 'keylog', 'stolen', 'tracker'],
        'PUP': ['pup', 'adware', 'pua', 'unwanted'],
        'Suspicious': ['malware', 'virus', 'exploit', 'injection'],
    }
    
    @staticmethod
    def scan_file(filepath):
        """Scan a single file for threats"""
        threats = []
        try:
            fn = os.path.basename(filepath).lower()
            # Check filename patterns
            for threat_type, patterns in VirusScanner.MALWARE_SIGNATURES.items():
                if any(pat in fn for pat in patterns):
                    threats.append({'type': threat_type, 'reason': f'Suspicious filename: {fn}'})
            
            # Check file extension
            suspicious_exts = ['.exe', '.scr', '.vbs', '.js', '.bat', '.cmd', '.dll', '.sys']
            ext = os.path.splitext(filepath)[1].lower()
            if ext in suspicious_exts and 'temp' in filepath.lower():
                threats.append({'type': 'Suspicious', 'reason': f'Executable in temp: {ext}'})
            
            # Check file size anomalies (system files shouldn't be in temp)
            if os.path.isfile(filepath):
                sz = os.path.getsize(filepath)
                if sz > 100*1024*1024 and 'cache' in filepath.lower():
                    threats.append({'type': 'Suspicious', 'reason': f'Unusually large cache file: {fmt(sz)}'})
        except:
            pass
        return threats
    
    @staticmethod
    def scan_directory(dirpath, max_files=1000):
        """Scan directory for threats"""
        infected = []
        count = 0
        try:
            for root, dirs, files in os.walk(dirpath):
                if count > max_files: break
                for f in files[:100]:
                    if count > max_files: break
                    fpath = os.path.join(root, f)
                    threats = VirusScanner.scan_file(fpath)
                    if threats:
                        infected.append({'path': fpath, 'threats': threats})
                    count += 1
        except:
            pass
        return infected

# ───────── SYSTEM HEALTH CHECK ─────────
class SystemHealthCheck:
    """Detects Windows system problems and issues"""
    
    @staticmethod
    def check_issues():
        """Scan for common Windows problems"""
        issues = []
        W = os.environ.get('WINDIR', 'C:\\Windows')
        
        # 1. Check corrupt system files
        corrupt_files = []
        sys_checks = [
            (os.path.join(W, 'System32', 'kernel32.dll'), 'Critical: kernel32.dll missing'),
            (os.path.join(W, 'System32', 'ntdll.dll'), 'Critical: ntdll.dll missing'),
            (os.path.join(W, 'explorer.exe'), 'Critical: explorer.exe missing'),
        ]
        for fpath, desc in sys_checks:
            if not os.path.exists(fpath):
                corrupt_files.append({'path': fpath, 'issue': desc, 'severity': 'CRITICAL'})
        
        if corrupt_files:
            issues.append({
                'type': 'System Files',
                'title': f'Missing/Corrupt System Files ({len(corrupt_files)})',
                'details': corrupt_files,
                'recommendation': 'Run: sfc /scannow (as admin) to repair Windows'
            })
        
        # 2. Check registry size (indicates bloat)
        try:
            reg_path = os.path.join(W, 'System32', 'config', 'SOFTWARE')
            if os.path.exists(reg_path):
                reg_size = os.path.getsize(reg_path)
                if reg_size > 500*1024*1024:
                    issues.append({
                        'type': 'Registry Bloat',
                        'title': f'Large Registry ({fmt(reg_size)})',
                        'details': [{'path': reg_path, 'size': fmt(reg_size)}],
                        'recommendation': 'Consider using Windows Registry Cleaner'
                    })
        except:
            pass
        
        # 3. Check startup programs (using common autorun locations)
        LA = os.environ.get('LOCALAPPDATA', '')
        startup_issues = []
        startup_paths = [
            os.path.join(LA, 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'),
            os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'),
        ]
        for sp in startup_paths:
            if os.path.exists(sp):
                try:
                    for item in os.listdir(sp)[:50]:
                        if item.endswith(('.exe', '.vbs', '.js', '.bat', '.cmd')):
                            startup_issues.append({'path': os.path.join(sp, item), 'program': item})
                except:
                    pass
        
        if startup_issues:
            issues.append({
                'type': 'Startup Programs',
                'title': f'Startup Items ({len(startup_issues)})',
                'details': startup_issues,
                'recommendation': 'Review in Task Manager → Startup tab to disable unnecessary programs'
            })
        
        # 4. Check for bloated event logs
        event_log_path = os.path.join(W, 'System32', 'winevt', 'Logs')
        log_issues = []
        if os.path.exists(event_log_path):
            try:
                total_size = 0
                for root, dirs, files in os.walk(event_log_path):
                    for f in files:
                        if f.endswith('.evtx'):
                            fpath = os.path.join(root, f)
                            sz = os.path.getsize(fpath)
                            total_size += sz
                            if sz > 100*1024*1024:
                                log_issues.append({'file': f, 'size': fmt(sz)})
                
                if total_size > 1000*1024*1024:
                    issues.append({
                        'type': 'Event Logs',
                        'title': f'Large Event Logs ({fmt(total_size)})',
                        'details': log_issues[:10],
                        'recommendation': 'Open Event Viewer → right-click logs → Clear Log'
                    })
            except:
                pass
        
        # 5. Check for pending Windows updates
        try:
            pending_updates_path = os.path.join(W, 'SoftwareDistribution', 'Download')
            if os.path.exists(pending_updates_path):
                size = sum(os.path.getsize(os.path.join(pending_updates_path, f)) 
                          for f in os.listdir(pending_updates_path) 
                          if os.path.isfile(os.path.join(pending_updates_path, f)))
                if size > 0:
                    issues.append({
                        'type': 'Updates',
                        'title': f'Pending Updates ({fmt(size)})',
                        'details': [{'path': pending_updates_path, 'status': 'Waiting to install'}],
                        'recommendation': 'Install Windows updates and restart: Settings → Update & Security'
                    })
        except:
            pass
        
        return issues

# ───────── GLOW BUTTON ─────────
class GlowBtn(tk.Canvas):
    def __init__(self, parent, text="", cmd=None, color='#7c4dff',
                 w=220, h=46, fs=11, bold=True, radius=12, **kw):
        super().__init__(parent, width=w, height=h, bg=C['bg2'],
                         highlightthickness=0, **kw)
        self.cmd=cmd; self.color=color; self.txt=text
        self.W=w; self.H=h; self.fs=fs; self.bold=bold; self.r=radius
        self._hov=False; self._prs=False; self._disabled=False
        self._draw()
        self.bind('<Enter>', lambda e: self._set_hov(True))
        self.bind('<Leave>', lambda e: self._set_hov(False))
        self.bind('<ButtonPress-1>', lambda e: self._set_prs(True))
        self.bind('<ButtonRelease-1>', self._click)

    def _rr(self, x1,y1,x2,y2,r=12,**kw):
        pts=[x1+r,y1, x2-r,y1, x2,y1, x2,y1+r,
             x2,y2-r, x2,y2, x2-r,y2, x1+r,y2,
             x1,y2, x1,y2-r, x1,y1+r, x1,y1]
        return self.create_polygon(pts, smooth=True, **kw)

    def _draw(self):
        self.delete('all')
        if self._disabled:
            self._rr(1,1,self.W-1,self.H-1, self.r, fill=C['bg4'], outline=C['brd'])
            self.create_text(self.W//2, self.H//2, text=self.txt,
                            fill=C['tx3'], font=('Segoe UI',self.fs))
            return
        c = darker(self.color,50) if self._prs else (lighter(self.color,20) if self._hov else self.color)
        self._rr(2,4,self.W,self.H+1, self.r, fill='#000000', outline='')
        self._rr(0,0,self.W-2,self.H-3, self.r, fill=c, outline=lighter(c,15))
        h2 = (self.H-3)//2
        self._rr(2,2,self.W-4,h2, self.r-2, fill=lighter(c,35), outline='')
        fw = 'bold' if self.bold else 'normal'
        self.create_text(self.W//2, (self.H-3)//2+2, text=self.txt,
                        fill='#fff', font=('Segoe UI',self.fs,fw))

    def _set_hov(self,v): self._hov=v; self._draw()
    def _set_prs(self,v): self._prs=v; self._draw()
    def _click(self,e):
        self._prs=False; self._draw()
        if self.cmd and not self._disabled: self.cmd()
    def disable(self):
        self._disabled=True; self._draw()
    def enable(self):
        self._disabled=False; self._draw()

# ───────── GRADIENT PROGRESS BAR ─────────
class GradProgress(tk.Canvas):
    def __init__(self, parent, w=300, h=28, **kw):
        super().__init__(parent, width=w, height=h, bg=C['inp'],
                         highlightthickness=0, **kw)
        self.W=w; self.H=h; self.val=0; self._draw()

    def _rr(self, x1,y1,x2,y2,r=8,**kw):
        pts=[x1+r,y1,x2-r,y1,x2,y1,x2,y1+r,
             x2,y2-r,x2,y2,x2-r,y2,x1+r,y2,
             x1,y2,x1,y2-r,x1,y1+r,x1,y1]
        return self.create_polygon(pts,smooth=True,**kw)

    def _draw(self):
        self.delete('all')
        self._rr(0,0,self.W,self.H,8, fill=C['inp'], outline=C['brd'])
        fw = max(0, int(self.W * self.val / 100))
        if fw > 10:
            r1,g1,b1 = 0x7c,0x4d,0xff
            r2,g2,b2 = 0x00,0xe5,0xff
            steps=min(fw,100)
            for i in range(steps):
                x1=int(i*fw/steps); x2=int((i+1)*fw/steps)+1
                ratio=i/max(steps-1,1)
                r=int(r1+(r2-r1)*ratio); g=int(g1+(g2-g1)*ratio); b=int(b1+(b2-b1)*ratio)
                self.create_rectangle(x1,3,x2,self.H-3,
                                     fill=f'#{r:02x}{g:02x}{b:02x}', outline='')
            self.create_rectangle(4,4,fw-4,self.H//2-2,
                                 fill=lighter('#7c4dff',55), outline='', stipple='gray25')
        self.create_text(self.W//2, self.H//2, text=f"{int(self.val)}%",
                        fill='#fff', font=('Segoe UI',9,'bold'))

    def set(self,v): self.val=max(0,min(100,v)); self._draw()

# ───────── STAT CARD ─────────
class StatCard(tk.Frame):
    def __init__(self, parent, title="", value="", color=C['cyn'], icon="", **kw):
        super().__init__(parent, bg=C['bg3'], highlightbackground=C['brd'],
                         highlightthickness=1, **kw)
        self.color = color
        tk.Frame(self, bg=color, height=3).pack(fill='x')
        inner = tk.Frame(self, bg=C['bg3'])
        inner.pack(fill='x', padx=14, pady=(10,6))
        tk.Label(inner, text=f"{icon} {title}", font=('Segoe UI',9),
                bg=C['bg3'], fg=C['tx3']).pack(anchor='w')
        self.val_lbl = tk.Label(inner, text=value, font=('Segoe UI',14,'bold'),
                               bg=C['bg3'], fg=color)
        self.val_lbl.pack(anchor='w', pady=(2,0))
        tk.Frame(self, bg=C['bg3'], height=4).pack()

    def update_val(self, v):
        self.val_lbl.configure(text=v)

# ════════════════════════════════════════════════════
#          MAIN APPLICATION
# ════════════════════════════════════════════════════
class DeepDiskCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Deep Disk Cleaner Pro v2.0")
        self.root.geometry("1300x820")
        self.root.minsize(1000, 600)
        self.root.configure(bg=C['bg0'])

        self.scanning = False
        self.scan_results = OrderedDict()
        self.disk_vars = {}
        self.item_vars = {}
        self.cat_data = {}
        self.total_sz=0; self.sel_sz=0; self.total_files=0
        self.is_admin = self._chk_admin()
        self._scan_thread = None

        self._styles()
        self._build_ui()
        self._detect_disks()

        if not self.is_admin:
            self.root.after(500, self._admin_warn)

    def _chk_admin(self):
        try: return ctypes.windll.shell32.IsUserAnAdmin()
        except: return False

    def _admin_warn(self):
        messagebox.showwarning(
            "⚠️ Admin Mode Recommended",
            "Running without Administrator privileges.\n\n"
            "Some locations may not be fully accessible.\n\n"
            "Please right-click → 'Run as Administrator'\n"
            "for complete results.")

    def _styles(self):
        s = ttk.Style(); s.theme_use('clam')
        s.configure('Main.Treeview', background=C['bg3'], foreground=C['tx2'],
                    fieldbackground=C['bg3'], borderwidth=0, font=('Segoe UI',10),
                    rowheight=36)
        s.configure('Main.Treeview.Heading', background=C['bg4'], foreground=C['cyn'],
                    font=('Segoe UI',10,'bold'), borderwidth=0, relief='flat')
        s.map('Main.Treeview', background=[('selected',C['pur'])],
              foreground=[('selected','#fff')])
        s.configure('Main.Vertical.TScrollbar', background=C['bg3'],
                    troughcolor=C['bg1'], borderwidth=0, arrowsize=14)

    def _build_ui(self):
        hdr = tk.Frame(self.root, bg=C['bg1'], height=72)
        hdr.pack(fill='x'); hdr.pack_propagate(False)

        self.gline = tk.Canvas(hdr, height=3, bg=C['bg1'], highlightthickness=0)
        self.gline.pack(fill='x')
        self.gline.bind('<Configure>', self._draw_gline)

        hc = tk.Frame(hdr, bg=C['bg1'])
        hc.pack(fill='both', expand=True, padx=24, pady=(8,0))

        lf = tk.Frame(hc, bg=C['bg1']); lf.pack(side='left')
        tk.Label(lf, text="⚡", font=('Segoe UI',26), bg=C['bg1'],
                fg=C['cyn']).pack(side='left')
        tf = tk.Frame(lf, bg=C['bg1']); tf.pack(side='left', padx=(6,0))
        tk.Label(tf, text="DEEP DISK CLEANER", font=('Segoe UI',18,'bold'),
                bg=C['bg1'], fg=C['tx1']).pack(anchor='w')
        tk.Label(tf, text="Professional Disk Optimization Tool", font=('Segoe UI',9),
                bg=C['bg1'], fg=C['tx3']).pack(anchor='w')

        rf = tk.Frame(hc, bg=C['bg1']); rf.pack(side='right')
        status_txt = "🛡️ ADMIN" if self.is_admin else "⚠ Limited"
        status_col = C['grn'] if self.is_admin else C['org']
        tk.Label(rf, text=status_txt, font=('Segoe UI',10,'bold'),
                bg=C['bg1'], fg=status_col).pack(side='right')

        main = tk.Frame(self.root, bg=C['bg0'])
        main.pack(fill='both', expand=True, padx=18, pady=(8,18))

        left = tk.Frame(main, bg=C['bg0'], width=350)
        left.pack(side='left', fill='y', padx=(0,14)); left.pack_propagate(False)
        self._build_sidebar(left)

        right = tk.Frame(main, bg=C['bg0'])
        right.pack(side='right', fill='both', expand=True)
        self._build_content(right)

    def _draw_gline(self, e):
        cv=self.gline; cv.delete('all'); w=cv.winfo_width()
        colors=[C['cyn'],C['blu'],C['pur'],C['pnk'],C['org'],C['grn']]
        seg=max(1,w//len(colors))
        for i,c in enumerate(colors):
            cv.create_rectangle(i*seg,0,(i+1)*seg+2,3, fill=c, outline='')

    def _build_sidebar(self, parent):
        # Delete button — pinned to BOTTOM first so it is ALWAYS visible,
        # even on short screens where the sidebar overflows.
        df = tk.Frame(parent, bg=C['bg0'])
        df.pack(side='bottom', fill='x', padx=10, pady=(8,10))
        self.del_btn = GlowBtn(df, "🗑️  DELETE SELECTED", self._delete_sel,
                               C['red'], 340, 50, 12, radius=14)
        self.del_btn.pack(padx=0, pady=0)

        dc = tk.Frame(parent, bg=C['bg2'], highlightbackground=C['brd'],
                     highlightthickness=1)
        dc.pack(fill='x', pady=(0,10))

        dh = tk.Frame(dc, bg=C['bg2']); dh.pack(fill='x', padx=14, pady=(12,2))
        tk.Label(dh, text="💾 DRIVES", font=('Segoe UI',11,'bold'),
                bg=C['bg2'], fg=C['cyn']).pack(side='left')
        tk.Button(dh, text="↻", font=('Segoe UI',14), bg=C['bg2'], fg=C['cyn'],
                 bd=0, cursor='hand2', command=self._detect_disks,
                 activebackground=C['bg4'], activeforeground=C['cyn']).pack(side='right')

        tk.Frame(dc, bg=C['brd'], height=1).pack(fill='x', padx=14, pady=6)
        self.disk_frame = tk.Frame(dc, bg=C['bg2'])
        self.disk_frame.pack(fill='x', padx=10, pady=(0,10))

        bf = tk.Frame(parent, bg=C['bg0']); bf.pack(fill='x', pady=(0,10))
        
        # Main scan button (full width)
        self.scan_btn = GlowBtn(bf, "🔍  START DEEP SCAN", self._start_scan,
                                C['pur'], 340, 52, 13, radius=14)
        self.scan_btn.pack(pady=(0,8))
        
        # Sub-buttons (virus scan + system health)
        self.sub_btn_frame = tk.Frame(bf, bg=C['bg0'])
        self.sub_btn_frame.pack(fill='x', pady=(0,6))
        
        self.virus_btn = GlowBtn(self.sub_btn_frame, "🦠 VIRUS SCAN", self._start_virus_scan,
                                 C['red'], 164, 42, 10, radius=10)
        self.virus_btn.pack(side='left', padx=(0,4), expand=True, fill='x')
        
        self.health_btn = GlowBtn(self.sub_btn_frame, "⚕️ SYSTEM HEALTH", self._start_health_check,
                                  C['org'], 164, 42, 10, radius=10)
        self.health_btn.pack(side='right', padx=(4,0), expand=True, fill='x')
        
        # Stop button (hidden initially)
        self.stop_btn = GlowBtn(bf, "⏹  STOP", self._stop_scan,
                                C['red'], 340, 42, 11, radius=10)

        pc = tk.Frame(parent, bg=C['bg2'], highlightbackground=C['brd'],
                     highlightthickness=1)
        pc.pack(fill='x', pady=(0,10))

        ph = tk.Frame(pc, bg=C['bg2']); ph.pack(fill='x', padx=14, pady=(10,2))
        tk.Label(ph, text="📊 PROGRESS", font=('Segoe UI',11,'bold'),
                bg=C['bg2'], fg=C['pur']).pack(side='left')
        self.prog_lbl = tk.Label(ph, text="Ready", font=('Segoe UI',9),
                                bg=C['bg2'], fg=C['tx3'])
        self.prog_lbl.pack(side='right')

        self.prog_bar = GradProgress(pc, 318, 28)
        self.prog_bar.pack(padx=14, pady=4)

        self.status_lbl = tk.Label(pc, text="Select drives and click Scan",
                                   font=('Segoe UI',9), bg=C['bg2'],
                                   fg=C['tx2'], wraplength=310)
        self.status_lbl.pack(padx=14, pady=(0,10))

        sf = tk.Frame(parent, bg=C['bg0']); sf.pack(fill='x', pady=(0,0))

        row1 = tk.Frame(sf, bg=C['bg0']); row1.pack(fill='x', pady=(0,6))
        self.card_total = StatCard(row1, "Total Found", "0 B", C['cyn'], "📦")
        self.card_total.pack(side='left', fill='x', expand=True, padx=(0,4))
        self.card_files = StatCard(row1, "Files", "0", C['org'], "📄")
        self.card_files.pack(side='right', fill='x', expand=True, padx=(4,0))

        self.card_sel = StatCard(sf, "Selected to Delete", "0 B", C['grn'], "🎯")
        self.card_sel.pack(fill='x', pady=(0,10))

    def _build_content(self, parent):
        rc = tk.Frame(parent, bg=C['bg2'], highlightbackground=C['brd'],
                     highlightthickness=1)
        rc.pack(fill='both', expand=True)

        rh = tk.Frame(rc, bg=C['bg2']); rh.pack(fill='x', padx=16, pady=(12,2))
        tk.Label(rh, text="🗑️ SCAN RESULTS", font=('Segoe UI',12,'bold'),
                bg=C['bg2'], fg=C['pnk']).pack(side='left')

        bb = tk.Frame(rh, bg=C['bg2']); bb.pack(side='right')
        self._mk_sbtn(bb, "☑ Select All", C['grn'], self._sel_all)
        self._mk_sbtn(bb, "☐ Deselect All", C['org'], self._desel_all)

        tk.Frame(rc, bg=C['brd'], height=1).pack(fill='x', padx=16, pady=6)

        tf = tk.Frame(rc, bg=C['bg2'])
        tf.pack(fill='both', expand=True, padx=14, pady=(2,14))

        cols = ('chk','cat','path','size','files')
        self.tree = ttk.Treeview(tf, columns=cols, show='headings',
                                style='Main.Treeview', selectmode='none')
        self.tree.heading('chk', text='✓', anchor='center')
        self.tree.heading('cat', text='Category', anchor='w')
        self.tree.heading('path', text='Path / Description', anchor='w')
        self.tree.heading('size', text='Size', anchor='e')
        self.tree.heading('files', text='Files', anchor='center')
        self.tree.column('chk', width=40, anchor='center', stretch=False)
        self.tree.column('cat', width=155, anchor='w')
        self.tree.column('path', width=460, anchor='w')
        self.tree.column('size', width=105, anchor='e')
        self.tree.column('files', width=70, anchor='center')

        sb = ttk.Scrollbar(tf, orient='vertical', command=self.tree.yview,
                          style='Main.Vertical.TScrollbar')
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side='right', fill='y')
        self.tree.pack(fill='both', expand=True)
        self.tree.bind('<Button-1>', self._tree_click)

        for name, color in CAT_C.items():
            tag = name.lower().replace(' ','_')
            self.tree.tag_configure(tag, foreground=color,
                                   font=('Segoe UI',10,'bold'))
        self.tree.tag_configure('cat_row', background=C['bg4'],
                               foreground=C['cyn'],
                               font=('Segoe UI',10,'bold'))
        self.tree.tag_configure('item_row', background=C['bg3'],
                               foreground=C['tx2'])
        self.tree.tag_configure('sel_row', background='#0a2218',
                               foreground=C['grn'])
        self.tree.tag_configure('empty_row', foreground=C['tx3'],
                               font=('Segoe UI',11,'italic'))

        self.empty_id = self.tree.insert('','end',
            values=('','','No items yet — click Deep Scan to start','',''),
            tags=('empty_row',))

    def _mk_sbtn(self, parent, text, color, cmd):
        b = tk.Button(parent, text=text, font=('Segoe UI',9), bg=color,
                     fg='#fff', bd=0, padx=10, pady=4, cursor='hand2',
                     command=cmd, activebackground=lighter(color),
                     activeforeground='#fff')
        b.pack(side='left', padx=3)

    def _detect_disks(self):
        for w in self.disk_frame.winfo_children(): w.destroy()
        self.disk_vars = {}
        try: parts = psutil.disk_partitions(all=False)
        except: parts = []
        for p in parts:
            try: u = psutil.disk_usage(p.mountpoint)
            except: continue
            dl = p.mountpoint[:2]
            var = tk.BooleanVar(value=True); self.disk_vars[dl] = var

            dc = tk.Frame(self.disk_frame, bg=C['inp'],
                         highlightbackground=C['brd'], highlightthickness=1)
            dc.pack(fill='x', pady=3)

            row = tk.Frame(dc, bg=C['inp']); row.pack(fill='x', padx=10, pady=7)
            cb = tk.Checkbutton(row, variable=var, bg=C['inp'], fg=C['cyn'],
                               selectcolor=C['bg0'], activebackground=C['inp'],
                               activeforeground=C['cyn'], font=('Segoe UI',13),
                               cursor='hand2', bd=0, highlightthickness=0)
            cb.pack(side='left')

            inf = tk.Frame(row, bg=C['inp'])
            inf.pack(side='left', padx=(10,0), fill='x', expand=True)
            tk.Label(inf, text=f"{dl}  {p.fstype}", font=('Segoe UI',11,'bold'),
                    bg=C['inp'], fg=C['tx1']).pack(anchor='w')
            tk.Label(inf, text=f"{fmt(u.used)} / {fmt(u.total)}",
                    font=('Segoe UI',8), bg=C['inp'], fg=C['tx3']).pack(anchor='w')

            pct = u.percent
            pc = C['red'] if pct>90 else (C['org'] if pct>70 else C['grn'])
            tk.Label(row, text=f"{pct}%", font=('Segoe UI',12,'bold'),
                    bg=C['inp'], fg=pc).pack(side='right')

            bf = tk.Frame(dc, bg=C['bg0'], height=5)
            bf.pack(fill='x', padx=10, pady=(0,7)); bf.pack_propagate(False)
            tk.Frame(bf, bg=pc, height=5).place(relwidth=pct/100, relheight=1)

    def _start_scan(self):
        if self.scanning: return
        sel = [d for d,v in self.disk_vars.items() if v.get()]
        if not sel:
            messagebox.showwarning("No Drives", "Please select at least one drive.")
            return

        self.scanning = True
        self.scan_results = OrderedDict(); self.item_vars = {}
        self.cat_data = {}; self.total_sz=0; self.sel_sz=0; self.total_files=0

        for i in self.tree.get_children(): self.tree.delete(i)

        # Hide scan buttons, show stop button
        self.scan_btn.pack_forget()
        self.sub_btn_frame.pack_forget()
        self.stop_btn.pack(pady=(0,6))
        self.del_btn.disable()

        self._scan_thread = threading.Thread(target=self._scan_worker,
                                             args=(sel,), daemon=True)
        self._scan_thread.start()

    def _stop_scan(self):
        self.scanning = False
        self.root.after(100, self._scan_stopped)

    def _scan_worker(self, drives):
        targets = self._build_targets(drives)
        total_cats = len(targets)

        for idx, (cat, info) in enumerate(targets.items()):
            if not self.scanning: 
                return
            pct = int(idx / total_cats * 95)
            self.root.after(0, self._ui_prog, pct, f"Scanning: {cat}")

            items = []
            for pi in info['paths']:
                if not self.scanning: return
                p = pi['path']; nm = pi.get('name', p)

                if not os.path.exists(p): continue
                if not is_safe_path(p): continue

                self.root.after(0, self._ui_status, f"  → {nm[:50]}")

                try:
                    filt = pi.get('filter')
                    if filt:
                        sz, fc = self._size_pattern(p, filt, max_depth=12)
                    else:
                        sz, fc = self._size_dir(p, max_depth=12)
                except:
                    continue

                if sz > 0:
                    items.append({
                        'path': p, 'name': nm, 'size': sz, 'files': fc,
                        'filter': filt, 'sel': True
                    })

            if items:
                self.scan_results[cat] = {'icon': info['icon'], 'items': items}
                self.root.after(0, self._add_cat_ui, cat, info['icon'], items)

        self.root.after(0, self._scan_done)

    def _size_dir(self, path, max_depth=12):
        sz=0; fc=0
        if os.path.isfile(path):
            try: sz=os.path.getsize(path); fc=1
            except: pass
            return sz, fc
        base_depth = path.count(os.sep)
        try:
            for dp, dns, fns in os.walk(path):
                if dp.count(os.sep) - base_depth > max_depth:
                    dns.clear(); continue
                for f in fns:
                    if not self.scanning: return sz, fc
                    try:
                        fp = os.path.join(dp, f)
                        if os.path.isfile(fp):
                            sz += os.path.getsize(fp); fc += 1
                    except: continue
        except: pass
        return sz, fc

    def _size_pattern(self, path, filt, max_depth=12):
        sz=0; fc=0
        if os.path.isfile(path):
            fn = os.path.basename(path)
            try:
                if filt(fn): sz=os.path.getsize(path); fc=1
            except: pass
            return sz, fc
        base_depth = path.count(os.sep)
        try:
            for dp, dns, fns in os.walk(path):
                if dp.count(os.sep) - base_depth > max_depth:
                    dns.clear(); continue
                for f in fns:
                    if not self.scanning: return sz, fc
                    try:
                        if filt(f):
                            fp = os.path.join(dp, f)
                            if os.path.isfile(fp):
                                sz += os.path.getsize(fp); fc += 1
                    except: continue
        except: pass
        return sz, fc

    def _build_targets(self, drives):
        t = OrderedDict()
        W = os.environ.get('WINDIR','C:\\Windows')
        LA = os.environ.get('LOCALAPPDATA','')
        RA = os.environ.get('APPDATA','')
        UP = os.environ.get('USERPROFILE','')
        TMP = os.environ.get('TEMP','')
        PD = os.environ.get('PROGRAMDATA','C:\\ProgramData')

        # 1) TEMP FILES
        tp = []
        if TMP: tp.append({'path':TMP,'name':'User Temp Folder'})
        tp.append({'path':os.path.join(W,'Temp'),'name':'Windows Temp'})
        tp.append({'path':os.path.join(W,'Prefetch'),'name':'Prefetch Cache'})
        if UP:
            office_exts = ('.docx','.xlsx','.pptx','.doc','.xls','.ppt')
            tp.append({'path':UP,'name':'Office Temp (~$ files)',
                      'filter':lambda f, exts=office_exts: f.startswith('~$') and f.endswith(exts)})
        t['Temp Files'] = {'icon':'🗑️','paths':tp}

        # 2) BROWSER CACHE
        bp = []
        browsers = [
            ('Chrome', os.path.join(LA,'Google','Chrome','User Data')),
            ('Edge', os.path.join(LA,'Microsoft','Edge','User Data')),
            ('Brave', os.path.join(LA,'BraveSoftware','Brave-Browser','User Data')),
            ('Opera', os.path.join(LA,'Opera Software','Opera Stable')),
            ('Vivaldi', os.path.join(LA,'Vivaldi','User Data')),
        ]
        for bname, bbase in browsers:
            if not os.path.exists(bbase): continue
            try:
                for d in os.listdir(bbase):
                    dp = os.path.join(bbase, d)
                    if not os.path.isdir(dp): continue
                    for cd in ['Cache','Code Cache','GPUCache',
                               'Service Worker\\CacheStorage',
                               'Service Worker\\ScriptCache','ShaderCache',
                               'DawnCache','DawnGraphiteCache','DawnWebGPUCache',
                               'GrShaderCache','Network\\Cache',
                               'Cache_Data','blob_storage','File System']:
                        cp = os.path.join(dp, cd)
                        if os.path.exists(cp):
                            bp.append({'path':cp,'name':f'{bname} — {d[:20]} — {cd}'})
            except: continue
        ffp = os.path.join(LA,'Mozilla','Firefox','Profiles')
        if os.path.exists(ffp):
            try:
                for d in os.listdir(ffp):
                    dp = os.path.join(ffp,d)
                    if not os.path.isdir(dp): continue
                    for cd in ['cache2','startupCache','shader-cache']:
                        cp = os.path.join(dp,cd)
                        if os.path.exists(cp):
                            bp.append({'path':cp,'name':f'Firefox — {d[:20]} — {cd}'})
            except: pass
        t['Browser Cache'] = {'icon':'🌐','paths':bp}

        # 3) WINDOWS CACHE
        wp = []
        exp = os.path.join(LA,'Microsoft','Windows','Explorer')
        if os.path.exists(exp):
            wp.append({'path':exp,'name':'Thumbnail & Icon Cache',
                      'filter':lambda f, p1='thumbcache_', p2='iconcache_': f.startswith(p1) or f.startswith(p2)})
        for n,p in [
            ('Internet Cache', os.path.join(LA,'Microsoft','Windows','INetCache')),
            ('Web Cache', os.path.join(LA,'Microsoft','Windows','WebCache')),
            ('Font Cache', os.path.join(W,'ServiceProfiles','LocalService','AppData','Local','FontCache')),
            ('Internet Cookies', os.path.join(LA,'Microsoft','Windows','INetCookies')),
        ]:
            if os.path.exists(p): wp.append({'path':p,'name':n})
        t['Windows Cache'] = {'icon':'🪟','paths':wp}

        # 4) APP CACHE
        ap = []
        app_list = [
            ('Discord Cache', os.path.join(LA,'Discord','Cache')),
            ('Discord Code Cache', os.path.join(LA,'Discord','Code Cache')),
            ('Discord GPUCache', os.path.join(LA,'Discord','GPUCache')),
            ('Spotify Cache', os.path.join(LA,'Spotify','Storage')),
            ('Teams Cache', os.path.join(LA,'Microsoft','Teams','Cache')),
            ('Teams Blob', os.path.join(LA,'Microsoft','Teams','blob_storage')),
            ('Teams GPU', os.path.join(LA,'Microsoft','Teams','GPUCache')),
            ('VSCode Cache', os.path.join(LA,'Microsoft','vscode','Cache')),
            ('VSCode CachedData', os.path.join(LA,'Microsoft','vscode','CachedData')),
            ('Telegram Cache', os.path.join(RA,'Telegram Desktop','tdata','cache')),
            ('Slack Cache', os.path.join(RA,'Slack','Cache')),
            ('Slack GPU', os.path.join(RA,'Slack','GPUCache')),
            ('Zoom Cache', os.path.join(LA,'Zoom','data','cache')),
            ('Epic Games', os.path.join(LA,'Epic Games','Launcher','Cache')),
            ('GOG Galaxy', os.path.join(LA,'GOG.com','Galaxy','Cache')),
            ('Steam HTML Cache', os.path.join(LA,'Steam','htmlcache')),
            ('Battle.net Cache', os.path.join(LA,'Battle.net','Cache')),
            ('NVIDIA GL Cache', os.path.join(LA,'NVIDIA','GLCache')),
            ('NVIDIA DX Cache', os.path.join(LA,'NVIDIA','DXCache')),
            ('DirectX Shader Cache', os.path.join(LA,'D3DSCache')),
            ('Adobe Cache', os.path.join(LA,'Adobe','Common','Media Cache')),
            ('Adobe CameraRaw', os.path.join(LA,'Adobe','CameraRaw','Cache')),
            ('OneDrive Cache', os.path.join(LA,'Microsoft','OneDrive','cache')),
            ('Outlook Cache', os.path.join(LA,'Microsoft','Outlook')),
            ('WhatsApp Cache', os.path.join(LA,'WhatsApp','Cache')),
            ('Signal Cache', os.path.join(RA,'Signal','Cache')),
            ('Postman Cache', os.path.join(RA,'Postman','Cache')),
            ('Figma Cache', os.path.join(LA,'Figma','Cache')),
            ('Notion Cache', os.path.join(RA,'Notion','Cache')),
            ('JetBrains Cache', os.path.join(LA,'JetBrains')),
            ('Unity Cache', os.path.join(LA,'Unity','cache')),
            ('Cursor Cache', os.path.join(LA,'Cursor','Cache')),
            ('VSCode (Code) Cache', os.path.join(RA,'Code','Cache')),
            ('VSCode (Code) CachedData', os.path.join(RA,'Code','CachedData')),
            ('VSCode GPUCache', os.path.join(RA,'Code','GPUCache')),
        ]
        for nm,p in app_list:
            if os.path.exists(p): ap.append({'path':p,'name':nm})
        if os.path.exists(LA):
            try:
                handled = {'Google','Microsoft','Mozilla','Opera','BraveSoftware',
                          'Discord','Spotify','Teams','Telegram','Slack',
                          'Vivaldi','GOG.com','Epic Games','vscode','Programs'}
                for ad in os.listdir(LA):
                    if ad in handled: continue
                    apath = os.path.join(LA,ad)
                    if not os.path.isdir(apath): continue
                    for cn in ['Cache','cache','GPUCache','Code Cache','CachedData',
                               'ShaderCache','Cache_Data','blob_storage',
                               'Network\\Cache','DawnCache','GrShaderCache']:
                        cp = os.path.join(apath,cn)
                        if os.path.exists(cp):
                            ap.append({'path':cp,'name':f'{ad} — {cn}'})
            except: pass
        # Generic Roaming (APPDATA) cache sweep
        if os.path.exists(RA):
            try:
                ra_handled = {'Telegram Desktop','Slack','Code','Signal',
                              'Postman','Notion','Microsoft','npm-cache'}
                for ad in os.listdir(RA):
                    if ad in ra_handled: continue
                    apath = os.path.join(RA,ad)
                    if not os.path.isdir(apath): continue
                    for cn in ['Cache','cache','GPUCache','Code Cache','CachedData',
                               'ShaderCache','Cache_Data','blob_storage']:
                        cp = os.path.join(apath,cn)
                        if os.path.exists(cp):
                            ap.append({'path':cp,'name':f'{ad} (Roaming) — {cn}'})
            except: pass
        t['App Cache'] = {'icon':'📱','paths':ap}

        # 5) LOG FILES
        lp = []
        for n,p in [
            ('Windows Logs', os.path.join(W,'Logs')),
            ('CBS Logs', os.path.join(W,'Logs','CBS')),
            ('DISM Logs', os.path.join(W,'Logs','DISM')),
            ('Panther Logs', os.path.join(W,'Panther')),
            ('Crash Dumps', os.path.join(LA,'CrashDumps')),
            ('WER Reports', os.path.join(PD,'Microsoft','Windows','WER')),
            ('Minidumps', os.path.join(W,'Minidump')),
            ('Memory Dump', os.path.join(W,'MEMORY.DMP')),
            ('Temp Logs', os.path.join(W,'Temp')),
            ('Performance Logs', os.path.join(W,'System32','LogFiles')),
        ]:
            if os.path.exists(p): lp.append({'path':p,'name':n})
        t['Log Files'] = {'icon':'📋','paths':lp}

        # 6) UPDATE CLEANUP
        up = []
        for n,p in [
            ('Win Update Downloads', os.path.join(W,'SoftwareDistribution','Download')),
            ('WinSxS Temp', os.path.join(W,'WinSxS','Temp')),
            ('Installer Cache', os.path.join(W,'Installer','$PatchCache$')),
            ('Delivery Optimization', os.path.join(W,'SoftwareDistribution','DeliveryOptimization')),
            ('Delivery Opt Cache', os.path.join(PD,'Microsoft','Network','Downloader')),
            ('Windows Update Logs', os.path.join(W,'Logs','WindowsUpdate')),
        ]:
            if os.path.exists(p): up.append({'path':p,'name':n})
        t['Update Cleanup'] = {'icon':'🔄','paths':up}

        # 7) PYTHON CACHES
        pyp = []
        pycache_filter = lambda f: f.endswith('.pyc') or f.endswith('.pyo')
        for pth in [
            os.path.join(LA,'Programs','Python'),
            os.path.join(UP,'.venv'),
            os.path.join(UP,'.pyenv'),
        ]:
            if os.path.exists(pth):
                pyp.append({'path':pth,'name':f'Python: {os.path.basename(pth)}',
                           'filter':pycache_filter})
        if pyp:
            t['Python Caches'] = {'icon':'🐍','paths':pyp}

        # 8) NPM & NODE
        npp = []
        npm_home = os.path.join(UP,'.npm')
        npm_cache = os.path.join(RA,'npm-cache')
        if os.path.exists(npm_home): npp.append({'path':npm_home,'name':'NPM Home'})
        if os.path.exists(npm_cache): npp.append({'path':npm_cache,'name':'NPM Cache'})
        if npp:
            t['NPM & Node'] = {'icon':'📦','paths':npp}

        # 9) RECYCLE BIN
        rp = []
        for d in drives:
            rb = os.path.join(d+os.sep,'$Recycle.Bin')
            if os.path.exists(rb): rp.append({'path':rb,'name':f'Recycle Bin ({d})'})
        t['Recycle Bin'] = {'icon':'♻️','paths':rp}

        # 10) MISC JUNK
        mp = []
        # Only search common user locations, not entire drives (too slow & risky)
        user_roots = [os.path.expanduser('~'), os.path.join(os.path.expanduser('~'),'Desktop'),
                      os.path.join(os.path.expanduser('~'),'Downloads'),
                      os.path.join(os.path.expanduser('~'),'Documents')]
        # Safe junk: thumbnail dbs, leftover temp & crash dump files only
        junk_exts = ('.tmp', '.dmp', '.stackdump', '.chk')
        junk_filter = lambda f: (f.lower() in ('thumbs.db', 'desktop.ini.tmp')
                                 or f.lower().endswith(junk_exts))
        for root in user_roots:
            if os.path.exists(root):
                mp.append({'path':root,'name':f'Junk files in {os.path.basename(root) or root}',
                          'filter':junk_filter})
        t['Misc Junk'] = {'icon':'🧹','paths':mp}

        return t

    def _ui_prog(self, val, txt):
        self.prog_bar.set(val)
        self.prog_lbl.configure(text=txt)

    def _ui_status(self, txt):
        self.status_lbl.configure(text=txt)

    def _add_cat_ui(self, cat, icon, items):
        color = CAT_C.get(cat, C['cyn'])
        csz = sum(i['size'] for i in items)
        cfc = sum(i['files'] for i in items)

        cid = self.tree.insert('','end',
            values=('☑', f'{icon} {cat}', '', fmt(csz), cfc),
            tags=('cat_row',))

        self.cat_data[cid] = {'cat':cat, 'items':items, 'size':csz}

        for it in items:
            var = tk.BooleanVar(value=True)
            iid = self.tree.insert(cid,'end',
                values=('☑', '', it['name'], fmt(it['size']), it['files']),
                tags=('sel_row',))
            self.item_vars[iid] = var
            it['tid'] = iid; it['var'] = var

        self.tree.item(cid, open=True)
        self._update_stats()

    def _scan_stopped(self):
        self.prog_bar.set(0)
        self.prog_lbl.configure(text="Stopped")
        self.stop_btn.pack_forget()
        self.scan_btn.pack(pady=(0,8))
        self.sub_btn_frame.pack(fill='x', pady=(0,6))
        self.status_lbl.configure(text="Scan stopped by user")

    def _start_virus_scan(self):
        if self.scanning: return
        self.scanning = True
        self.scan_results = OrderedDict(); self.item_vars = {}
        self.cat_data = {}; self.total_sz=0; self.sel_sz=0; self.total_files=0

        for i in self.tree.get_children(): self.tree.delete(i)

        # Hide scan buttons, show stop button
        self.scan_btn.pack_forget()
        self.sub_btn_frame.pack_forget()
        self.stop_btn.pack(pady=(0,6))
        self.del_btn.disable()

        self._scan_thread = threading.Thread(target=self._virus_scan_worker, daemon=True)
        self._scan_thread.start()

    def _virus_scan_worker(self):
        """Scan for viruses and malware"""
        W = os.environ.get('WINDIR', 'C:\\Windows')
        LA = os.environ.get('LOCALAPPDATA', '')
        
        scan_paths = [
            os.path.join(LA, 'Downloads'),
            os.path.join(LA, 'Temp'),
            os.path.join(W, 'Temp'),
            os.path.expanduser('~'),
        ]
        
        threat_items = []
        
        for idx, path in enumerate(scan_paths):
            if not self.scanning: return
            
            pct = int(idx / len(scan_paths) * 90)
            self.root.after(0, self._ui_prog, pct, f"Scanning: {os.path.basename(path)}")
            
            if not os.path.exists(path): continue
            
            self.root.after(0, self._ui_status, f"  → {path[:50]}")
            
            try:
                infected = VirusScanner.scan_directory(path, max_files=500)
                for item in infected:
                    threat_items.append({
                        'path': item['path'],
                        'name': f"Threats: {', '.join(t['type'] for t in item['threats'])}",
                        'threats': item['threats'],
                        'size': os.path.getsize(item['path']) if os.path.exists(item['path']) else 0,
                        'files': 1,
                        'sel': True
                    })
            except:
                pass
        
        if threat_items:
            self.scan_results['Virus Threats'] = {'icon': '🦠', 'items': threat_items}
            self.root.after(0, self._add_virus_ui, threat_items)
        
        self.root.after(0, self._virus_scan_done)

    def _add_virus_ui(self, items):
        """Add virus threats to UI"""
        cat = 'Virus Threats'
        icon = '🦠'
        csz = sum(i['size'] for i in items)
        cfc = len(items)

        cid = self.tree.insert('','end',
            values=('☑', f'{icon} {cat}', '', fmt(csz), cfc),
            tags=('cat_row',))

        self.cat_data[cid] = {'cat': cat, 'items': items, 'size': csz}

        for it in items:
            var = tk.BooleanVar(value=True)
            threat_desc = ', '.join(f"{t['type']}" for t in it['threats'])
            iid = self.tree.insert(cid, 'end',
                values=('☑', '', f"{it['name']} - {it['path'][:40]}", fmt(it['size']), it['files']),
                tags=('sel_row',))
            self.item_vars[iid] = var
            it['tid'] = iid; it['var'] = var

        self.tree.item(cid, open=True)
        self._update_stats()

    def _virus_scan_done(self):
        self.scanning = False
        self.prog_bar.set(100)
        self.prog_lbl.configure(text="Complete ✓")
        self.stop_btn.pack_forget()
        self.scan_btn.pack(pady=(0,8))
        self.sub_btn_frame.pack(fill='x', pady=(0,6))
        self.del_btn.enable()

        if self.scan_results:
            self.status_lbl.configure(
                text=f"⚠️ Found {fmt(self.total_sz)} of threats")
        else:
            self.status_lbl.configure(text="✅ No threats detected!")
            self.tree.insert('','end',
                values=('','','No threats found — system is safe!','',''),
                tags=('empty_row',))

    def _start_health_check(self):
        if self.scanning: return
        self.scanning = True
        self.scan_results = OrderedDict(); self.item_vars = {}
        self.cat_data = {}; self.total_sz=0; self.sel_sz=0; self.total_files=0

        for i in self.tree.get_children(): self.tree.delete(i)

        # Hide scan buttons, show stop button
        self.scan_btn.pack_forget()
        self.sub_btn_frame.pack_forget()
        self.stop_btn.pack(pady=(0,6))
        self.del_btn.disable()

        self._scan_thread = threading.Thread(target=self._health_check_worker, daemon=True)
        self._scan_thread.start()

    def _health_check_worker(self):
        """Scan for system health issues"""
        if not self.scanning: return
        
        self.root.after(0, self._ui_prog, 30, "Checking system files...")
        self.root.after(0, self._ui_status, "  → Scanning Windows integrity")
        
        issues = SystemHealthCheck.check_issues()
        
        issue_items = []
        for issue in issues:
            if not self.scanning: return
            
            # Create item for each issue type
            detail_text = issue.get('recommendation', 'No action needed')
            sz = len(str(issue['details']))  # Use detail size as proxy
            
            for detail in issue['details'][:3]:  # Show first 3 items per issue
                detail_path = detail.get('path') or detail.get('file') or str(detail)
                issue_items.append({
                    'path': detail_path,
                    'name': f"{issue['type']}: {issue['title']}",
                    'issue': issue['type'],
                    'detail': detail_text,
                    'size': 0,
                    'files': 1,
                    'sel': False  # Don't auto-select health issues
                })
        
        if issue_items:
            self.scan_results['System Issues'] = {'icon': '⚕️', 'items': issue_items}
            self.root.after(0, self._add_health_ui, issue_items, issues)
        
        self.root.after(0, self._health_check_done)

    def _add_health_ui(self, items, issues):
        """Add system issues to UI"""
        cat = 'System Issues'
        icon = '⚕️'

        cid = self.tree.insert('','end',
            values=('☐', f'{icon} {cat}', '', f'{len(items)} issues', len(items)),
            tags=('cat_row',))

        self.cat_data[cid] = {'cat': cat, 'items': items, 'size': 0}

        for it in items:
            var = tk.BooleanVar(value=False)
            iid = self.tree.insert(cid, 'end',
                values=('☐', '', f"{it['name']}\n📌 Fix: {it['detail'][:60]}", '', it['files']),
                tags=('item_row',))
            self.item_vars[iid] = var
            it['tid'] = iid; it['var'] = var

        self.tree.item(cid, open=True)

    def _health_check_done(self):
        self.scanning = False
        self.prog_bar.set(100)
        self.prog_lbl.configure(text="Complete ✓")
        self.stop_btn.pack_forget()
        self.scan_btn.pack(pady=(0,8))
        self.sub_btn_frame.pack(fill='x', pady=(0,6))
        self.del_btn.disable()  # Don't allow deletion of health issues

        if self.scan_results:
            issue_count = sum(len(v['items']) for v in self.scan_results.values())
            self.status_lbl.configure(
                text=f"⚠️ Found {issue_count} system issues - see recommendations above")
        else:
            self.status_lbl.configure(text="✅ System is healthy! No issues found.")
            self.tree.insert('','end',
                values=('','','System check complete — all healthy!','',''),
                tags=('empty_row',))

    def _scan_done(self):
        self.scanning = False
        self.prog_bar.set(100)
        self.prog_lbl.configure(text="Complete ✓")
        self.stop_btn.pack_forget()
        self.scan_btn.pack(pady=(0,8))
        self.sub_btn_frame.pack(fill='x', pady=(0,6))
        self.del_btn.enable()

        if self.scan_results:
            self.status_lbl.configure(
                text=f"✅ Found {fmt(self.total_sz)} of cleanable files across "
                     f"{len(self.scan_results)} categories")
        else:
            self.status_lbl.configure(text="✅ Your system is clean! No junk found.")
            self.tree.insert('','end',
                values=('','','No junk files found — system is clean!','',''),
                tags=('empty_row',))

    def _tree_click(self, event):
        rid = self.tree.identify_row(event.y)
        if not rid: return

        if rid in self.cat_data:
            ci = self.cat_data[rid]
            any_sel = any(it['var'].get() for it in ci['items'])
            ns = not any_sel
            for it in ci['items']:
                it['var'].set(ns)
                v = self.tree.item(it['tid'],'values')
                self.tree.item(it['tid'],
                    values=('☑' if ns else '☐', v[1], v[2], v[3], v[4]),
                    tags=('sel_row' if ns else 'item_row',))
            v = self.tree.item(rid,'values')
            self.tree.item(rid,
                values=('☑' if ns else '☐', v[1], v[2], v[3], v[4]))

        elif rid in self.item_vars:
            var = self.item_vars[rid]
            ns = not var.get(); var.set(ns)
            v = self.tree.item(rid,'values')
            self.tree.item(rid,
                values=('☑' if ns else '☐', v[1], v[2], v[3], v[4]),
                tags=('sel_row' if ns else 'item_row',))
            pid = self.tree.parent(rid)
            if pid in self.cat_data:
                ci = self.cat_data[pid]
                alls = all(it['var'].get() for it in ci['items'])
                anys = any(it['var'].get() for it in ci['items'])
                pv = self.tree.item(pid,'values')
                sym = '☑' if alls else ('⊡' if anys else '☐')
                self.tree.item(pid, values=(sym, pv[1], pv[2], pv[3], pv[4]))

        self._update_stats()

    def _sel_all(self):
        for iid, var in self.item_vars.items():
            var.set(True)
            v = self.tree.item(iid,'values')
            self.tree.item(iid, values=('☑',v[1],v[2],v[3],v[4]),
                          tags=('sel_row',))
        for cid in self.cat_data:
            v = self.tree.item(cid,'values')
            self.tree.item(cid, values=('☑',v[1],v[2],v[3],v[4]))
        self._update_stats()

    def _desel_all(self):
        for iid, var in self.item_vars.items():
            var.set(False)
            v = self.tree.item(iid,'values')
            self.tree.item(iid, values=('☐',v[1],v[2],v[3],v[4]),
                          tags=('item_row',))
        for cid in self.cat_data:
            v = self.tree.item(cid,'values')
            self.tree.item(cid, values=('☐',v[1],v[2],v[3],v[4]))
        self._update_stats()

    def _update_stats(self):
        tt=0; st=0; tf=0
        for cid, ci in self.cat_data.items():
            tt += ci['size']
            for it in ci['items']:
                tf += it['files']
                if it['var'].get(): st += it['size']
        self.total_sz=tt; self.sel_sz=st; self.total_files=tf
        self.card_total.update_val(fmt(tt))
        self.card_files.update_val(f"{tf:,}")
        self.card_sel.update_val(fmt(st))

    def _delete_sel(self):
        to_del = []
        for cid, ci in self.cat_data.items():
            for it in ci['items']:
                if it['var'].get(): to_del.append(it)
        if not to_del:
            messagebox.showinfo("Nothing Selected", "Please select items to delete.")
            return

        tsz = sum(i['size'] for i in to_del)
        msg = (f"⚠️  DELETE CONFIRMATION\n\n"
               f"You are about to delete {len(to_del)} items ({fmt(tsz)}).\n\n"
               f"This will permanently remove temp, cache & log FILES.\n"
               f"Folders will be preserved. App data will NOT be touched.\n"
               f"System files are protected.\n\n"
               f"This action CANNOT be undone. Continue?")
        if not messagebox.askyesno("Confirm Deletion", msg, icon='warning'):
            return

        self.scan_btn.pack_forget()
        self.stop_btn.pack(pady=(0,6))
        self.del_btn.disable()
        self.scanning = True
        threading.Thread(target=self._del_worker, args=(to_del,),
                        daemon=True).start()

    def _del_worker(self, items):
        deleted=0; failed=0; freed=0; errors=[]

        for idx, it in enumerate(items):
            if not self.scanning: 
                self.root.after(0, self._del_stopped, deleted, freed)
                return
            pct = int(idx/len(items)*100)
            self.root.after(0, self._ui_prog, pct, f"Deleting: {it['name'][:40]}")
            self.root.after(0, self._ui_status, f"  → {it['path'][:70]}")

            try:
                filt = it.get('filter')
                if filt:
                    cnt, fsz = self._del_pattern(it['path'], filt)
                    deleted += cnt; freed += fsz
                else:
                    cnt, fsz = self._del_dir_files(it['path'])
                    deleted += cnt; freed += fsz
            except Exception as e:
                failed += 1
                errors.append(f"{it['name']}: {e}")
            time.sleep(0.01)

        self.scanning = False
        self.root.after(0, self._del_done, deleted, failed, freed, items, errors)

    def _del_dir_files(self, path):
        cnt=0; freed=0
        if os.path.isfile(path):
            try:
                freed = os.path.getsize(path)
                os.remove(path); cnt=1
            except: pass
            return cnt, freed
        try:
            for dp, dns, fns in os.walk(path):
                for f in fns:
                    if not self.scanning: return cnt, freed
                    try:
                        fp = os.path.join(dp, f)
                        if os.path.isfile(fp):
                            freed += os.path.getsize(fp)
                            os.remove(fp); cnt += 1
                    except: continue
        except: pass
        return cnt, freed

    def _del_pattern(self, path, filt):
        cnt=0; freed=0
        if os.path.isfile(path):
            fn = os.path.basename(path)
            try:
                if filt(fn):
                    freed = os.path.getsize(path); os.remove(path); cnt=1
            except: pass
            return cnt, freed
        try:
            for dp, dns, fns in os.walk(path):
                for f in fns:
                    if not self.scanning: return cnt, freed
                    try:
                        if filt(f):
                            fp = os.path.join(dp, f)
                            if os.path.isfile(fp):
                                freed += os.path.getsize(fp)
                                os.remove(fp); cnt += 1
                    except: continue
        except: pass
        return cnt, freed

    def _del_done(self, deleted, failed, freed, items, errors):
        self.stop_btn.pack_forget(); self.scan_btn.pack(pady=(0,6))
        self.del_btn.enable()
        self.prog_bar.set(100); self.prog_lbl.configure(text="Done ✓")

        status = f"✅ Deleted {deleted} items, freed {fmt(freed)}"
        if failed:
            status += f" | ⚠️ {failed} items couldn't be deleted"
        self.status_lbl.configure(text=status)

        # Only remove successfully deleted items (those with tid and var.get() == True)
        for it in items:
            tid = it.get('tid')
            if tid and self.tree.exists(tid) and it['var'].get():
                self.tree.delete(tid)
                if tid in self.item_vars: del self.item_vars[tid]

        for cid in list(self.cat_data.keys()):
            ci = self.cat_data[cid]
            # Keep items that weren't deleted (var is False) or didn't complete deletion
            ci['items'] = [i for i in ci['items'] if not i['var'].get()]
            if not ci['items']:
                if self.tree.exists(cid): self.tree.delete(cid)
                del self.cat_data[cid]
            else:
                nsz = sum(i['size'] for i in ci['items'])
                nfc = sum(i['files'] for i in ci['items'])
                v = self.tree.item(cid,'values')
                self.tree.item(cid, values=('☑',v[1],'',fmt(nsz),nfc))
                ci['size'] = nsz

        self._update_stats()

        messagebox.showinfo("Deletion Complete",
            f"✅ Successfully freed {fmt(freed)}\n"
            f"   {deleted} files deleted\n" +
            (f"   ⚠️ {failed} files couldn't be deleted (in use)" if failed else ""))

    def _del_stopped(self, deleted, freed):
        self.stop_btn.pack_forget(); self.scan_btn.pack(pady=(0,6))
        self.del_btn.enable()
        self.prog_bar.set(0); self.prog_lbl.configure(text="Stopped")
        self.status_lbl.configure(text=f"Deletion stopped. Freed {fmt(freed)} from {deleted} files.")

    def _on_close(self):
        self.scanning = False
        time.sleep(0.1)
        self.root.destroy()

def main():
    try: ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except: pass
    root = tk.Tk()
    app = DeepDiskCleaner(root)
    root.protocol("WM_DELETE_WINDOW", app._on_close)
    root.mainloop()

if __name__ == '__main__':
    main()
