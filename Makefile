# Makefile pentru Movie Manager (Client-Server Architecture)

help:
	@echo "Comenzi disponibile:"
	@echo "  make install    - Instaleaza dependentele Python"
	@echo "  make run        - Porneste tot sistemul (Server + Client)"
	@echo "  make run-server - Porneste doar Server-ul API (Backend)"
	@echo "  make run-client - Porneste doar Client-ul Web (Frontend)"
	@echo "  make clean      - Sterge fisierele de cache Python"

install:
	pip install -r requirements.txt

run:
	python start.py

run-server:
	cd server && python app.py

run-client:
	cd client && python app.py

clean:
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
