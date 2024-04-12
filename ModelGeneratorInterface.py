from abc import ABC, abstractmethod


class ModelGenerator(ABC):

    def __init__(self, instance_file_name, model_type):
        self.instance_file = instance_file_name
        self.model_type = model_type
        self.nb_items = 0
        self.nb_nodes = 0
        self.edges = []
        self.edges_cost = {}  # Dictionary that contains the costs of each edge (key is in format start_dest)
        self.dest = []
        self.dest_demands = {}
        self.source = []
        self.source_capacities = {}
        self.intermediate_nodes = []

    @abstractmethod
    def extract_edge_info(self, file, line):
        pass

    @abstractmethod
    def extract_source_info(self, file, line):
        pass

    @abstractmethod
    def extract_dest_info(self, file, line):
        pass

    @abstractmethod
    def write_objective_in_file(self, file):
        pass

    @abstractmethod
    def write_source_constraints_in_file(self, file):
        pass

    @abstractmethod
    def write_destination_constraints_in_file(self, file):
        pass

    @abstractmethod
    def write_intermediate_constraints_in_file(self, file):
        pass

    def parse_instance_file(self, instance_file):
        with open("instances/" + instance_file + ".txt", "r") as file:
            self.get_file_info(file)
            self.intermediate_nodes.extend([i for i in range(self.nb_nodes)])
            for line in file:
                self.extract_edge_info(file, line)
                self.extract_source_info(file, line)
                self.extract_dest_info(file, line)

    def get_file_info(self, file):
        self.nb_items = int((file.readline().strip().split(" ")[1]))
        file.readline()
        self.nb_nodes = int((file.readline().strip().split(" ")[1]))

    def generate_model(self):
        self.parse_instance_file(self.instance_file)
        with open(self.instance_file + "_" + str(self.model_type) + ".lp", "w") as file:
            # Objective
            self.write_objective_in_file(file)
            # Constraints
            file.write("SUBJECT TO\n")
            self.write_source_constraints_in_file(file)
            self.write_destination_constraints_in_file(file)
            self.write_intermediate_constraints_in_file(file)

            file.write("BINARY\n")

            file.write("END\n")