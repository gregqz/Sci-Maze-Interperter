import re
import copy

import funcs
import controls
from functools import reduce
from decimal import *

switchgate = Decimal(0.0) 
xcoordplot = []
ycoordplot = []
tcoordplot = []
def create_cars(maze, Car):
    """
        Goes through maze and creates a car for any start cells.
    """
    cars = []
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell.name == 'start':
                cars.append(Car(0, x, y))

    return cars


def move_cars(maze, cars):
    """
        Moves all the cars one frame.
    """
    maze_after = copy.deepcopy(maze)
    cars_after = copy.deepcopy(cars)

    for i in range(len(cars)):
        car = cars_after[i]

        # Don't move a car if it is paused.
        if car.pause:
            continue

        # Splitters do their own thing.
        if maze[car.y][car.x].name == 'splitter':
            car_copy = copy.deepcopy(car)
            cars_after.append(car_copy)

            car.direction = 'R'
            car.x += 1
            car_copy.direction = 'L'
            car_copy.x -= 1

        else:

            if car.direction in 'Nn':
                continue

            directions = ['U', 'R', 'D', 'L']

            # Move current direction to front
            try:
                directions.remove(car.direction.lower())
            except ValueError:
                directions.remove(car.direction.upper())
            directions.insert(0, car.direction)

            # Move current backwards direction to back
            opp = opp_dir(car.direction)
            try:
                directions.remove(opp.lower())
            except ValueError:
                directions.remove(opp.upper())
            directions.append(opp)

            # Check all directions.
            for d in directions:
                x, y = dir_to_pos(car, d)
                can_move_dir = check_pos(maze, x, y)

                if can_move_dir: break

            # If car can move.
            if can_move_dir:
                car.x = x
                car.y = y
                car.direction = d

    # Error if any cars share a cell.
    if len(cars) is not len(set((car.x, car.y) for car in cars)):
        funcs.error('Multiple cars in same cell.')

    return maze_after, cars_after


def car_actions(maze, cars, functions, debug=False):
    """
        Runs any functions a car is on.
    """
    global switchgate
    global xcoordplot
    global ycoordplot
    
    # Do signal first so it's enabled before any functions are run.
    signals = []
    for car in cars:
        if maze[car.y][car.x].name == 'signal':
            signals.append(maze[car.y][car.x].value)

    logs = ''
    removed = []
    for car in cars:

        # Count down any paused cars.
        if car.pause:
            car.pause -= 1
            continue

        cell = maze[car.y][car.x]

        # Actions:
        if cell.name == 'wall':
            funcs.error('Car got in wall.')

        elif cell.name == 'path':
            pass

        elif cell.name == 'pause':
            car.pause = int(cell.value)

        elif cell.name == 'hole':
            removed.append(car)

        elif cell.name == 'out':
            logs += str(car.value)

        elif cell.name == 'ln-out':
            logs += str(car.value) + '\n'

        elif cell.name == 'in':
            car.value = input('> ')

        elif cell.name == 'one-use':
            cell.name = 'wall'
            cell.value = controls.display['wall']

        elif cell.name == 'direction':
            car.direction = cell.value[1]

        elif cell.name == 'function':
            function = functions[cell.value]
            try:
                result = str(function(car.value))
            except TypeError:
                result = str(function(car.value, signals))

            if not result == 'None':
                match = re.match(controls.regexes['direction'], result)
                if match:
                    car.direction = result[1]
                else:
                    car.value = str(result)
        elif cell.name == 'passenger':
            car.busstop = str(cell.value)
        elif cell.name == 'bus-stop':
            #Passenger and bench Operations
            op = car.busstop
            if op == ';-':
                car.passengers[-1] = Decimal(car.passengers[-1]) - Decimal(cell.bench)
            if op == ';+':
                car.passengers[-1] = Decimal(car.passengers[-1]) + Decimal(cell.bench)
            if op == ';*':
                car.passengers[-1] = Decimal(car.passengers[-1]) * Decimal(cell.bench)
            if op == ';/':
                car.passengers[-1] = Decimal(car.passengers[-1]) / Decimal(cell.bench)
            if op == ';$':
                car.passengers.append(Decimal(cell.corner))
            if op == ';s':
                passbuff = Decimal(car.passengers[-1])
                drivbuff = Decimal(car.value)
                car.value = Decimal(passbuff)
                car.passengers[-1] = Decimal(drivbuff)
            if op == ';c':
                car.passengers.append(Decimal(car.value))
            if op == ';k':
                car.passengers = car.passengers[:-1]
            if op == ';l':
                cell.bench = Decimal(car.passengers[-1])
                car.passengers = car.passengers[:-1]
            if op == ';h':
                car.value = Decimal(cell.bench)
                cell.bench = Decimal(0)
            if op == ';w':
                switchgate = car.value
            if op == ';u':
                car.value = switchgate
            if op == ';x':
                xcoordplot.append(Decimal(car.value))
            if op == ';y':
                ycoordplot.append(Decimal(car.value))
            if op == ';t':
                tcoordplot.append(Decimal(car.value))
            if op == ';p':
                a = [tcoordplot,xcoordplot,ycoordplot]
                at = [reduce(lambda z,k: str(z) + " " + str(k),list(x)) for x in zip(*a)]
                lines = ['t x y']
                lines.extend(at)
                end = ["","","set xlabel <xlabel>'","set ylabel '<ylabel>'","set title '<title>'","set pointsize 1.5 ","set terminal png size 1200,900 enhanced font \"Helvetica,20\"","set key top right","set output 'output.png'","plot \"Plotdata.dat\" using 1:2 title '<x series>', \"Plotdata.dat\" using 1:3 title '<y series>'","quit"]
                lines.extend(end)
                file = open("Plotdata.dat","w")
                for line in lines:
                    file.write(line + "\r\n")
                file.close()
                
            car.busstop = ''
    # Remove any deleted cars.
    for car in removed:
        cars.remove(car)

    return maze, cars, logs


def dir_to_pos(car, direction):
    if direction in 'Uu':
        x = car.x
        y = car.y - 1
    elif direction in 'Rr':
        x = car.x + 1
        y = car.y
    elif direction in 'Dd':
        x = car.x
        y = car.y + 1
    elif direction in 'Ll':
        x = car.x - 1
        y = car.y

    return x, y


def check_pos(maze, x, y):
    return not maze[y][x].name == 'wall'


def opp_dir(direction):
    if direction in 'Uu':
        return 'D'
    elif direction in 'Rr':
        return 'L'
    elif direction in 'Dd':
        return 'U'
    elif direction in 'Ll':
        return 'R'
