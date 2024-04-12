import sys
from exceptions.IncorrectFormatError import IncorrectFormatError


class ModelGenerator:
    def __init__(self, instance_file_name, model_type):
        self.instance_file = instance_file_name
        self.model_type = model_type
        self.nb_items = 0
        self.nb_nodes = 0
        self.edges = []
        self.edges_cost = {} # Dictionary that contains the costs of each edge (key is in format start_dest)
        self.dest = []
        self.dest_demands = {}
        self.source = []
        self.source_capacities = {}
        self.intermediate_nodes = []

    def generate_model(self):
        self.parse_instance_file(self.instance_file)
        if self.model_type == 0:
            self.generate_aggregated_model()
        elif self.model_type == 1:
            self.generate_disaggregated_model()

    def parse_instance_file(self, instance_file):
        with open("instances/" + instance_file + ".txt", "r") as file:
            self.nb_items = int((file.readline().strip().split(" ")[1]))
            file.readline()
            self.nb_nodes = int((file.readline().strip().split(" ")[1]))

            edges = {}
            self.intermediate_nodes.extend([i for i in range(self.nb_nodes)])
            for line in file:
                #print([i for i in range(self.nb_nodes)])
                self.extract_edge_info(file, line)
                self.extract_source_info(file, line)
                self.extract_dest_info(file, line)

        print(self.intermediate_nodes)


    def extract_edge_info(self, file, line):
        if line.startswith("EDGES"):
            nb_edges = int(line.split()[1])
            next(file)
            for _ in range(nb_edges):
                edge_info = next(file).strip().split()
                edge_id, start, end = edge_info[:3]
                costs = []
                for i in range(3, len(edge_info)):
                    costs.append(edge_info[i])

                cost_avg = 0
                for cost in costs:
                    cost_avg += int(cost)
                cost_avg /= self.nb_items
                self.edges.append(start + "_" + end)
                self.edges_cost[start + "_" + end] = cost_avg
                #print("cost_avg = ", cost_avg)

    def generate_aggregated_model(self):
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

    def write_source_constraints_in_file(self, file):
        source_constraints = ""
        for source in self.source:
            constraint = "\tc_source_" + source + ": "
            for edge in self.edges:
                if edge.startswith(source + "_"):  # If the edge ends in 'dest'
                    edge_end_node = edge.split("_")[1]
                    constraint += " + x_" + str(source) + "_" + str(edge_end_node)
                elif edge.endswith("_" + source):
                    # Soustraire ce que le noeud source reçoit (car il peut aussi agir en tant que noeud intermédiaire)
                    edge_start_node = edge.split("_")[0]
                    constraint += " - x_" + str(edge_start_node) + "_" + str(source)
            #constraint = constraint[:len(constraint) - 3]
            constraint += " <= "
            constraint += str(self.source_capacities[source])
            constraint += "\n"
            source_constraints += constraint
        file.write(source_constraints)

    def write_destination_constraints_in_file(self, file):
        dest_constraints = ""
        for dest in self.dest:
            constraint = "\tc_dest_" + dest + ": "
            for edge in self.edges:
                if edge.endswith("_" + dest):  # If the edge ends in 'dest'
                    edge_start_node = edge.split("_")[0]
                    constraint += " + x_" + str(edge_start_node) + "_" + str(dest)
                elif edge.startswith(dest + "_"):
                    # Soustraire ce que le noeud destination redonne (agit en tant que noeud intermédiaire)
                    edge_end_node = edge.split("_")[1]
                    constraint += " - x_" + str(dest) + "_" + str(edge_end_node)
            #constraint = constraint[:len(constraint) - 3]
            constraint += " = "
            constraint += str(self.dest_demands[dest])
            constraint += "\n"
            dest_constraints += constraint
        file.write(dest_constraints)

    """Tout noeud intermédiaire doit redonner tout ce qu'il recoit (flux entrant = flux sortant)"""
    def write_intermediate_constraints_in_file(self, file):
        constraint = "\n"
        for inter_node in self.intermediate_nodes:
            constraint = "\tc_inter_" + str(inter_node) + ": "

            for edge in self.edges:
                if edge.startswith(str(inter_node) + "_"): # Si le noeud intermediaire est la source (il donne)
                    edge_end_node = edge.split("_")[1]
                    constraint += " - x_" + str(inter_node) + "_" + str(edge_end_node)
                elif edge.endswith("_" + str(inter_node)):     # Si le noeud intermediaire est la destination
                    edge_start_node = edge.split("_")[0]
                    constraint += " + x_" + str(edge_start_node) + "_" + str(inter_node)
            constraint += " = 0"
            constraint += "\n"
            file.write(constraint)



    def write_objective_in_file(self, file):
        file.write("MINIMIZE\n")
        objective = "\tobj: "
        for edge in self.edges:
            objective += str(self.edges_cost[edge]) + " x_" + str(edge) + " + "
        objective = objective[:len(objective) - 2] + "\n"
        file.write(objective)

    def generate_disaggregated_model(self):  # instance_name, nodes, edges, sources, destinations):
        pass

    def extract_source_info(self, file, line):
        if line.startswith("SOURCES"):
            nb_source = int(line.split()[1])
            next(file)
            for _ in range(nb_source):
                source_info = next(file).strip().split()
                source_id = source_info[0]
                self.intermediate_nodes.remove(int(source_id))
                self.source.append(source_id)
                source_capacity = 0
                for i in range(1, len(source_info)):
                    source_capacity += int(source_info[i])
                self.source_capacities[source_id] = source_capacity
                #print("Cap = " + str(source_capacity))


    def extract_dest_info(self, file, line):
        if line.startswith("DESTINATIONS"):
            nb_dest = int(line.split()[1])
            next(file)
            for _ in range(nb_dest):
                dest_info = next(file).strip().split()
                dest_id = dest_info[0]
                self.intermediate_nodes.remove(int(dest_id))
                self.dest.append(dest_id)
                dest_demand = 0
                for i in range(1, len(dest_info)):
                    dest_demand += int(dest_info[i])
                self.dest_demands[dest_id] = dest_demand




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
