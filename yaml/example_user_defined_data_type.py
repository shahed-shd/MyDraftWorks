import yaml     # pip install pyyaml
import pprint


class MyClass(yaml.YAMLObject):
    yaml_tag = u'!myclass'

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def __repr__(self):
        return "%s(name=%s, gender=%s)" % (self.__class__.__name__, self.name, self.gender)


def main():
    with open('example.yml', 'r') as f:
        cfg = yaml.load(f)

    pprint.pprint(cfg)
    print("\nDUMPING:\n")
    print(yaml.dump(cfg))


if __name__ == '__main__':
    main()
