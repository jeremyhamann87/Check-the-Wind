# Check the Wind

Live wind, weather, alerts, air quality and "best times to get outside" for any U.S. or Canadian location.
Static site — plain HTML/CSS/JS (Alpine.js + Leaflet from a CDN), no build step.

Live at **https://www.checkthewind.com**

## What's in the repo

| Path | What it is |
| --- | --- |
| `index.html` | The site (Design B). Phone, tablet and desktop layouts in one file. |
| `futurecast/index.html` | The expanded radar page, embedded by the site in a modal. |
| `pipeline/` | Python pipeline that renders the radar frames. See `pipeline/README.md`. |
| `windline.html`, `compare-ab.html` | Design A and the A/B compare page. Kept for reference; **not published**. |
| `workers/airnow-proxy.js` | Cloudflare Worker that holds the AirNow API key as a secret and answers air-quality requests for the site. Deployed separately in Cloudflare (not by the workflow). |
| `404.html`, `robots.txt`, `sitemap.xml`, `CNAME` | Published alongside the site. |
| `.github/workflows/deploy.yml` | Builds the radar frames and publishes the site to GitHub Pages. |

## Run it locally

```bash
python3 -m http.server 8765
# open http://localhost:8765/
```

The radar page needs `futurecast/manifest.json` and `futurecast/frames/`, which are generated
(not committed). Run the pipeline once (`pipeline/README.md`) if you want radar frames locally.

## Deploying

Every push to `main` — and a schedule every 15 minutes — runs the **Build and deploy the site**
workflow, which renders fresh radar frames and publishes to GitHub Pages.

One-time setup:

1. **Settings → Pages → Build and deployment → Source: GitHub Actions.**
2. **Settings → Pages → Custom domain: `www.checkthewind.com`**, then tick **Enforce HTTPS** once the certificate is ready.
3. DNS at the domain registrar:
   * `www` — `CNAME` → `jeremyhamann87.github.io`
   * apex `checkthewind.com` — four `A` records: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
     (GitHub then redirects the bare domain to `www`).

## Data sources

National Weather Service (U.S. weather, alerts, place names), Environment and Climate Change Canada (Canadian weather, alerts and radar), NOAA MRMS / HRRR and NEXRAD via Iowa Environmental Mesonet (radar),
AirNow / EPA and Open-Meteo (air quality, recent rainfall, place search), OpenStreetMap (map tiles),
SUNRISE-SUNSET.ORG (sun times). Credits and terms are in the site's "Disclaimers & Data Sources" panel.

## Contact

Questions, feedback or bug reports: **contact@checkthewind.com**, or open an issue on this repo.
