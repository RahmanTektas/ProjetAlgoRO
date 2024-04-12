import sys
from exceptions.IncorrectFormatError import IncorrectFormatError
from AggregatedModelGenerator import AggregatedModelGenerator
from DisaggregatedModelGenerator import DisaggregatedModelGenerator


def main():
    try:
        if len(sys.argv) != 3:
            raise IncorrectFormatError("Usage: python3 generate_model.py instance_file_name.txt model_type(0 or 1).")
        instance_file_name = sys.argv[1].split(".")[0]
        model_type = int(sys.argv[2])
        if model_type == 0:
            model_generator = AggregatedModelGenerator(instance_file_name, model_type)
        else:
            model_generator = DisaggregatedModelGenerator(instance_file_name, model_type)
        model_generator.generate_model()
    except ValueError:
        print("Error: The second argument must be an integer (0 or 1).")
    except IncorrectFormatError as err:
        print(f"Error: {err}")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
