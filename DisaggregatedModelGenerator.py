from ModelGeneratorInterface import ModelGenerator


class DisaggregatedModelGenerator(ModelGenerator):
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
                self.edges.append(start + "_" + end)
                self.edges_cost[start + "_" + end] = costs

    def extract_source_info(self, file, line):
        if line.startswith("SOURCES"):
            nb_source = int(line.split()[1])
            next(file)
            for _ in range(nb_source):
                source_info = next(file).strip().split()
                source_id = source_info[0]
                self.intermediate_nodes.remove(int(source_id))
                self.source.append(source_id)
                self.source_capacities[source_id] = []
                for i in range(1, len(source_info)):
                    self.source_capacities[source_id].append(int(source_info[i]))

    def extract_dest_info(self, file, line):
        if line.startswith("DESTINATIONS"):
            nb_dest = int(line.split()[1])
            next(file)
            for _ in range(nb_dest):
                dest_info = next(file).strip().split()
                dest_id = dest_info[0]
                self.intermediate_nodes.remove(int(dest_id))
                self.dest.append(dest_id)
                self.dest_demands[dest_id] = []
                for i in range(1, len(dest_info)):
                    self.dest_demands[dest_id].append(int(dest_info[i]))

    def write_objective_in_file(self, file):
        file.write("MINIMIZE\n")
        objective = "\tobj: "
        for edge in self.edges_cost:
            for item in range(self.nb_items):
                if int(self.edges_cost[edge][item]) < 0: # So that we don't have syntax error '+ -'
                    objective += str(self.edges_cost[edge][item]) + " x_" + edge + "_" + str(item)
                else:
                    objective += " + " + str(self.edges_cost[edge][item]) + " x_" + edge + "_" + str(item)

        objective = objective[:len(objective)] + "\n"

        file.write(objective)

    def write_source_constraints_in_file(self, file):
        source_constraints = ""
        for item in range(self.nb_items):
            for source in self.source:
                constraint = "\tc_source_" + source + "_item_" + str(item) + ": "
                for edge in self.edges:
                    if edge.startswith(source + "_"):  # If the edge ends in 'dest'
                        edge_end_node = edge.split("_")[1]
                        constraint += " + x_" + str(source) + "_" + str(edge_end_node) + "_" + str(item)
                    elif edge.endswith("_" + source):
                        # Soustraire ce que le noeud source reçoit (car il peut aussi agir en tant que noeud intermédiaire)
                        edge_start_node = edge.split("_")[0]
                        constraint += " - x_" + str(edge_start_node) + "_" + str(source) + "_" + str(item)
                constraint += " <= "
                constraint += str(self.source_capacities[source][item])
                constraint += "\n"
                source_constraints += constraint
        file.write(source_constraints)

    def write_destination_constraints_in_file(self, file):
        dest_constraints = ""
        for item in range(self.nb_items):
            for dest in self.dest:
                constraint = "\tc_dest_" + dest + "_item_" + str(item) + ": "
                for edge in self.edges:
                    if edge.endswith("_" + dest):  # If the edge ends in 'dest'
                        edge_start_node = edge.split("_")[0]
                        constraint += " + x_" + str(edge_start_node) + "_" + str(dest) + "_" + str(item)
                    elif edge.startswith(dest + "_"):
                        # Soustraire ce que le noeud destination redonne (agit en tant que noeud intermédiaire)
                        edge_end_node = edge.split("_")[1]
                        constraint += " - x_" + str(dest) + "_" + str(edge_end_node) + "_" + str(item)
                constraint += " = "
                constraint += str(self.dest_demands[dest][item])
                constraint += "\n"
                dest_constraints += constraint
        file.write(dest_constraints)

    """Tout noeud intermédiaire doit redonner tout ce qu'il recoit (flux entrant = flux sortant)"""
    def write_intermediate_constraints_in_file(self, file):
        for item in range(self.nb_items):

            for inter_node in self.intermediate_nodes:
                constraint = "\tc_inter_" + str(inter_node) + "_item_" + str(item) + ": "
                for edge in self.edges:
                    if edge.startswith(str(inter_node) + "_"):  # Si le noeud intermediaire est la source (il donne)
                        edge_end_node = edge.split("_")[1]
                        constraint += " - x_" + str(inter_node) + "_" + str(edge_end_node) + "_" + str(item)
                    elif edge.endswith("_" + str(inter_node)):  # Si le noeud intermediaire est la destination (il reçoit)
                        edge_start_node = edge.split("_")[0]
                        constraint += " + x_" + str(edge_start_node) + "_" + str(inter_node) + "_" + str(item)
                constraint += " = 0"
                constraint += "\n"
                file.write(constraint)



