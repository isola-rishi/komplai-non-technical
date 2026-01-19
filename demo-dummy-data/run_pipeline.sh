#!/bin/bash
# Helper script to run the Komplai Demo Pipeline with correct environment

# Set library path for WeasyPrint on macOS
export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH

# Run the pipeline using uv
uv run python main_pipeline.py "$@"
