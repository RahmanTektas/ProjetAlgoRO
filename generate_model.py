import sys
from exceptions.IncorrectFormatError import IncorrectFormatError


class ModelGenerator:
    def __init__(self, instance_file_name, model_type):
        self.instance_file = instance_file_name
        self.model_type = model_type
        self.nb_items = 0
        self.nb_nodes = 0

    def generate_model(self):
        self.parse_instance_file(self.instance_file)
        if self.model_type == 0:
            self.generate_aggregated_model()
        elif self.model_type == 1:
            self.generate_disaggregated_model()

    def parse_instance_file(self, instance_file):
        with open("instances/" + instance_file + ".txt", "r") as file:
            self.nb_items = (file.readline().strip().split(" ")[1])
            file.readline()
            self.nb_nodes = (file.readline().strip().split(" ")[1])

    def generate_aggregated_model(self):
        with open(self.instance_file + "_" + str(self.model_type) + ".lp", "w") as file:
            file.write("MAXIMIZE\n")
            objective = "\tobj: \n"
            file.write(objective)

            file.write("SUBJECT TO\n")

            file.write("BINARY\n")

            file.write("END\n")

    def generate_disaggregated_model(self):  # instance_name, nodes, edges, sources, destinations):
        pass


def main():
    try:
        if len(sys.argv) != 3:
            raise IncorrectFormatError("Usage: python3 generate_model.py instance_file_name.txt model_type(0 or 1).")

        instance_file_name = sys.argv[1].split(".")[0]
        model_type = int(sys.argv[2])
        model_generator = ModelGenerator(instance_file_name, model_type)
        model_generator.generate_model()
    except ValueError:
        print("Error: The second argument must be an integer (0 or 1).")
    except IncorrectFormatError as err:
        print(f"Error: {err}")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
