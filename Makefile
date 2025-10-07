# Makefile para facilitar comandos comuns do projeto

.PHONY: help install test clean data notebooks format lint

help:  ## Mostra esta mensagem de ajuda
	@echo "Comandos dispon├¡veis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Instala depend├¬ncias do projeto
	pip install -r requirements.txt
	pip install -e .

install-dev:  ## Instala depend├¬ncias de desenvolvimento
	pip install -r requirements.txt
	pip install -e ".[dev]"

test:  ## Executa testes
	pytest tests/ -v

test-cov:  ## Executa testes com cobertura
	pytest tests/ --cov=src --cov-report=html --cov-report=term

clean:  ## Remove arquivos tempor├írios e cache
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

data:  ## Processa todos os datasets
	python src/data/load_ecommerce.py
	python src/data/load_retail.py
	python src/data/load_sales_data.py

features:  ## Cria features
	python src/features/build_features.py

notebooks:  ## Inicia Jupyter Notebook
	jupyter notebook

lab:  ## Inicia JupyterLab
	jupyter lab

format:  ## Formata c├│digo com black
	black src/ tests/

lint:  ## Verifica c├│digo com flake8
	flake8 src/ tests/ --max-line-length=100

validate:  ## Valida qualidade dos dados
	python src/data/data_validator.py

structure:  ## Mostra estrutura do projeto
	tree -L 3 -I '__pycache__|*.pyc|.ipynb_checkpoints'

# Windows: use 'tree /F /A' em vez de 'tree -L 3'

