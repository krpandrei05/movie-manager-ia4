Movie Manager este o aplicatie web pentru gestionarea filmelor, serialelor si show-urilor TV. Aplicatia permite utilizatorilor sa isi creeze conturi, sa adauge filme in trei liste diferite si sa interactioneze cu alti utilizatori prin sistemul de prieteni si recomandari.

Functionalitatile principale includ crearea de conturi cu autentificare securizata, adaugarea de filme prin cautare integrata cu TVMaze API, mutarea filmelor intre liste, notarea filmelor din lista Completed, sistem de prieteni si recomandari de filme intre prieteni.

Aplicatia este structurata in doua parti principale. Backend-ul ruleaza pe portul 5000 si ofera un API REST si gestioneaza baza de date SQLite. Frontend-ul ruleaza pe portul 5001 si ofera interfata web cu pagini HTML generate dinamic folosind Jinja2 templates.

Link GitHub: https://github.com/krpandrei05/movie-manager-ia4

Pentru partea de backend am folosit Python 3 cu framework-ul Flask. Flask este un framework web care ne-a permis sa cream API-ul REST. Am folosit Flask pentru a crea rutele API, pentru a gestiona request-urile HTTP si pentru a returna raspunsuri in format JSON.

Pentru baza de date am folosit SQLite pentru ca este simplu, nu necesita instalare separata si este suficient pentru un proiect de acest tip. SQLite stocheaza datele intr-un fisier local, ceea ce face aplicatia usor de rulat fara sa fie nevoie de un server de baza de date separat. Am creat patru tabele: users pentru utilizatori, movies pentru filme, friends pentru relatiile de prietenie si recommendations pentru recomandari.

Pentru securitate am folosit Werkzeug care vine cu Flask. Werkzeug ofera functii pentru criptarea parolelor folosind hash-uri securizate. Am folosit generate_password_hash pentru a cripta parolele la inregistrare si check_password_hash pentru a verifica parolele la login.

Pentru integrarea cu API-urile externe am folosit biblioteca standard urllib din Python. Am facut request-uri HTTP catre TVMaze API pentru a cauta filme. TVMaze este un API gratuit care nu necesita cheie API.

Pentru partea de frontend am folosit tot Flask cu Jinja2 templates. Jinja2 este template engine-ul care vine cu Flask si permite generarea dinamica a paginilor HTML. Am creat template-uri pentru fiecare pagina: login, register, dashboard, friends, recommendations si friend profile.

Pentru stilizare am scris CSS manual fara sa folosim framework-uri externe precum Bootstrap. Am ales tema dark pentru ca arata mai modern si este mai usor pentru ochi. Am creat stiluri pentru toate componentele: sidebar-ul de navigare, listele de filme, butoanele, formularele, dropdown-urile si dialog-urile de confirmare.

Pentru interactiunile in timp real am folosit JavaScript. JavaScript-ul este folosit pentru autocomplete-ul de la cautarea filmelor, pentru ca aceasta functionalitate necesita request-uri in timp real catre backend pe masura ce utilizatorul scrie. Am implementat un sistem de debounce care asteapta 300 de milisecunde dupa ce utilizatorul a oprit sa scrie inainte de a face request-ul, pentru a nu face prea multe request-uri inutile. Am folosit si JavaScript pentru gestionarea dialog-ului de confirmare pentru stergerea filmelor.

Am folosit si biblioteca requests in Python, desi in final frontend-ul comunica direct cu backend-ul prin import-uri Python, nu prin HTTP requests. Requests este inclus in requirements.txt pentru ca am avut initial planuri sa folosim comunicare prin HTTP, dar am schimbat abordarea pentru simplitate.

Pentru a rula aplicatia, primul pas este sa instalezi dependentele Python. Ruleaza comanda pip install -r requirements.txt in folderul principal al proiectului. Aceasta comanda va instala Flask versiunea 3.0.0, Werkzeug versiunea 3.0.1 si requests versiunea 2.31.0. Asigura-te ca ai Python 3.8 sau o versiune mai noua instalata pe sistem.

