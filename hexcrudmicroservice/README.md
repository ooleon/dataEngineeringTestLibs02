# Hexagonal CRUD Microservice

## Requisitos
- Python >= 3.11
- `uv` o `pip`

## Instalación
```bash
```
cd hex_crud_microservice
python -m venv .venv && source .venv/bin/activate
pip install .
# o con uv: uv pip install .
cp .env.example .env
# Edita .env según tu infraestructura
PYTHONPATH=src uvicorn src.main:app --reload
PYTHONPATH=src pytest src/tests -v

## ejecución
# 1. Clonar/Generar proyecto
python generate_project.py
cd hex_crud_microservice
cp .env.example .env

# 2. Levantar infraestructura base (solo caché)
make up-cache

# 3. Probar localmente sin infra completa
CACHE_BACKEND=valkey CACHE_URL=redis://localhost:6379 LOG_BACKEND=console \
  uv run uvicorn src.main:app --reload

# 4. Levantar stack completo
make build
make up

# 5. Ejecutar tests de integración (spin up/down automático)
make test

# 6. Verificar salud y métricas
curl -s http://localhost:8000/docs | grep "swagger"
docker compose ps --format "table {{.Name}}\t{{.Status}}"