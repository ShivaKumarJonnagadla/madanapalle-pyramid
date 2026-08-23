# Madanapalle Meditation Pyramid — Fundraising Website

A single-page fundraising website for the **Madanapalle Pyramid Spiritual Society** to help
complete a meditation pyramid. Land was donated by the family; the foundation, borewell,
electricity and pillars are done; funds are now exhausted and the work has paused.

The site is a plain static page — no build step, no dependencies.

## Files

```
pyramid-site/
├── index.html          ← the complete website (photos + videos + donation details)
├── artifact.html       ← self-contained copy (photos inlined, no videos) — for quick sharing
├── build_artifact.py   ← regenerates artifact.html from index.html
└── assets/
    ├── img/            ← photographs used on the page
    ├── video/          ← construction videos (~42 MB)
    └── docs/           ← (optional) PDFs
```

## Run locally

Just open `index.html` in a browser, or serve it:

```bash
cd pyramid-site
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploy

See **DEPLOY.md** for GitHub + Vercel step-by-step instructions.

## Edit the donation details

All donation info is in `index.html` inside the `id="donate"` section:
UPI ID `6509092255@myapgb`, account number, IFSC, and the QR image at `assets/img/upi-qr.jpg`.
Always verify the account name reads **Madanapalle Pyramid Spiritual Society** before publishing.
