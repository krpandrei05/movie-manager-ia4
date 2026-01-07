# Modul pentru gestionarea securitatii: token-uri si verificare autentificare
from models.database import get_db_connection

def verifica_token(text_header):
    if not text_header:
        return None
    
    # Extragere username din token (format: token_secret_pentru_<username>)
    nume_user = text_header.replace('token_secret_pentru_', '')
    baza = get_db_connection()
    
    utilizator = baza.execute('SELECT id FROM users WHERE username = ?', (nume_user,)).fetchone()
    baza.close()
    
    if utilizator:
        return utilizator['id']
    
    return None

