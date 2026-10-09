# ShaderBench Convert

Hilir dari [`shaderbench-scraper`](https://github.com/<USERNAME>/shaderbench-scraper),
hulu dari [`shaderbench-build`](https://github.com/<USERNAME>/shaderbench-build):
mengubah skor benchmark mentah (AnTuTu/GeekBench/3DMark/Cinebench) menjadi
`gpu_index` / `cpu_index` terkalibrasi dalam CSV staging.

## Pengertian Kode
| File | Tanggung jawab |
|---|---|
| `convert/normalize.py` | `normalize_all(raw, out_csv)`: bridge skor SoC mobile → index (anchor perangkat referensi, clipping, dedup). |
| `convert/normalize_pc.py` | `normalize_pc_all(raw, cpu_csv, gpu_csv)`: bridge skor PC per form (desktop/laptop) → index CPU & GPU. |

## Cara Kerja
```
scraper: parsed.json / parsed_pc.json  ──►  normalize_*()  ──►  data/staging/*.csv  ──►  build/backend
```
Dipanggil otomatis oleh `scraper/run_scrape.py`; bisa juga dijalankan manual
dengan me-load raw JSON sendiri.

## Penjelasan Lanjutan
- Anchor & skala dipilih agar konsisten dengan `TARGET_FPS=45` dan `BASE` di inference;
  mengubah anchor = mengubah seluruh kurva prediksi → lakukan lewat pengukuran, bukan tebakan.
- Kolom output adalah **kontrak** yang dibaca tooling backend/build; jangan ganti nama kolom.

## Setup (paths & data dibuat sendiri)
Ikuti blok tutorial **SETUP** (Langkah 1–2): buat `paths.py` di root workspace dan
biarkan `data/staging/` dibuat otomatis. Repo ini tidak butuh `api/` → aman standalone.

## Menjalankan (manual, tanpa scraper)
```python
from convert.normalize import normalize_all
import json
raw = json.load(open("data/raw/parsed.json", encoding="utf-8"))
normalize_all(raw, "data/staging/benchmark_soc.csv")
```