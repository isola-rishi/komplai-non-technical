# Komplai Demo Pipeline - Setup Instructions

## 🚀 Quick Setup (Recommended)

This will create an isolated Python environment for the project:

```bash
./setup.sh
```

That's it! The script will:
- Create a virtual environment in `venv/` directory
- Install all required dependencies locally
- Keep everything isolated from your global Python installation

---

## 📦 Manual Setup

If you prefer to set up manually:

### 1. Create Virtual Environment

```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ▶️ Running the Pipeline

### Option 1: Using the run script (automatically activates venv)

```bash
./run.sh
```

### Option 2: Manual activation and run

```bash
# Activate virtual environment
source venv/bin/activate

# Run pipeline
python main_pipeline.py

# Deactivate when done
deactivate
```

---

## 📋 Installed Dependencies

All dependencies are installed in the local `venv/` folder and won't affect your global Python:

- **pandas** (2.3.3) - Data manipulation
- **pyyaml** (6.0.1) - Configuration files
- **openpyxl** (3.1.5) - Excel file operations
- **gspread** (6.2.1) - Google Sheets integration
- **oauth2client** (4.1.3) - Google authentication
- **jinja2** (3.1.6) - Template rendering
- **weasyprint** (67.0) - PDF generation (optional on Mac)
- **cffi** (2.0.0) - Foreign function interface
- **cryptography** (46.0.3) - Encryption utilities

---

## 🔧 Virtual Environment Commands

### Activate
```bash
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### Deactivate
```bash
deactivate
```

### Check if activated
When activated, you'll see `(venv)` at the start of your terminal prompt:
```
(venv) user@computer:~/demo-dummy-data$
```

### Delete and recreate (if needed)
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
demo-dummy-data/
├── venv/                    # Virtual environment (not in git)
├── requirements.txt         # Python dependencies
├── setup.sh                 # One-time setup script
├── run.sh                   # Run pipeline with venv
├── main_pipeline.py         # Main pipeline
└── ...                      # Other project files
```

---

## ✅ Verifying Setup

After running `./setup.sh`, verify everything is installed:

```bash
source venv/bin/activate
python -c "import pandas, yaml, openpyxl, gspread; print('✓ All dependencies installed!')"
```

---

## 🆘 Troubleshooting

### "Permission denied" when running ./setup.sh
```bash
chmod +x setup.sh
./setup.sh
```

### "python3: command not found"
Install Python 3.8+ from python.org or use your package manager

### WeasyPrint fails on Mac
This is expected - PDF generation will be skipped but everything else works.
The pipeline will display: `⚠ PDF Generator disabled`

### Want to use a different Python version?
```bash
python3.11 -m venv venv  # Use specific version
```

---

## 🎯 GitHub Desktop Users

After cloning:

1. Open Terminal in the project folder
2. Run: `./setup.sh`
3. Run: `python main_pipeline.py` (or use `./run.sh`)

The virtual environment is already in `.gitignore` so it won't be committed.

---

## 💡 Benefits of Virtual Environment

✅ **Isolated dependencies** - Won't conflict with other Python projects
✅ **Reproducible** - Same versions for everyone using requirements.txt
✅ **Clean uninstall** - Just delete the `venv/` folder
✅ **Multiple Python versions** - Can have different versions per project
✅ **Safe experimentation** - Test new packages without breaking system Python

---

## 🔄 Updating Dependencies

If you need to add new packages:

```bash
source venv/bin/activate
pip install package-name
pip freeze > requirements.txt  # Save updated dependencies
```

---

**You're all set! Run `./setup.sh` to get started.**
