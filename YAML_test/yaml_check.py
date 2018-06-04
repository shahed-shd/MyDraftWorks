import yaml     # pip install pyyaml
import pprint
import sys

def main():
    try:
        arg1 = sys.argv[1]
    except:
        print("No yaml file assigned.")
        exit()

    with open(arg1, 'r') as yaml_file:
        obj = yaml.safe_load(yaml_file)

    print("AS PYTHON OBJECT:\n")
    pprint.pprint(obj, stream=sys.stdout, indent=2, width=120)

    print("\nAS YAML DUMPING:\n")
    yaml.safe_dump(obj, stream=sys.stdout)


if __name__ == '__main__':
    main()