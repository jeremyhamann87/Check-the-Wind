/**
 * AirNow proxy — a Cloudflare Worker that keeps the AirNow API key out of the web page.
 *
 *   Browser  ->  https://aqi.checkthewind.com/?lat=40.17&lon=-105.10  ->  AirNow (with the secret key)
 *
 * - The key lives in the Worker secret AIRNOW_API_KEY, never in the site's code.
 * - Only requests from checkthewind.com pages are answered.
 * - Coordinates are rounded to 2 decimals (~1 km) and answers are cached for 15 minutes, so many visitors
 *   in the same area cost one AirNow call (AirNow limits each key to ~500 calls an hour).
 *
 * Deploy: Cloudflare dashboard > Workers & Pages > airnow-proxy. Secret: Settings > Variables and Secrets.
 */
const ALLOWED_ORIGINS = ['https://www.checkthewind.com', 'https://checkthewind.com'];

export default {
  async fetch(request, env, ctx) {
    const origin = request.headers.get('Origin') || '';
    const allowed = ALLOWED_ORIGINS.includes(origin);
    const cors = {
      'Access-Control-Allow-Origin': allowed ? origin : ALLOWED_ORIGINS[0],
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Max-Age': '86400',
      'Vary': 'Origin',
    };
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (request.method !== 'GET') return new Response('Method not allowed', { status: 405, headers: cors });
    if (origin && !allowed) return new Response('Forbidden', { status: 403, headers: cors });

    const url = new URL(request.url);
    const lat = parseFloat(url.searchParams.get('lat'));
    const lon = parseFloat(url.searchParams.get('lon'));
    if (!isFinite(lat) || !isFinite(lon) || Math.abs(lat) > 90 || Math.abs(lon) > 180) {
      return new Response('Bad request', { status: 400, headers: cors });
    }
    if (!env.AIRNOW_API_KEY) return new Response('Not configured', { status: 503, headers: cors });

    const la = lat.toFixed(2), lo = lon.toFixed(2);
    const cache = caches.default;
    const cacheKey = new Request('https://airnow-cache.checkthewind.internal/' + la + ',' + lo);
    let cached = await cache.match(cacheKey);
    if (!cached) {
      const upstream = await fetch(
        'https://www.airnowapi.org/aq/observation/current/ziplatlong?format=application/json' +
        '&latitude=' + la + '&longitude=' + lo + '&API_KEY=' + encodeURIComponent(env.AIRNOW_API_KEY)
      );
      if (!upstream.ok) return new Response('Upstream error', { status: 502, headers: cors });
      cached = new Response(await upstream.text(), {
        headers: { 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=900' },
      });
      ctx.waitUntil(cache.put(cacheKey, cached.clone()));
    }
    const headers = new Headers(cached.headers);
    Object.entries(cors).forEach(([k, v]) => headers.set(k, v));
    headers.set('Cache-Control', 'public, max-age=300');
    return new Response(cached.body, { status: 200, headers });
  },
};
