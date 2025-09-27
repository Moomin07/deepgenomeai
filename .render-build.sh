#!/usr/bin/env bash
# Tell Render: DO NOT USE POETRY
export RENDER_BUILD_DISABLE_POETRY=1

# Install from requirements.txt
pip install -r requirements.txt

echo "✅ Flask installed successfully!"