# What is this?
It's a very unfinished Discord RPC thing for Fluxer on Linux.
Shows (most?) Discord RPC apps on your status!

Works by listening to the discord-ipc-0 socket (only supported path is currently $XDG_RUNTIME_DIR/discord-ipc-0!) and using the recieved json to create a status which is set through the Fluxer API.

# Setup
## Latest Release
1. Download the binary
2. Put the binary in its own directory (optional)
3. Create "token.txt" inside of the directory where the binary resides in
4. Put your Fluxer token inside of "token.txt"
5. Run the binary!
## Latest Commit
1. Clone the repo somewhere
```sh
git clone https://github.com/GiveMeTheButter/fluxer-rpc-reader-linux.git
```
2. Inside the cloned directory, add a file named "token.txt" and put your Fluxer token in it

3. Create a python venv somewhere (preferably in the cloned directory)
```sh
python -m venv venv
```
4. Install aiohttp via pip
```sh
venv/path/to/pip install aiohttp
```
5. Run main.py with python inside the root of the cloned directory
```sh
venv/path/to/python main.py
```
#
One thing that is important to note is that you likely have to remove discord-ipc-0 before using this. This will also very likely not work while Discord is open.
