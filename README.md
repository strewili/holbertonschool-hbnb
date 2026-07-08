# HBnB Project

## Structure
- app/ - core application code
  - api/v1/ - API endpoints (versioned)
  - models/ - business logic classes
  - services/ - Facade pattern, mediates between layers
  - persistence/ - in-memory repository (to be replaced by a DB-backed one)
- run.py - entry point
- config.py - environment/app configuration
- requirements.txt - dependencies

## Setup
pip install -r requirements.txt
python run.py
