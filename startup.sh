#!/bin/bash
cd /workspace/comfyui
python main.py &

cd /workspace/app
python app.py
