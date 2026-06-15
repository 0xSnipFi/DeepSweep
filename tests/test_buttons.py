#!/usr/bin/env python3
"""Test script to verify button visibility issue"""

import tkinter as tk

# Color theme
C = {
    'bg0':'#04060e', 'bg1':'#080d1a', 'bg2':'#0e1628', 'bg3':'#141e35',
    'bg4':'#1a2844', 'bg5':'#203050', 'inp':'#0a1220',
    'cyn':'#00e5ff', 'blu':'#2979ff', 'pur':'#7c4dff', 'pnk':'#ff4081',
    'grn':'#00e676', 'ylw':'#ffd600', 'org':'#ff9100', 'red':'#ff1744',
    'tel':'#1de9b6', 'wht':'#ffffff', 'tx1':'#eceff1', 'tx2':'#90a4ae',
    'tx3':'#546e7a', 'brd':'#1a2a48', 'brd2':'#2a3a5a',
}

def lighter(c, a=30):
    c = c.lstrip('#')
    return f'#{min(255,int(c[0:2],16)+a):02x}{min(255,int(c[2:4],16)+a):02x}{min(255,int(c[4:6],16)+a):02x}'

def test_buttons():
    root = tk.Tk()
    root.title("Button Visibility Test")
    root.geometry("800x400")
    root.configure(bg=C['bg0'])
    
    # Create the same structure as in the app
    rc = tk.Frame(root, bg=C['bg2'], highlightbackground=C['brd'],
                 highlightthickness=1)
    rc.pack(fill='both', expand=True, padx=20, pady=20)
    
    rh = tk.Frame(rc, bg=C['bg2'])
    rh.pack(fill='x', padx=16, pady=(12,2))
    
    tk.Label(rh, text="🗑️ SCAN RESULTS", font=('Segoe UI',12,'bold'),
            bg=C['bg2'], fg=C['pnk']).pack(side='left')
    
    bb = tk.Frame(rh, bg=C['bg2'])
    bb.pack(side='right')
    
    print(f"Creating buttons in frame: {bb}")
    print(f"Frame bg color: {C['bg2']}")
    print(f"Green button color: {C['grn']}")
    print(f"Orange button color: {C['org']}")
    
    # Create buttons using the same method
    b1 = tk.Button(bb, text="☑ Select All", font=('Segoe UI',9), bg=C['grn'],
                   fg='#fff', bd=0, padx=10, pady=4, cursor='hand2',
                   command=lambda: print("Select All clicked"),
                   activebackground=lighter(C['grn']),
                   activeforeground='#fff')
    b1.pack(side='left', padx=3)
    print(f"Button 1 created: {b1}")
    print(f"Button 1 winfo_width: {b1.winfo_reqwidth()}")
    
    b2 = tk.Button(bb, text="☐ Deselect All", font=('Segoe UI',9), bg=C['org'],
                   fg='#fff', bd=0, padx=10, pady=4, cursor='hand2',
                   command=lambda: print("Deselect All clicked"),
                   activebackground=lighter(C['org']),
                   activeforeground='#fff')
    b2.pack(side='left', padx=3)
    print(f"Button 2 created: {b2}")
    print(f"Button 2 winfo_width: {b2.winfo_reqwidth()}")
    
    # Add some content below
    tk.Label(rc, text="If you can see two colored buttons above (green and orange), they are working!",
            bg=C['bg2'], fg=C['tx1'], font=('Segoe UI',11)).pack(pady=20)
    
    # Check after window is drawn
    def check_buttons():
        print(f"\nAfter rendering:")
        print(f"Button 1 actual width: {b1.winfo_width()}, height: {b1.winfo_height()}")
        print(f"Button 2 actual width: {b2.winfo_width()}, height: {b2.winfo_height()}")
        print(f"Button 1 visible: {b1.winfo_viewable()}")
        print(f"Button 2 visible: {b2.winfo_viewable()}")
        print(f"Frame bb width: {bb.winfo_width()}, height: {bb.winfo_height()}")
    
    root.after(100, check_buttons)
    
    root.mainloop()

if __name__ == '__main__':
    test_buttons()
