# What is this?
It's a very unfinished Discord RPC thing for Fluxer on Linux.
Shows (most?) Discord RPC apps on your status!

Works by listening to the discord-ipc-0 socket (only supported path is currently $XDG_RUNTIME_DIR/discord-ipc-0!) and using the recieved json to create a status which is set through the Fluxer API.

# Setup
1. Clone the repo somewhere
```sh
git clone https://github.com/GiveMeTheButter/fluxer-rpc-reader-linux.git
```
2. Create a python venv somewhere (preferably in the cloned directory)
```sh
python -m venv venv
```
3. Install aiohttp via pip
```sh
venv/path/to/pip install aiohttp
```
4. Run main.py with python inside the root of the cloned directory
```sh
venv/path/to/python main.py
```
