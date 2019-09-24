from pathlib import Path

from storify.interfaces.repl import StoreREPL
from storify.interfaces.server import StoreServer
from storify.store import Store

ROOT_DIR = Path(__file__).parents[1]
DATA_DIR = ROOT_DIR / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

def main():
    store = Store(name="OPEN store")
    server = StoreServer(store)
    server.start()
    StoreREPL(store).cmdloop()
    server.close()
    store.close()
