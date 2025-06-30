from pathlib import Path
import sys

# Mendapatkan path absolut dari file saat ini
FILE = Path(__file__).resolve()
ROOT = FILE.parent

# Menambahkan path root ke sys.path jika belum ada
if ROOT not in sys.path:
    sys.path.append(str(ROOT))

# Ubah path menjadi relatif terhadap working directory saat ini
ROOT = ROOT.relative_to(Path.cwd())

# Konfigurasi model ML
MODEL_DIR = ROOT / 'weights'
DETECTION_MODEL = MODEL_DIR / 'best(6).pt'
