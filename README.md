# Movie Manager

## Descriere
Movie Manager este o aplicatie distribuita de tip Client-Server pentru gestionarea colectiilor personale de filme si seriale. Arhitectura este complet decuplata: Backend-ul expune un API REST, iar Frontend-ul (Client Web) consuma acest API pentru a oferi interfata utilizatorului. Utilizatorii pot cauta filme (TVMaze API), le pot organiza in liste (To Watch, Watching, Completed) si pot interactiona prin sistemul de prieteni.

## Link GitHub
https://github.com/krpandrei05/movie-manager-ia4

## Limbaje si tehnologii
*   **Python 3**: Limbajul principal
*   **Flask**: Framework web folosit atat pentru Server (API), cat si pentru Client (Web Server)
*   **SQLite**: Baza de date relationala (lightweight)
*   **Requests**: Biblioteca pentru comunicarea HTTP intre Client si Server
*   **HTML / CSS / JavaScript**: Interfata grafica (tema Dark Mode custom, interactiuni AJAX)

## Instructiuni rulare
1.  **Instalare dependente:**
    Se recomanda crearea unui mediu virtual.
    ```bash
    pip install -r requirements.txt
    ```

2.  **Pornire sistem (Client + Server):**
    Scriptul `start.py` porneste automat ambele procese (API pe portul 5000, Web pe 5001).
    ```bash
    python start.py
    ```

3.  **Accesare:**
    Deschideti browser-ul la: `http://localhost:5001`

*(Optional) Rulare manuala:*
*   Server: `cd server && python app.py`
*   Client: `cd client && python app.py`

## Contributii individuale

### Vlad Darie
*   Implementarea aplicatiei Client folosind Flask si template-uri Jinja2.
*   Dezvoltarea interfetei grafice (HTML, CSS custom, Responsive Design).
*   Implementarea logicii de JavaScript pentru cautare (autocomplete) si interactiuni dinamice.
*   Crearea modulului `api_client.py` pentru comunicarea cu API-ul REST.

### Carp Andrei
*   Arhitectura si implementarea Serverului API REST folosind Flask.
*   Proiectarea si gestionarea bazei de date SQLite (modele: Users, Movies, Friends, Recommendations).
*   Implementarea logicii de business si a serviciilor (Auth, integrare TVMaze API).
*   Securizarea endpoint-urilor si gestionarea sesiunilor.

## Dificultati si rezolvari

1.  **Arhitectura Client-Server**: Asigurarea unei comunicari eficiente intre Client si Server a fost o provocare. Solutia a fost definirea clara a contractului API si folosirea librariei `requests` pentru a consuma endpoint-urile expuse de backend.
2.  **Sincronizarea proceselor**: Pornirea separata a backend-ului si frontend-ului poate fi incomoda. Am rezolvat prin crearea scriptului `start.py` care foloseste `subprocess` pentru a gestiona ciclul de viata al ambelor servicii simultan.
3.  **Cross-Origin Resource Sharing (CORS)**: Clientul web si Serverul API ruleaza pe porturi diferite (5001 vs 5000), ceea ce a generat restrictii de securitate. Am rezolvat prin configurarea corecta a headers-urilor CORS in `server/app.py`.