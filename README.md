# Gesture Detection Demo

This is a small gesture control demo I hacked together on an afternoon to show
that you can do something useful and fun with computer vision
as a school project.

In this demo you can switch your virtual desktop by tilting your head to the side.
But you can easily adapt this to anything you can program in Python.
See [my notes](notes.md) for some brainstorming, e.g. how to control VLC media player.

## How it works

There is a Client which does the Gesture Detection using a pretrained PoseNet model
(a neural network). It takes an image from a webam and outputs where certain features
of a face (_landmarks_) are. If the landmarks move in a certain way, a _gesture_ is detected.
For example if the line between your eyes diverges from horizontal by a certain angle.
(Actually it is more like a static _pose_ whereas a gesture would be a transition from
one pose to another.)

The detection event is then sent over a web socket to a Python server which runs
a certain command to switch desktops.

The client is uses the model from

- `camera.js`
- `camera.html`
- `server.py`
- (`client.html` as websocket playground)

## Installation

Y

See `tfjs-models/posenet/demos`:

```sh
cd tfjs-models/posenet/demos
# Install dependencies
## Client
yarn
## Server
mkvirtualenv -a . -p python3.7 posenet
pip install sanic python-socketio

# Start client
npx parcel --no-hmr camera.html  # hot module replacement does not work with model loading
# Goto browser and check if pose is detected

# Start server
python server.py

# Tilt head to switch workspaces
```

## Usage

- Roll head left/right to switch workspace.
  - Use angle of line between eyes.
  - Reset when horizontal to prevent multiple triggers of the pose.
  - Run shell command: `wmctrl -s N`
- Write text:
  - Roll head left/right to send binary number.
  - From ASCII table.
