#!/bin/bash
# Komplai Demo Pipeline - Quick Run Script

echo "======================================================================"
echo "  KOMPLAI DEMO DATA PIPELINE"
echo "======================================================================"
echo ""

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠ Virtual environment not found. Running setup first..."
    ./setup.sh
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting pipeline execution..."
echo ""

# Run the pipeline
python main_pipeline.py

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "======================================================================"
    echo "  ✓ PIPELINE COMPLETED SUCCESSFULLY"
    echo "======================================================================"
    echo ""
    echo "Next steps:"
    echo "  1. Check Excel file: Komplai_Demo_Master (Claude).xlsx"
    echo "  2. Check PDFs in: ./output/pdfs/"
    echo "  3. Share Google Sheet to enable sync (see COMPLETION_SUMMARY.md)"
    echo ""
else
    echo ""
    echo "======================================================================"
    echo "  ✗ PIPELINE FAILED - Check error messages above"
    echo "======================================================================"
    echo ""
    exit 1
fi
