#!/bin/bash
# Setup script for Komplai Demo Pipeline

echo "======================================================================"
echo "  KOMPLAI DEMO PIPELINE - SETUP"
echo "======================================================================"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✓ Virtual environment already exists"
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

echo ""
echo "Activating virtual environment..."

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "✗ Error: Could not find venv/bin/activate"
    exit 1
fi

echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "======================================================================"
echo "  SETUP COMPLETE!"
echo "======================================================================"
echo ""
echo "To use the pipeline:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the pipeline:"
echo "     python main_pipeline.py"
echo ""
echo "  3. When done, deactivate:"
echo "     deactivate"
echo ""
