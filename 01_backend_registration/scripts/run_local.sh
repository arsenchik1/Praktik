#!/bin/bash
cd ../01_backend_registration
python -m venv venv
source venv/Scripts/activate
pip install -r app/requirements.txt
cd app
python app.py