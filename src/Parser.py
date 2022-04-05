import Street
import Car

# parses the first line
# of the input file
def parse_first_line(line):
    splitted = line.split()

    duration = splitted[0]  # simulation duration (D)
    n_intersections = splitted[1]  # number of intersections (I)
    n_streets = splitted[2]  # number of streets (S)
    n_cars = splitted[3]  # number of cars
    bonus = splitted[4]  # bonus points for each car that reaches destination

    return {"duration": duration, "n_intersections": n_intersections, "n_streets": n_streets, "n_cars": n_cars, "bonus": bonus}

# parses one line of the input file
# relative to the streets
def parse_street_line(line):
    splitted = line.split()

    start_intersection = splitted[0]
    end_intersection = splitted[1]
    street_name = splitted[2]
    time_cost = splitted[3]

    street = Street(start_intersection, end_intersection, street_name, time_cost)

    return street

# parses one line of the input file
# relative to the cars paths
def parse_car_line(line, streets):
    splitted = line.split()

    path_length = splitted[0]
    path = []

    for i in range(1, splitted.length+1):
        path.append(x for x in streets if x.street_name == splitted[i])

    car = Car(path_length, path)

    return car


# parses all the input file
def parse_input_file(path):
    file = open(path, 'r')

    streets = []
    cars = []

    lines = file.readline()
    init_variables = parse_first_line(lines.pop(0))

    for i in range(0, init_variables["n_streets"]):
        streets.append(parse_street_line(lines.pop(i)))

    for line in lines:
        cars.append(parse_car_line(line,streets))

    return init_variables, streets, cars
