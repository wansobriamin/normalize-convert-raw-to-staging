import csv
import datetime
from pathlib import Path


CPU_FIELDS = [
    "cpu_slug", "name", "form_factor",
    "cb_single", "cb_multi", "rating", "primary_score",
    "source", "source_url", "updated", "confidence",
]
GPU_FIELDS = [
    "gpu_slug", "name", "form_factor",
    "score_3dmark", "score_geekbench", "tflops", "rating", "primary_score",
    "source", "source_url", "updated", "confidence",
]


def _write(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def normalize_pc_all(records: list, cpu_out: Path, gpu_out: Path):
    cpu_rows, gpu_rows = [], []
    today = datetime.date.today().isoformat()

    for r in records:
        base = {
            "name": (r.get("name_raw") or "").strip(),
            "form_factor": r.get("form_factor"),
            "rating": r.get("rating"),
            "primary_score": r.get("primary_score"),
            "source": r.get("source"),
            "source_url": r.get("source_url"),
            "updated": today,
            "confidence": "....", #pilih brand website yang di scraping
        }
        if r.get("kind") == "cpu":
            cpu_rows.append({
                **base,
                "cpu_slug": r.get("slug_raw"),
                "cb_single": r.get("cb_single"),
                "cb_multi": r.get("cb_multi"),
            })
        else:
            gpu_rows.append({
                **base,
                "gpu_slug": r.get("slug_raw"),
                "score_3dmark": r.get("score_3dmark"),
                "score_geekbench": r.get("score_geekbench"),
                "tflops": r.get("tflops"),
            })

    _write(cpu_out, CPU_FIELDS, cpu_rows)
    _write(gpu_out, GPU_FIELDS, gpu_rows)
    print(f"[OK] PC CPU: {len(cpu_rows)} baris -> {cpu_out}")
    print(f"[OK] PC GPU: {len(gpu_rows)} baris -> {gpu_out}")