from rich.console import Console
from rich.traceback import install as tr_install

console = Console()
tr_install(console=console)
