import os
import subprocess
import sys

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
    def __init__(self, model_type, timer):
        self.model_type = model_type
        self.timer = timer
        self.duration_timer = 600

    def generate_solution(self):
        # Empty the linearPrograms folder
        self.empty_folder(self.lp_output_folder)
        # Empty the solutions folder
        self.empty_folder(self.sol_output_folder)

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
                glp_command = ["glpsol", "--lp", lp_file, "-o", sol_file]
                if self.timer:
                    glp_command.append("--tmlim " + str(self.duration_timer))  #600 billions nns = 10 m
                print(glp_command)
                #subprocess.run(["glpsol", "--lp", lp_file, "-o", sol_file])
                glpsol_output = subprocess.run(["glpsol", "--lp", lp_file, "-o", sol_file], capture_output=True,
                                               text=True).stdout

                # Extract and print the time used
                time_used_index = glpsol_output.find("Time used:")
                if time_used_index != -1:
                    time_used = glpsol_output[time_used_index:].splitlines()[0].strip()
                    print(time_used)

    def empty_folder(self, folder):
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)


solution_generatior = SolutionGenerator(sys.argv[1], False)
solution_generatior.generate_solution()