Dupa instalarea dependentelor, poti rula aplicatia in doua moduri. Primul mod este cel mai simplu si recomandat: ruleaza python start.py din folderul principal. Acest script porneste automat ambele servere necesare pentru aplicatie. Backend-ul va porni pe portul 5000 si frontend-ul pe portul 5001. Scriptul initializeaza si baza de date SQLite automat la prima rulare, creand toate tabelele necesare in folderul backend/instance/production.db.

Al doilea mod de rulare este sa pornesti manual fiecare server in terminale separate. Intr-un terminal, navigheaza la folderul proiectului si ruleaza python backend/app.py. Acest lucru va porni backend-ul pe portul 5000. Backend-ul va crea automat baza de date daca nu exista deja. Intr-un al doilea terminal, ruleaza python frontend/app.py pentru a porni frontend-ul pe portul 5001. Important: trebuie sa pornesti backend-ul inainte de frontend, pentru ca frontend-ul are nevoie de backend pentru a functiona.

Dupa ce ambele servere ruleaza, deschide browser-ul la adresa http://localhost:5001. Acolo vei vedea pagina de login. Daca nu ai deja un cont, poti crea unul nou apasand pe butonul Sign Up. La inregistrare trebuie sa introduci un username de cel putin 3 caractere si o parola de cel putin 3 caractere. Dupa crearea contului, te poti loga cu username-ul si parola.

Dupa login, vei ajunge pe dashboard-ul principal unde poti vedea cele trei liste de filme: To Watch, Watching si Completed. Pentru a adauga un film, scrie numele filmului in caseta de cautare de sus. Aplicatia va cauta automat filme pe masura ce scrii si va afisa rezultatele intr-un dropdown. Selecteaza un film din dropdown pentru a-l adauga in lista To Watch. Nu poti adauga un film daca nu il selectezi din dropdown, pentru a evita erorile.

Pentru a muta un film intre liste, apasa pe butoanele corespunzatoare: To Watch, Watching sau Completed. Pentru a nota un film din lista Completed, selecteaza o nota de la 1 la 10 din dropdown-ul de rating. Pentru a sterge un film, apasa pe butonul Delete. Va aparea un dialog de confirmare unde trebuie sa apesi Yes pentru a confirma stergerea.

In sidebar-ul din stanga poti naviga intre pagini. Pagina Friends iti permite sa adaugi prieteni prin username si sa vezi lista cu toti prietenii tai. Daca apesi pe un prieten din lista, vei vedea toate filmele lui organizate pe cele trei liste. De acolo poti recomanda filme prietenului tau folosind caseta de cautare. Pagina Recommendations iti arata toate recomandarile primite de la prieteni, pe care le poti sterge dupa ce le-ai vazut.

Pentru a te deconecta, apasa pe butonul Logout din partea de jos a sidebar-ului. Pentru a opri serverele, apasa Ctrl+C in terminal. Daca ai folosit start.py, ambele servere se vor opri odata. Daca ai pornit serverele manual, trebuie sa opresti fiecare terminal separat.

Vlad Darie:
- Am lucrat la folderul frontend si am implementat toate functionalitatile de pe partea de interfata web
- Am creat toate paginile HTML folosind Jinja2 templates: pagina de login, pagina de inregistrare, dashboard-ul principal cu cele trei liste de filme, pagina de prieteni, pagina de recomandari si pagina de profil pentru prieteni
- Am scris tot CSS-ul pentru stilizarea aplicatiei, creand tema dark si stilurile pentru toate componentele: sidebar-ul, butoanele, formularele, listele de filme, dropdown-urile si dialog-urile
- Am implementat JavaScript-ul pentru autocomplete-ul de la cautarea filmelor, care face request-uri catre backend pe masura ce utilizatorul scrie, implementeaza debounce pentru a nu face prea multe request-uri, si gestioneaza afisarea si ascunderea dropdown-ului cu rezultate
- Am implementat functionalitatea pentru dialog-ul de confirmare custom folosit la stergerea filmelor si recomandarilor
- Am creat toate view-urile Flask din folderul frontend/views: auth_views.py pentru autentificare, dashboard_views.py pentru gestionarea filmelor si friend_views.py pentru prieteni si recomandari, care proceseaza formularele, valideaza datele, comunica cu backend-ul si returneaza paginile HTML corespunzatoare
- Am implementat sistemul de sesiuni Flask pentru autentificare persistenta si am adaugat validari pentru a preveni adaugarea de filme duplicate
- Am creat utilitarele din frontend/utils: validators.py pentru validarea input-urilor si api_client.py pentru comunicarea cu backend-ul prin HTTP, desi in final nu s-a folosit in mod activ
- Am configurat app.py din frontend pentru a inregistra toate blueprint-urile si a seta ruta root pentru redirect la login sau dashboard

