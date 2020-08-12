# Pose Remote Control

Pose Estimation Frameworks:

- OpenPose
- [Multi]PoseNet
  - Realtime implementation with tensorflow ([github](https://github.com/tensorflow/tfjs-models/tree/master/posenet), [medium article](https://medium.com/tensorflow/real-time-human-pose-estimation-in-the-browser-with-tensorflow-js-7dd0bc881cd5))
- DensePose

- (Python implemenation with pretrained models: [eldar/pose-tensorflow](https://github.com/eldar/pose-tensorflow))
- ([OpenCV Tutorial](https://www.learnopencv.com/deep-learning-based-human-pose-estimation-using-opencv-cpp-python/))
  - ([Head Pose Estimation](https://www.learnopencv.com/head-pose-estimation-using-opencv-and-dlib/))

## Some projects on GitHub

- github.com/tensorflow/tfjs-models
- github.com/ildoonet/tf-openpose
- github.com/eldar/pose-tensorflow

## Platform

To use the pretrained Posenet TensorFlow model you have to send messages from the browser to a device to be controlled:

- Client: Browser, JavaScript + Tensorflow
- Server: Desktop, Python, Websocket.

Alternatives:

- Electron.
- Run pose estimation on desktop.

### Server

Python with:

- `python-websocket`
- You need a (wsgi) webapp to deploy the webserver: Sanic.
- [Run arbitrary shell commands](https://docs.python.org/3/library/subprocess.html#subprocess.run):
  - [`wmctrl`](https://linux.die.net/man/1/wmctrl) to swap workspaces.

## Gesture control

Approaches:

- Static gestures: Trigger action on change of pose.
  - The poses must be distinct enough, i.e. long non-pose sections between registered poses.
  - Example: Orientation of eye line.
  - Example: Hands above head or below.
  - Compare distances (e.g. of hands) to body height.
  - Don't use if too small in pixels compared to dimensions of trained model = 386x386.
  - Record samples and calculate short-term variance. Don't use if variance too high (low pass filtering).
  - Some [`Math`](https://developer.mozilla.org/de/docs/Web/JavaScript/Reference/Global_Objects/Math/atan2) is required.
- Dynamic gestures: Use movement to trigger actions.
  - Swipe.
  - Rotate hands.

## Case Study: Switch workspace

Tilt head left/right to switch workspace.
  - Use angle of line between eyes.
  - Reset when horizontal to prevent multiple triggers of the pose.
  - Run shell command: `wmctrl -s N`

## Case Study: Write text

- Roll head left/right to send binary number.
- From ASCII table.

## Case Study: Remote Control VLC

VLC has [different interfaces](https://wiki.videolan.org/Interfaces):

- graphical (`qt`)
- command line ([`oldrc` and `telnet`](https://wiki.videolan.org/Console/)): You can communicate through sockets with telnet or netcat.
- browser ([`http`](https://wiki.videolan.org/Web_Interface/))

#### How to use the `rc` interface

[Tutorial](https://n0tablog.wordpress.com/2009/02/09/controlling-vlc-via-rc-remote-control-interface-using-a-unix-domain-socket-and-no-programming/)

Enable the interface in "Einstellungen > Interfaces > Hauptinterfaces > RC"

- TCP Socket (run `vlc -I oldrc --rc-host localhost:9999` or):
  1. Add host `localhost:9999` as command. Run `vlc video.mp4`.
  2. Verify that vlc is listening on the port: `netstat -peanut | grep vlc`.
  3. Send commands to that port:
     - `telnet localhost 9999` and write `play`/`pause`/etc. or
     - `echo pause | ncat localhost 9999` or
     - see below for using the telnet interface programmatically with python.
- Unix Socket (run `vlc -I oldrc --rc-unix vlc.sock`):
  1. Check "Fake TTY".
  2. Add socket `/tmp/vlc.sock`.
  3. `echo pause | ncat -U /tmp/vlc.sock`

**NOTE:**

- `ncat` is a rewrite of `nc`/`netcat`. It is part of the `nmap` package (`apt install nmap`).
- You can add `--send-only`, to surpress received messages.
- If you use `netcat`, also add `-N` to terminate connection after sending the command and receiving `EOF`.

**NOTE:** When using the Unix Socket, you have to use `pause` again to resume playing.

#### Remote Control VLC from Python

- Use built-in [`telnetlib`](https://docs.python.org/3/library/telnetlib.html) and VLCs telnet interface.
- **TODO:** Command line untility `vlc-ctrl`.

##### Telnet

Python has a very simple built-in telnet module called `telnetlib`:

First, play around with the telnet interface of VLC:

```python
from telnetlib import Telnet

with Telnet('localhost', 9999) as tn:
    tn.interact()

# VLC media player 3.0.3 Vetinari
# Command Line Interface initialized. Type `help' for help.
# >
```

You should type `help` there to see what commands are available.

To control VLC programmatically, write a command as `bytestring` followed by a linebreak:

```python
tn = Telnet('localhost', 9999)
tn.write(b'stats\n')
tn.write(b'pause\n')
# ...
tn.write(b'play\n')
```

Note: You can make a simple telnet server with `netcat`:

```bash
$ nc -l PORT
```
