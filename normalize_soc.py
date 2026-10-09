import csv
import datetime
import json
import re
from pathlib import Path

from paths import RAW_DIR

DETAILS_CACHE = RAW_DIR / "details_cache.json"

SLUG_ALIASES = {
    "a10_fusion": "apple_a10", "a11_bionic": "apple_a11", "a12_bionic": "apple_a12",
    "a13_bionic": "apple_a13", "a14_bionic": "apple_a14", "a15_bionic": "apple_a15",
    "a16_bionic": "apple_a16", "a17_pro": "apple_a17_pro",
    "m1": "apple_m1", "m2": "apple_m2", "m3": "apple_m3", "m4": "apple_m4",
}
VENDOR_PREFIXES = (
    "qualcomm_", "mediatek_", "samsung_", "apple_",
    "hisilicon_", "unisoc_", "google_", "xiaomi_",
)

FIELDNAMES = [
    "soc_slug", "gpu_slug", "gpu_name",
    "antutu_gpu", "antutu_total", "antutu_version",
    "geekbench6_single", "geekbench6_multi", "rating",
    "source", "source_url", "updated", "confidence",
]


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", str(text).lower())
    return s.strip("_")


def strip_vendor(slug: str) -> str:
    for p in VENDOR_PREFIXES:
        if slug.startswith(p):
            return slug[len(p):]
    return slug


def load_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return default


def normalize_all(records: list, out_path: Path):
    details = load_json(DETAILS_CACHE, {})
    rows = {}
    today = datetime.date.today().isoformat()

    for r in records:
        raw_slug = r.get("soc_slug_raw") or slugify(r.get("soc_raw", ""))
        soc = SLUG_ALIASES.get(strip_vendor(slugify(raw_slug)), strip_vendor(slugify(raw_slug)))

        d = details.get(raw_slug, {})
        antutu_gpu = d.get("antutu_gpu") or d.get("antutu10_gpu") 

        gpu_name = (r.get("gpu_name") or "").strip() or None
        gpu_slug = slugify(gpu_name) if gpu_name else None

        if antutu_gpu:
            conf = "benchmark"
        elif r.get("antutu_total"):
            conf = "proxy_antutu_total"
        else:
            conf = "needs_review"

        rows[soc] = {
            "soc_slug": soc,
            "gpu_slug": gpu_slug or soc,
            "gpu_name": gpu_name,
            "antutu_gpu": antutu_gpu,
            "antutu_total": r.get("antutu_total"),
            "antutu_version": 11,
            "geekbench6_single": r.get("geekbench6_single"),
            "geekbench6_multi": r.get("geekbench6_multi"),
            "rating": r.get("rating"),
            "source": r.get("source", "...."), #pilih brand website yang di scraping
            "source_url": r.get("source_url"),
            "updated": today,
            "confidence": conf,
        }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        w.writerows(rows.values())
    print(f"[OK] {len(rows)} baris SoC -> {out_path}")