Carp Andrei:
- Am lucrat la folderul backend si am implementat toate functionalitatile de pe partea de API si logica de business
- Am creat structura bazei de date SQLite cu toate cele patru tabele necesare: users pentru utilizatori, movies pentru filme, friends pentru relatiile de prietenie si recommendations pentru recomandari
- Am implementat functiile din models/database.py pentru gestionarea conexiunii la baza de date si initializarea tabelelor
- Am creat toate rutele API din folderul routes: auth_routes.py pentru autentificare cu endpoint-uri pentru register si login, movie_routes.py pentru gestionarea filmelor cu endpoint-uri pentru adaugare, mutare intre liste, notare si stergere, si friend_routes.py pentru prieteni si recomandari cu endpoint-uri pentru adaugare prieteni, vizualizare filme prieteni, trimitere recomandari si gestionare recomandari
- Am implementat serviciile din folderul services: auth_service.py pentru logica de autentificare cu criptarea parolelor folosind Werkzeug si validarea datelor, si external_api.py pentru integrarea cu TVMaze API
- Am creat functia search_movies care face request-uri catre TVMaze, proceseaza rezultatele si le returneaza intr-un format compatibil cu aplicatia
- Am implementat security.py pentru verificarea token-urilor de autentificare, unde token-urile sunt simple si au formatul token_secret_pentru_username, iar functia verifica_token extrage username-ul din token si verifica daca utilizatorul exista in baza de date
- Am configurat app.py din backend pentru a inregistra toate blueprint-urile cu prefix-ul /api, am adaugat CORS headers pentru a permite comunicarea cu frontend-ul, si am creat endpoint-ul pentru cautarea filmelor si health check
- Am setat initializarea bazei de date la pornirea serverului

Amandoi am lucrat la start.py pentru a crea un script care porneste automat ambele servere. Scriptul foloseste subprocess pentru a rula fiecare server in propriul proces si afiseaza output-ul ambelor servere in consola.

Prima dificultate majora a fost coordonarea intre cei doi membri ai echipei pentru a lucra pe parti separate ale proiectului. Darie Vlad a lucrat pe frontend si Carp Andrei pe backend, asa ca a trebuit sa ne asiguram ca interfetele dintre cele doua parti sunt clare si bine definite. Am stabilit de la inceput ce format de date se transmite intre frontend si backend si am documentat endpoint-urile API pentru a ne coordona mai bine.

O dificultate pe partea de backend a fost structurarea API-ului REST. A trebuit sa ne gandim la ce endpoint-uri sunt necesare, ce metode HTTP sa folosim pentru fiecare operatie si ce format de date sa returnam. Am ales sa folosim blueprint-uri in Flask pentru a separa rutele pe categorii: autentificare, filme si prieteni. Aceasta organizare a facut codul mai clar si mai usor de inteles.

Pentru baza de date, a trebuit sa ne gandim la structura tabelelor si la relatiile dintre ele. Am ales sa facem prietenia bidirectionala, adica cand utilizatorul A adauga utilizatorul B ca prieten, se creeaza doua inregistrari in tabelul friends: una cu user_id=A si friend_id=B si alta cu user_id=B si friend_id=A. Aceasta abordare a simplificat interogarile pentru a gasi toti prietenii unui utilizator.

