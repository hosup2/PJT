import os
import django
import asyncio
from channels.layers import get_channel_layer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

async def check():
    layer = get_channel_layer()
    try:
        await layer.send('test_channel', {'type': 'test.message'})
        print("Redis Connection Successful!")
    except Exception as e:
        print(f"Redis Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(check())
