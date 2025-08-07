import protogen.models as pgmodels
import protogen.enums as pgenums
import sys


def serialize_to_file(filename: str) -> None:
    print("Python: serializing")

    person = pgmodels.Person()
    person.name = "Alice"
    person.id = 1
    person.email = "alice@example.com"
    person.phone_numbers.extend(["123", "456"])

    person.address.street = "123 Main St"
    person.address.city = "Wonderland"
    person.address.zip = "00001"

    person.status = pgenums.Status.ACTIVE

    with open(filename, "wb") as f:
        f.write(person.SerializeToString())


def deserialize_from_file(filename: str) -> None:
    print("Python: deserializing")

    with open(filename, "rb") as f:
        data: bytes = f.read()
        person = pgmodels.Person()
        person.parse(data)

        print("----- Deserialized instance output -----")
        print(person)
        print("---------- Done ----------")


def main() -> None:
    command: str = sys.argv[1]
    filename: str = sys.argv[2]

    if command == "serialize":
        serialize_to_file(filename)
    elif command == "deserialize":
        deserialize_from_file(filename)
    elif command == "demo":
        serialize_to_file(filename)
        deserialize_from_file(filename)
    else:
        raise ValueError(f"Invalid command {command}")


if __name__ == "__main__":
    main()
