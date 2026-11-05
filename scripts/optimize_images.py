#!/usr/bin/env python3
"""Generate WebP + responsive-width variants for every raster image under assets/.

    python3 scripts/optimize_images.py            # create / refresh variants + manifest
    python3 scripts/optimize_images.py --check    # exit 1 if anything is stale (CI / pre-commit)
    python3 scripts/optimize_images.py --dry-run  # show what would change
    python3 scripts/optimize_images.py --snippet assets/photos/hero-golden.jpg \
        --sizes "100vw" --alt "Banwag at golden hour" [--loading eager|hero] [--style "..."]

What it does
  * For each .jpg/.jpeg/.png/.webp source it writes up to three WebP files next
    to it, named  <stem>.<width>w.webp  (e.g. hero-golden.480w.webp).
    Originals are never modified or deleted (Decap CMS, press kits and the
    lightbox still point at them).
  * Widths come from a per-folder profile (see PROFILES). A width is only used if
    it is smaller than the source; if the source is <= the largest profile width
    its native width is added, so nothing is ever upscaled.
  * EXIF (incl. any GPS tags) is dropped from the variants and orientation is applied.
  * It writes _data/images.json, which Jekyll exposes as site.data.images. The
    _includes/picture.html include uses it to emit <picture>/srcset with the
    real width/height. Images missing from the manifest (e.g. a fresh Decap CMS
    upload) still render, as a plain lazy <img>, until this script is re-run.
  * Re-running is cheap and deterministic: a variant is skipped when the source's
    SHA-1 (stored in the manifest) is unchanged and the file exists.

Only Pillow is required:  pip install Pillow
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
MANIFEST = ROOT / "_data" / "images.json"

SOURCE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
VARIANT_RE = re.compile(r"\.\d+w\.webp$")  # our own output; never treated as a source

# Per-folder settings. First matching prefix wins; "" is the default.
#   widths   – target widths (px), ascending
#   lossless – True for line art / text (drawings) where lossy WebP smears edges
#   quality  – WebP quality for lossy output
PROFILES = [
    # 12000x8000 scan with fine map labels, shown at ~full content width: allow a larger top width
    ("assets/photos/landas-masterplan", dict(widths=(960, 1600, 2400), lossless=False, quality=80)),
    ("assets/logos/",    dict(widths=(128, 256, 512),  lossless=False, quality=82)),
    ("assets/drawings/", dict(widths=(924,),           lossless=True,  quality=100)),
    ("",                 dict(widths=(480, 960, 1600), lossless=False, quality=76)),
]

# Pillow refuses >89 MP by default; assets/ includes a 96 MP masterplan scan we
# own and trust, so lift the guard for this script only.
Image.MAX_IMAGE_PIXELS = None


def profile_for(rel: str) -> dict:
    for prefix, prof in PROFILES:
        if rel.startswith(prefix):
            return prof
    raise AssertionError  # unreachable: "" matches


def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


def iter_sources():
    for p in sorted(ASSETS.rglob("*")):
        if p.is_file() and p.suffix.lower() in SOURCE_EXT and not VARIANT_RE.search(p.name):
            yield p


def pick_widths(src_w: int, targets) -> list[int]:
    widths = [w for w in targets if w < src_w]
    if src_w <= targets[-1]:
        widths.append(src_w)  # native size, no upscale
    return widths


def variant_path(src: Path, w: int) -> Path:
    return src.with_name(f"{src.stem}.{w}w.webp")


def make_variant(im: Image.Image, w: int, dest: Path, prof: dict) -> None:
    h = round(im.height * w / im.width)
    out = im if w == im.width else im.resize((w, h), Image.LANCZOS)
    kw = dict(method=6)
    if prof["lossless"]:
        kw.update(lossless=True, quality=100)
    else:
        kw.update(quality=prof["quality"], alpha_quality=90)
    out.save(dest, "WEBP", **kw)  # no exif/icc passed => stripped


def load_manifest() -> dict:
    try:
        return json.loads(MANIFEST.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def process(args) -> int:
    old = load_manifest()
    new: dict = {}
    stale = 0
    written = 0
    before = after = 0
    for src in iter_sources():
        rel = src.relative_to(ROOT).as_posix()
        digest = sha1(src)
        prev = old.get(rel)
        with Image.open(src) as probe:
            src_w, src_h = ImageOps.exif_transpose(probe).size if probe.getexif().get(0x0112, 1) in (5, 6, 7, 8) else probe.size
        prof = profile_for(rel)
        widths = pick_widths(src_w, prof["widths"])
        files = {w: variant_path(src, w) for w in widths}
        up_to_date = (
            not args.force
            and prev
            and prev.get("sha1") == digest
            and [v["w"] for v in prev.get("variants", [])] == widths
            and all(f.exists() for f in files.values())
        )
        if not up_to_date:
            stale += 1
            if args.check or args.dry_run:
                print(f"{'STALE' if args.check else 'would build'}: {rel} -> {widths}")
            else:
                with Image.open(src) as im:
                    im = ImageOps.exif_transpose(im)
                    has_alpha = im.mode in ("RGBA", "LA", "P") and (im.mode != "P" or "transparency" in im.info)
                    im = im.convert("RGBA" if has_alpha else "RGB")
                    for w, dest in files.items():
                        make_variant(im, w, dest, prof)
                        written += 1
        before += src.stat().st_size
        after += sum(f.stat().st_size for f in files.values() if f.exists())
        new[rel] = dict(
            w=src_w, h=src_h, sha1=digest,
            variants=[dict(w=w, src=variant_path(src, w).relative_to(ROOT).as_posix()) for w in widths],
        )

    # Orphans: variants no longer produced for any source (source gone or profile changed).
    # Reported, never auto-deleted.
    wanted = {v["src"] for m in new.values() for v in m["variants"]}
    for p in sorted(ASSETS.rglob("*.webp")):
        rel = p.relative_to(ROOT).as_posix()
        if VARIANT_RE.search(p.name) and rel not in wanted:
            print(f"orphan variant (safe to delete): {rel}")

    if args.check:
        if new != old:
            print("_data/images.json is out of date")
            stale = stale or 1
        print("OK: all variants up to date" if not stale else f"{stale} image(s) need `python3 scripts/optimize_images.py`")
        return 1 if stale else 0
    if args.dry_run:
        print(f"{stale} image(s) would be (re)built")
        return 0

    MANIFEST.parent.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps(new, indent=1, sort_keys=True) + "\n")
    print(f"{len(new)} sources, {written} variants written; originals {before/1e6:.1f} MB -> variants {after/1e6:.1f} MB")
    return 0


# --------------------------------------------------------------------------- #
# Markup helper – same output as _includes/picture.html, for hand-edited pages  #
# that Jekyll does not template (index.html, banwag.html, ... have no front     #
# matter because their {{ }} belong to the dc-runtime, not Liquid).             #
# --------------------------------------------------------------------------- #
def picture_html(src: str, alt: str, sizes: str = "100vw", loading: str = "lazy",
                 style: str = "", cls: str = "", prefix: str = "", extra: str = "") -> str:
    """loading: "lazy" (below the fold), "eager" (above the fold) or "hero" (LCP image:
    eager + fetchpriority=high). `prefix` is prepended to every URL ("" for the
    root-relative-less paths the static pages use, "/" for root-relative)."""
    key = src.lstrip("/")
    meta = load_manifest().get(key)
    attrs = f'alt="{html.escape(alt, quote=True)}"'
    if cls:
        attrs += f' class="{cls}"'
    if style:
        attrs += f' style="{style}"'
    attrs += {"lazy": ' loading="lazy" decoding="async"',
              "eager": ' decoding="async"',
              "hero": ' fetchpriority="high" decoding="async"'}[loading]
    if extra:
        attrs += " " + extra
    if not meta:
        return f'<img src="{prefix}{key}" {attrs}>'
    srcset = ", ".join(f'{prefix}{v["src"]} {v["w"]}w' for v in meta["variants"])
    return (f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
            f'<img src="{prefix}{key}" width="{meta["w"]}" height="{meta["h"]}" {attrs}></picture>')


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="exit 1 if variants/manifest are stale; writes nothing")
    ap.add_argument("--dry-run", action="store_true", help="list work without writing")
    ap.add_argument("--force", action="store_true", help="rebuild every variant")
    ap.add_argument("--snippet", metavar="ASSET", help="print <picture> markup for one asset and exit")
    ap.add_argument("--alt", default="")
    ap.add_argument("--sizes", default="100vw")
    ap.add_argument("--style", default="")
    ap.add_argument("--loading", choices=("lazy", "eager", "hero"), default="lazy",
                    help="lazy (default, below the fold) | eager (above the fold) | hero (LCP: eager + fetchpriority=high)")
    ap.add_argument("--prefix", default="", help='URL prefix, e.g. "/" for root-relative paths')
    args = ap.parse_args()
    if args.snippet:
        print(picture_html(args.snippet, args.alt, args.sizes, args.loading, args.style, prefix=args.prefix))
        return 0
    return process(args)


if __name__ == "__main__":
    sys.exit(main())
