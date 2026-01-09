# Makefile pentru Movie Manager

help:
	@echo "Comenzi disponibile:"
	@echo "  make install    - Instaleaza dependentele Python"
	@echo "  make run        - Porneste ambele servere (backend si frontend)"
	@echo "  make run-backend - Porneste doar backend-ul"
	@echo "  make run-frontend - Porneste doar frontend-ul"
	@echo "  make clean      - Sterge fisierele de cache Python"

install:
	pip install -r requirements.txt

run:
	python start.py

run-backend:
	cd backend && python app.py

run-frontend:
	cd frontend && python app.py

clean:
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
