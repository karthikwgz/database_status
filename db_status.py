import MySQLdb as mysql
import time

from rich.live import Live
from rich import print,box
from datetime import datetime
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.style import Style
from rich.console import Console

console = Console()

grid = Table.grid(expand=True)
grid.add_column(justify="center", ratio=1)
grid.add_column(justify="right")
grid.add_row(
    "Database Monitoring Tool",
    datetime.now().ctime().replace(":", "[blink]:[/]"),
)
print(Panel(grid, style="bright_yellow"))


db = mysql.connect(host = "localhost",user="root",passwd="root",db="INFORMATION_SCHEMA")
cur = db.cursor()

def info():
    table = Table(border_style="bright_red")
    table.add_column("Threads_connected",style="bright_cyan")
    table.add_column("Threads_created",style="bright_cyan")
    table.add_column("Threads_running",style="bright_cyan")
    table.add_column("Uptime",style="bright_cyan")
    table.add_column("Queries",style="bright_cyan")
    table.add_column("Max_used_connections",style="bright_cyan")

    with Live(table, refresh_per_second=1):
        while True:
            cur.execute('SHOW STATUS')
            res = dict(cur.fetchall())
            table.add_row(res['Threads_connected'],res['Threads_created'],res['Threads_running'],res['Uptime'],res['Queries'],res['Max_used_connections'])
            time.sleep(1.0)
    choice()

def pr_list():
    table = Table(border_style="bright_red")
    table.add_column("ID",style="bright_cyan")
    table.add_column("USER",style="bright_cyan")
    table.add_column("HOST",style="bright_cyan")
    table.add_column("DB",style="bright_cyan")
    table.add_column("COMMAND",style="bright_cyan")
    table.add_column("TIME",style="bright_cyan")
    table.add_column("STATE",style="bright_cyan")
    table.add_column("INFO",style="bright_cyan")
    table.add_column("PROGRESS",style="bright_cyan")
    
    with Live(table, refresh_per_second=1):
        cur.execute('SHOW FULL PROCESSLIST')
        resu = cur.fetchall()
        for res in resu:
            table.add_row(str(res[0]),res[1],res[2],res[3],res[4],str(res[5]),res[6],str(res[7]),str(res[8]))
            time.sleep(1.0)
    choice()

    
def choice():
    console.print("\n [blink] Press 1 [/blink] for Informations \t [blink] Press 2 [/blink] for Process List" ,style="bright_red")  
    ch = int(input("Enter the choice"))
    if ch == 1:
        info()
    elif ch == 2:
        pr_list()
    else:
        print("Invalid choice")
        choice()
    db.close()

choice()
    


