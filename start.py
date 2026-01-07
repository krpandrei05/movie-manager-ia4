#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import threading
from pathlib import Path

# Adaugam directoarele in path
BASE_DIR = Path(__file__).parent.absolute()
SERVER_DIR = BASE_DIR / 'server'
CLIENT_DIR = BASE_DIR / 'client'

def run_server():
    # Porneste serverul (Backend API) pe portul 5000
    os.chdir(SERVER_DIR)
    return subprocess.Popen(
        [sys.executable, 'app.py'],
        cwd=str(SERVER_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

def run_client():
    # Porneste clientul (Frontend Web) pe portul 5001
    os.chdir(CLIENT_DIR)
    return subprocess.Popen(
        [sys.executable, 'app.py'],
        cwd=str(CLIENT_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

if __name__ == '__main__':    
    processes = []
    
    try:
        # Pornim Server-ul (Backend)
        print("Pornire Server (Backend API)...")
        server_process = run_server()
        processes.append(('Server', server_process))
        time.sleep(2)  # Asteptam sa porneasca
        
        # Pornim Client-ul (Frontend)
        print("Pornire Client (Frontend Web)...")
        client_process = run_client()
        processes.append(('Client', client_process))
        time.sleep(2)  # Asteptam sa porneasca
        
        print()
        print("Sistemul rulează în arhitectura Client-Server!")
        print()
        print("Server API:   http://localhost:5000 (Backend)")
        print("Client Web:   http://localhost:5001 (Frontend)")
        print()
        print("Deschide browser-ul la: http://localhost:5001")
        print()
        
        # Afisam output-ul proceselor
        def monitor_process(name, process):
            for line in iter(process.stdout.readline, ''):
                if line:
                    print(f"[{name}] {line.rstrip()}")
        
        threads = []
        for name, process in processes:
            thread = threading.Thread(target=monitor_process, args=(name, process), daemon=True)
            thread.start()
            threads.append(thread)
        
        # Asteptam ca procesele sa ruleze
        while all(p.poll() is None for _, p in processes):
            time.sleep(1)
            
    except KeyboardInterrupt:
        print()
        print("Oprire sistem...")
        for name, process in processes:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        sys.exit(0)
