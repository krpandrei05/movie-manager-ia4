import subprocess
import time
import sys
import signal
import os

# Variabile globale pentru procese
server_process = None
client_process = None

def signal_handler(sig, frame):
    print("\n[Start Script] Interceptat Ctrl+C. Opreste procesele...")
    oprire_sistem()
    sys.exit(0)

def oprire_sistem():
    global server_process, client_process
    
    if server_process:
        print("[Start Script] Termina Server API...")
        server_process.terminate()
        server_process.wait()
    
    if client_process:
        print("[Start Script] Termina Client Web...")
        client_process.terminate()
        client_process.wait()
        
    print("[Start Script] Toate procesele au fost oprite.")

def run_project():
    global server_process, client_process
    
    # Inregistreaza handler pentru Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print("Porneste Server (Backend API)...")
    server_process = subprocess.Popen([sys.executable, 'server/app.py'])
    
    print("Porneste Client (Frontend Web)...")
    client_process = subprocess.Popen([sys.executable, 'client/app.py'])
    
    print("\nSistemul ruleaza in arhitectura Client-Server!")
    print("\nServer API:   http://localhost:5000 (Backend)")
    print("Client Web:   http://localhost:5001 (Frontend)")
    print("\nDeschide browser-ul la: http://localhost:5001\n")
    
    # Asteapta ca procesele sa ruleze
    try:
        server_process.wait()
        client_process.wait()
    except KeyboardInterrupt:
        pass # Se ocupa signal_handler

if __name__ == "__main__":
    run_project()
