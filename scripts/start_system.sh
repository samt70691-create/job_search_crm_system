#!/usr/bin/env bash
set -e
python3 -m src.pipelines.run_full_setup
streamlit run app.py
