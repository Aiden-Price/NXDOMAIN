"""
SID: 530502821
"""
from sys import argv
import socket
import time
from typing import List
from pathlib import Path

def validate(master: Path) -> bool:
    try:
        f = open(master, 'r')
        lines = f.readlines()

        if not lines:
            return False

        try:
            root = int(lines[0].strip())
        except Exception as e:
            return False

        if not (1024 <= root <= 65535):
            return False

        for i in lines[1:]:
            section = i.strip().split(',')

            if len(section) != 2 or not section[0] or not section[1].isdigit():
                return False

    except FileNotFoundError:
        return False
    
    return True
        
def generate(master: Path, out_directory: Path) -> bool:
    try:
        if not out_directory.is_dir():
            out_directory.mkdir()
        f = open(master, 'r')
        lines = f.readlines()
        root = int(lines[0].strip())

        for i in lines[1:]:
            section = line.strip().split(',')
            domain = section[0]
            port = int(section[1])
            config_single = out_directory / f"{domain}.conf"
            with open(config_single, 'w') as sf:
                sf.write(f"{port}\n")

    except Exception as e:
        print("NON-WRITABLE SINGLE DIR")
        return False
    return True

def main(args: list[str]) -> None:
    if len(args) != 2:
        print("INVALID ARGUMENTS")
        return

    master = Path(args[0])
    out_directory = Path(args[1])

    if not validate(master):
        print("INVALID MASTER")
        return
    
    try:
        with out_directory.open("w") as test_file:
            pass
    except:
        print("INVALID MASTER")
        return

    if generate(master, out_directory):
        print("SUCCESS")

if __name__ == "__main__":
    main(argv[1:])
