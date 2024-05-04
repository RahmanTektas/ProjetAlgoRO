import os
import matplotlib.pyplot as plt

class SolutionAnalyzer:
    # Path to the folder containing the sol files
    sol_folder_path = 'solutions/'
    # List all files in the folder
    sol_files = os.listdir(sol_folder_path)
    # Dictionary to store the objective values for each sol file
    objectives = {}

    def __init__(self, model_type):
        self.model_type = model_type

    def analyze(self):
        # Iterate over each sol file in the folder
        for sol_file_name in self.sol_files:
            # Construct the full path to the sol file
            sol_file_path = os.path.join(self.sol_folder_path, sol_file_name)

            # Open the sol file
            with open(sol_file_path, 'r') as sol_file:
                # Read the contents of the sol file
                sol_contents = sol_file.read()

                # Find the line containing the objective value
                objective_line = [line for line in sol_contents.split('\n') if 'Objective' in line]

                # If the line is found, extract the objective value
                if objective_line:
                    objective_value = objective_line[0].split('=')[1].strip().split()[0]

                    # Print the objective value
                    print(f"Objective value in {sol_file_name}: {objective_value}")
                    self.objectives[sol_file_name] = objective_value

    def generate_graph(self):
        # Extract sol file names and objective values
        sol_files = list(self.objectives.keys())
        objective_values = [float(value) for value in self.objectives.values()]

        # Plot the objective values
        plt.figure(figsize=(10, 6))
        plt.bar(sol_files, objective_values, color='skyblue')
        plt.xlabel('Fichier sol')
        plt.ylabel('Valeur fonction objectif')

        if self.model_type == 0:
            plt.title('valeur fonction objectif pour modèle agrégé')
        else:
            plt.title('valeur fonction objectif pour modèle désagrégé')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()



# Instantiate the SolutionAnalyzer and call the analyze method
analyzer = SolutionAnalyzer(1)
analyzer.analyze()
# Generate the graph
analyzer.generate_graph()