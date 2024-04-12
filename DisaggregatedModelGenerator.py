from ModelGeneratorInterface import ModelGenerator


class DisaggregatedModelGenerator(ModelGenerator):
    def extract_edge_info(self, file, line):
        pass

    def extract_source_info(self, file, line):
        pass

    def extract_dest_info(self, file, line):
        pass

    def write_source_constraints_in_file(self, file):
        pass

    def write_destination_constraints_in_file(self, file):
        pass

    def write_intermediate_constraints_in_file(self, file):
        pass

    def write_objective_in_file(self, file):
        pass
