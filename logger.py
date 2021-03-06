import colored
from colored import stylize

# See https://pypi.org/project/colored/ for colors

logs = []


def error(log):
    global logs
    log = "Error: {}".format(log)
    print(stylize(log, colored.fg("red")))
    logs.append(log)

def debug(log):
    global logs
    log = "Debug: {}".format(log)
    print(stylize(log, colored.fg("orange_1")))
    logs.append(log)

def info(log):
    global logs
    log = "Info: {}".format(log)
    print(stylize(log, colored.fg("yellow")))
    logs.append(log)

def event(log):
    global logs
    log = "Event: {}".format(log)
    print(stylize(log, colored.fg("green")))
    logs.append(log)

if __name__ == "__main__":
    pass