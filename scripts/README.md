# scripts/

Developer tooling. Not published (excluded in `_config.yml`).

## `optimize_images.py` — responsive WebP variants

```bash
pip install Pillow
python3 scripts/optimize_images.py            # build/refresh variants + _data/images.json
python3 scripts/optimize_images.py --check    # CI/pre-commit: exit 1 if anything is stale
python3 scripts/optimize_images.py --snippet assets/photos/x.jpg --sizes "100vw" --alt "..." [--loading eager|hero]
```

Run it after adding or replacing any image under `assets/` (including Decap CMS uploads) and commit the
generated `*.<width>w.webp` files plus `_data/images.json`. Originals are never touched.

* **Jekyll-rendered pages** (`_layouts/post.html`, `news/index.html`) use `{% include picture.html src=… %}`,
  which reads `_data/images.json`. An image with no variants yet still renders as a plain lazy `<img>`.
* **Static pages** (`index.html`, `banwag.html`, … — they have no front matter because `{{ }}` belongs to the
  dc-runtime, not Liquid) contain pre-rendered `<picture>` markup; generate more with `--snippet`.
* Every page's CSS needs `picture{display:contents}source{display:none}` so the wrapper adds no box.
* Above the fold → `loading=eager|hero`; everything else lazy (the default).

## `measure_page_weight.js` — page-weight check

```bash
jekyll build -d /tmp/site && node scripts/measure_page_weight.js /tmp/site [--react-dir <dir>] [--json out.json]
```

Loads home, two news posts, contact and banwag in an emulated phone, reports bytes at load and after scrolling,
and lists any `.ply`/`.mp4`/`.zip` fetched without a click (should be "none").
