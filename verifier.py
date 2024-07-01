from sys import argv
import pathlib

def read(path):
    try:
        with open(path, 'r') as f:
            lines = f.read().splitlines()
        return lines
    except FileNotFoundError:
        return None

def is_valid_line(line):
    parts = line.split(',')
    if len(parts) != 2:
        return False
    domain, port = parts
    if not port.isdigit() or int(port) <= 0:
        return False
    return True

def compare(master, directory_single):
    if not pathlib.Path(directory_single).exists() or not pathlib.Path(directory_single).is_dir():
        print("singles io error")
        exit(1)

    aggregated_single_lines = []
    for paths in pathlib.Path(directory_single).glob('*.conf'):
        lines = read(paths)
        if lines is None:
            print("invalid single")
            exit(1)
        for line in lines:
            if not is_valid_line(line):  
                print("invalid single")
                exit(1)
        aggregated_single_lines.extend(lines)

    if sorted(master) == sorted(aggregated_single_lines):
        return True
    else:
        return False

def main(args: list[str]) -> None:
    if len(args) != 2:
        print("invalid arguments")
        exit(1)

    master_file = args[0]
    directory_single = args[1]
    
    master_content = read(master_file)
    if master_content is None:
        print("invalid master")
        exit(1)


    for line in master_content:
        if not is_valid_line(line):
            print("invalid master")
            exit(1)

    if compare(master_content, directory_single):
        print("eq")
    else:
        print("neq")

if __name__ == "__main__":
    main(argv[1:])

