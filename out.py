import controls
import funcs
from colors import *
from decimal import *
import run
CLS = '\033[2J'
CLS_END = '\033[0J'
CLS_END_LN = '\033[0K'
REDRAW = '\033[0;0f'
HIDE_CUR = '\033[?25l'
SHOW_CUR = '\033[?25h'


def log_lines(logs, n):
    return ('\n' + CLS_END_LN).join(line for line in logs.split('\n')[-n:])


def output(maze, cars, logs, colors=True):
    out = ''
    busstops = []
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell.name == 'bus-stop':
                busstops.append(Decimal(cell.bench))
            # Get value of cell without car.
            value = controls.display[cell.name].format(value=cell.value)
            color = controls.colors[cell.name]

            # Should only be one car in cell, but if not print last one.
            car = [car for car in cars if car.x == x and car.y == y]
            if car:
                # Replace value of cell with value of car if there is one.
                value = car[-1].value
                color = {
                    'bg': color['bg'],
                    'fg': WHITE if color['bg'] == BLACK else BLACK,
                    'style': None
                }

            # Two characters wide.
            value = funcs.escape(value)
            if len(value) > 2:
                value = value[:2]
            elif len(value) < 2:
                value = ('0' * (2 - len(value))) + value

            out += colorStr(value, **color) if colors else value
        out += CLS_END_LN + '\n'
    out += logs
    out += CLS_END_LN + '\n'
    out += CLS_END_LN + '\n'
    i = 0
    for car in cars:
        if isinstance(car.value, str):
            out += "car " + str(i) + " = " + car.value + " carrying [ "
            for passe in car.passengers:
                if isinstance(passe, str):
                    out += passe + " , "
                else:
                    out += str(passe) + " , " 
            out += ' ] ' + CLS_END_LN + '\n'
        else:
            out += "car " + str(i) + " = " + str(Decimal(car.value)) + " carrying [ "
            for passe in car.passengers:
                if isinstance(passe, str):
                    out += passe + " , "
                else:
                    out += str(passe) + " , " 
            out += ' ] ' + CLS_END_LN + '\n' 
        i += 1
    i = 0
    for ibusstop in busstops:
        if Decimal(ibusstop) != Decimal(0):
            out += "Bus Stop " + str(i) + " = " + str(Decimal(ibusstop))
            out += CLS_END_LN + '\n'
        i += 1
    out += CLS_END_LN + '\n'
    global switchgate
    out += "switchgate = " + str(run.switchgate) + CLS_END_LN + '\n'
    out += "x hotel = [ "
    for i in run.xcoordplot:
        out += str(i) + " , " 
    out += ' ] ' + CLS_END_LN + '\n'
    out += "y hotel = [ "
    for i in run.ycoordplot:
        out += str(i) + " , " 
    out += ' ] ' + CLS_END_LN + '\n'
    out += "t hotel = [ "
    for i in run.tcoordplot:
        out += str(i) + " , " 
    out += ' ] ' + CLS_END_LN + '\n'
    out += CLS_END_LN + '\n'
    out += CLS_END_LN + '\n'
    print(REDRAW + out + CLS_END)


def init():
    print(HIDE_CUR + CLS)


def end():
    print(SHOW_CUR)
