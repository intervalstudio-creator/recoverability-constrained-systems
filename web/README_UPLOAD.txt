# RECOVS Upload-Ready Website Package

This package is ready to upload to the root of your GitHub repository.

## Files
- `index.html` — main website
- `style.css` — styles
- `app.js` — interaction logic and formal record generator
- `manifest.webmanifest` — installable app manifest
- `sw.js` — offline cache service worker
- `assets/` — icons

## Upload to GitHub
1. Open your repo.
2. Delete or replace the old root website files.
3. Upload **all files in this ZIP** to the repo root.
4. Commit changes.
5. In GitHub Pages, use:
   - Branch: `main`
   - Folder: `/ (root)`

## Domain
After GitHub Pages works, connect your domain to the repo.

Recommended:
- `www.recovs.org` -> GitHub Pages CNAME
- root domain -> GitHub Pages A records

## Notes
This package preserves the look and structure of the uploaded Boundary-style interface:
- home hero and situation cards
- structured yes/no and numeric questions
- result state block
- formal record download
- offline-ready manifest and service worker
