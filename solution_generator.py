import os
import subprocess

from aggregated_model_generator import AggregatedModelGenerator
from disaggregated_model_generator import DisaggregatedModelGenerator


class SolutionGenerator:
    # Path to the folder containing the files
    instances_folder_path = 'instances'
    # Define the path to the folder where you want to save the LP and SOL files
    lp_output_folder = 'linearPrograms/'
    sol_output_folder = 'solutions/'
    # List all files in the folder
    files = os.listdir(instances_folder_path)
    def __init__(self, model_type):
        self.model_type = model_type

    def generate_solution(self):

        # Iterate over each file in the folder
        for file_name in self.files:
            print(file_name)
            # Construct the full path to the file
            file_path = os.path.join(self.instances_folder_path, file_name)

            # Open the file
            with open(file_path, 'r') as file:
                instance_file_name = file_name.split(".")[0]
                if self.model_type == 0:
                    model_generator = AggregatedModelGenerator(instance_file_name, self.model_type, self.lp_output_folder)
                else:
                    model_generator = DisaggregatedModelGenerator(instance_file_name, self.model_type, self.lp_output_folder)
                model_generator.generate_model()

                # Specify the path to save the LP and SOL files in the output folder
                lp_file = os.path.join(self.lp_output_folder, f"{instance_file_name}_{self.model_type}.lp")
                sol_file = os.path.join(self.sol_output_folder, f"{instance_file_name}_{self.model_type}.sol")
                print(sol_file)

                # Run glpsol to generate the solution file
                subprocess.run(["glpsol", "--lp", lp_file, "-o", sol_file])


solution_generatior = SolutionGenerator(1)
solution_generatior.generate_solution()