O alta dificultate pe partea de backend a fost integrarea cu TVMaze API. TVMaze returneaza date intr-un format diferit fata de ce ne asteptam initial. Am trebuit sa procesam rezultatele si sa le transformam intr-un format compatibil cu aplicatia noastra. Am creat o functie care extrage informatiile relevante din raspunsul TVMaze si le formateaza corespunzator.

Pentru frontend, o dificultate majora a fost comunicarea cu backend-ul. Initial am planuit sa folosim doar HTTP requests, dar am realizat ca e mai simplu sa importam direct modulele din backend in frontend, pentru ca ambele ruleaza pe acelasi sistem. Am adaugat backend-ul in path-ul Python al frontend-ului si am putut importa direct functiile necesare. Aceasta abordare a simplificat mult codul si a eliminat necesitatea de a face request-uri HTTP intre cele doua parti.

Pentru autocomplete-ul de la cautarea filmelor am avut nevoie de JavaScript pentru ca trebuia sa facem request-uri in timp real. Am implementat un sistem de debounce care asteapta 300 de milisecunde dupa ce utilizatorul a oprit sa scrie inainte de a face request-ul, pentru a nu face prea multe request-uri catre TVMaze API. Am gestionat si cazurile in care request-ul esueaza sau nu gaseste rezultate.

O problema importanta a fost validarea filmelor. Am vrut sa ne asiguram ca utilizatorii nu pot adauga filme cu nume gresite sau goale. Am implementat un sistem cu un camp hidden numit movie_validated care se seteaza doar cand utilizatorul selecteaza un film din dropdown. JavaScript-ul seteaza acest camp la valoarea 1 cand utilizatorul face click pe un rezultat din dropdown. Backend-ul verifica acest camp inainte de a permite adaugarea filmului. Daca campul nu este setat corect, se returneaza un mesaj de eroare si se face redirect inapoi la dashboard.

Pentru stergerea filmelor am avut o problema cu dialogul de confirmare. Initial nu functiona corect pentru ca formularul nu se trimitea dupa confirmare. Problema era ca functia showConfirmDialog nu era disponibila in scope-ul corect. Am rezolvat mutand scriptul cu functia in afara block-ului de scripts din template-ul de baza, pentru a fi disponibil global. Apoi am folosit submit direct al formularului dupa confirmare.

O alta problema a fost cu duplicatele. Initial utilizatorii puteau adauga acelasi film de mai multe ori in liste. Am adaugat o verificare in backend care verifica daca filmul exista deja pentru utilizatorul curent inainte de a-l adauga. Verificarea se face dupa validarea campului movie_validated si inainte de inserarea in baza de date. Daca filmul exista deja, se returneaza un mesaj de eroare si se face redirect.

Pentru design am ales tema dark pentru ca arata mai modern si este mai usor pentru ochi. Am creat toate stilurile manual in CSS, fara sa folosim framework-uri externe. Aceasta abordare ne-a dat control complet asupra design-ului dar a necesitat mai mult timp pentru a crea stilurile pentru toate componentele. Am avut grija sa facem butoanele de login si sign up de aceeasi dimensiune si sa fie pe acelasi rand, ceea ce a necesitat ajustari multiple in CSS.

O dificultate a fost gestionarea sesiunilor Flask. Am trebuit sa ne asiguram ca sesiunile sunt setate corect la login si sunt verificate pe toate paginile care necesita autentificare. Am creat o functie require_auth care verifica daca utilizatorul este autentificat si face redirect la login daca nu este. Aceasta functie este apelata la inceputul fiecarui view care necesita autentificare.

Pentru scriptul start.py am avut probleme initial cu threading-ul. Flask nu functioneaza bine in thread-uri pentru ca reloader-ul sau poate cauza probleme. Am schimbat abordarea si am folosit subprocess pentru a rula fiecare server in propriul proces. Aceasta solutie a functionat mult mai bine si a permis afisarea corecta a output-ului ambelor servere.
