from ModelGeneratorInterface import ModelGenerator

class AggregatedModelGenerator(ModelGenerator):
    def __init__(self, instance_file_name, model_type):
        super().__init__(instance_file_name, model_type)

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
                self.edges.append(start + "_" + edge_id + "_" + end)
                self.edges_cost[start + "_" + edge_id + "_" + end] = cost_avg

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

    def write_objective_in_file(self, file):
        file.write("MINIMIZE\n")
        objective = "\tobj: "
        for edge in self.edges:
            if self.edges_cost[edge] < 0:
                objective += str(self.edges_cost[edge]) + " x_" + str(edge)
            else:
                objective += " + " + str(self.edges_cost[edge]) + " x_" + str(edge)
        objective = objective[:len(objective)] + "\n"
        file.write(objective)

    def write_source_constraints_in_file(self, file):
        source_constraints = ""
        for source in self.source:
            constraint = "\tc_source_" + source + ": "
            for edge in self.edges:
                if edge.startswith(source + "_"):  # If the edge ends in 'dest'
                    constraint += " + x_" + edge
                elif edge.endswith("_" + source):
                    # Soustraire ce que le noeud source reçoit (car il peut aussi agir en tant que noeud intermédiaire)
                    constraint += " - x_" + edge
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
                    constraint += " + x_" + edge
                elif edge.startswith(dest + "_"):
                    # Soustraire ce que le noeud destination redonne (agit en tant que noeud intermédiaire)
                    constraint += " - x_" + edge
            #constraint = constraint[:len(constraint) - 3]
            constraint += " = "
            constraint += str(self.dest_demands[dest])
            constraint += "\n"
            dest_constraints += constraint
        file.write(dest_constraints)

    """Tout noeud intermédiaire doit redonner tout ce qu'il recoit (flux entrant = flux sortant)"""
    def write_intermediate_constraints_in_file(self, file):
        for inter_node in self.intermediate_nodes:
            constraint = "\tc_inter_" + str(inter_node) + ": "
            for edge in self.edges:
                if edge.startswith(str(inter_node) + "_"):  # Si le noeud intermediaire est la source (il donne)
                    constraint += " - x_" + edge
                elif edge.endswith("_" + str(inter_node)):  # Si le noeud intermediaire est la destination
                    constraint += " + x_" + edge
            constraint += " = 0"
            constraint += "\n"
            file.write(constraint)
