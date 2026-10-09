# Normalize & Convert: Raw to Staging

Repository ini berisi skrip dan modul yang bertugas mengubah data mentah hasil *web scraping* spesifikasi hardware menjadi format yang terstruktur, bersih menjadi format `.csv`

Data spesifikasi hardware dari berbagai sumber web seringkali memiliki format penamaan yang tidak konsisten, satuan yang berbeda, dan struktur yang berantakan. Repository ini menjembatani data mentah tersebut agar sesuai dan digunakan oleh backend ShaderBench, sehingga kalkulasi *gpu_index* dan *cpu_index* dapat berjalan akurat.

---

## 🌟 Apa itu ShaderBench?
[ShaderBench](https://ShaderBench.com) adalah alat analisis performa dan rekomendasi setting Minecraft berbasis web. Alih-alih hanya memberikan tebakan, aplikasi ini menggunakan pendekatan provenance-first (jujur terhadap asal-usul data) dan model fisika satu-skalar yang dipadukan dengan Machine Learning (Random Forest).

---

### 🛠️ Komponen Utama
1. **Convert Scraper**
   Utilitas untuk membaca file mentah (JSON/CSV/HTML) hasil *scraper*, membuang *noise* (tag HTML, karakter anomali), dan mengubahnya ke dalam struktur dictionary dasar yang seragam sebelum masuk ke tahap normalisasi.
2. **Normalize SoC (System on Chip)**
   Modul khusus untuk memproses data chipset mobile (Android & iOS). Melakukan standarisasi nama (misal: *"Snapdragon 8 Gen 2"*), ekstraksi arsitektur CPU/GPU, dan pemetaan *performance index* berdasarkan benchmark (AnTuTu/Geekbench) ke dalam skala abstrak ShaderBench.
3. **Normalize PC**
   Modul untuk memproses data komponen PC (VGA/GPU dan Prosesor). Membersihkan nama varian (misal: *"NVIDIA GeForce RTX 3060 Laptop GPU"* ➔ `nvidia_rtx_3060_laptop`), menentukan *form factor* (desktop/laptop), dan menghitung *index score* (berdasarkan 3DMark/PassMark) untuk kalkulasi beban.

---

> | Repo | URL | Peran |
> |---|---|---|
> | **scraper** (ini) | [`Scraper`](https://github.com/wansobriamin/scraper-data-gpu-cpu-soc) | Scrape benchmark mentah |
> | **convert** | [`convert`](https://github.com/wansobriamin/normalize-convert-raw-to-staging) | Skor mentah → `gpu_index`/`cpu_index` (CSV staging) |
> | **build** | [`build`](https://github.com/<USERNAME>/shaderbench-build) | Kalibrasi beban shader + QC 3 lapis → DB final |

## Cara Kerja (Workflow)

```text
[ Sumber Data (web benchmark device) ]
                  │
                  ▼
      1. EXTRACT (Scraper)
         Mengambil data mentah (HTML/JSON)
                  │
                  ▼
      2. CONVERT (run_scraper.py)
         Parsing struktur dasar, buang noise
                  │
                  ▼
      3. NORMALIZE (normalize_soc.py / normalize_pc.py)
         Standarisasi nama ➔ Slug (nvidia_rtx_3060)
         Kalkulasi Index ➔ gpu_index / cpu_index
                  │
                  ▼
      4. LOAD (Staging Database)
         Export ke JSON/CSV bersih
```
---

## Etika & Lisensi

- kode ini bertugas mengubah data mentah hasil scraper menjadi data bersih
  mengagregasi untuk riset pribadi dan pengembangan ShaderBench.
- Kode ini disediakan apa adanya (as-is) untuk tujuan edukasi.

Copyright (c) 2026 wansobriamin
