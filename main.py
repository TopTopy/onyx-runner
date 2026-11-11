"""ONYX isolated runner bootstrap.

This runner intentionally exposes health/status only. The legacy source included
mass-message, harassment, account-deletion and reporting automation; none of that
code is shipped or imported here.
"""
import asyncio
import json
import os
import time
from aiohttp import web

STARTED = time.time()
ORDER_ID = os.getenv('ONYX_ORDER_ID', 'unassigned')
CUSTOMER_ID = os.getenv('ONYX_CUSTOMER_ID', 'unassigned')

async def health(_request):
    return web.json_response({
        'ok': True,
        'service': 'onyx-customer-runner',
        'order_id': ORDER_ID,
        'customer_id': CUSTOMER_ID,
        'uptime_seconds': int(time.time() - STARTED),
        'version': '1.0.0-safe-bootstrap',
    })

async def index(_request):
    return web.json_response({
        'service': 'ONYX Runner',
        'status': 'ready',
        'message': 'Runner مستقل است و آماده دریافت پیکربندی مجاز می‌باشد.',
        'health': '/health',
    })

async def main():
    app = web.Application(client_max_size=1024 * 1024)
    app.router.add_get('/', index)
    app.router.add_get('/health', health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv('PORT', '8080')))
    await site.start()
    print(json.dumps({'event':'runner_started','order_id':ORDER_ID,'customer_id':CUSTOMER_ID}))
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
