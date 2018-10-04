import asyncio

from sanic import Sanic
from sanic.response import html

import socketio

from subprocess import run

def num_desktops():
    result = run(['wmctrl', '-d'], capture_output=True, text=True)
    lines = result.stdout.split('\n')
    return len(lines)

def cur_desktop():
    result = run(['wmctrl', '-d'], capture_output=True, text=True)
    lines = result.stdout.split('\n')
    for i, line in enumerate(lines):
        if '*' == line.split()[1]:
            return i
    else:
        return -1

sio = socketio.AsyncServer(async_mode='sanic')
app = Sanic()
sio.attach(app)


async def background_task():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(10)
        count += 1
        await sio.emit('my response', {'data': 'Server generated event'},
                       namespace='/test')


@app.listener('before_server_start')
def before_server_start(sanic, loop):
    sio.start_background_task(background_task)


# @app.route('/')
# async def index(request):
#     with open('app.html') as f:
#         return html(f.read())


@sio.on('my event')
async def test_message(sid, message):
    await sio.emit('my response', {'data': message['data']})
    print('my event', message)

@sio.on('pose')
async def test_message(sid, message):
    # await sio.emit('my response', {'data': message['data']})
    print('pose', message)

    n = num_desktops()
    c = cur_desktop()

    if message == 'left' and c > 0:
        run(['wmctrl', '-s', str(c - 1)])
    elif message == 'horizontal':
        # run(['wmctrl', '-s', '1'])
        pass
    elif message == 'right' and c + 1 < n:
        run(['wmctrl', '-s', str(c + 1)])

if __name__ == '__main__':
    app.run()
