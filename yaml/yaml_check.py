# This program is used to parse a yaml file
# If the parsing is done without any exception, the yaml file can be assumed to be validated.
# For yaml dumping, pyaml module is used optionally.
# pyyaml and pyaml dumps in different manner.

import yaml     # pip install pyyaml
import pprint
import sys

def dump_as_py_obj(obj):
    print("========== AS PYTHON OBJECT ==========\n")
    pprint.pprint(obj, stream=sys.stdout, indent=2, width=120)


def dump_as_yaml(obj):
    print("\n========== AS YAML DUMPING ==========\n")
    yaml.safe_dump(obj, stream=sys.stdout)
    

def try_dumping_as_pyaml(obj):
    try:
        import pyaml         # pip install pyaml
    except:
        pass
    else:
        print("\n========== AS PYAML DUMPING ==========\n")
        pyaml.dump(obj, sys.stdout, vspacing=[1, 0])


def main():
    try:
        arg1 = sys.argv[1]
    except:
        print("No yaml file assigned.")
        exit()

    with open(arg1, 'r') as yaml_file:
        obj = yaml.safe_load(yaml_file)

        dump_as_py_obj(obj) 
        dump_as_yaml(obj)
        try_dumping_as_pyaml(obj)


if __name__ == '__main__':
    main()
