import os
import sys
import pytest
import importlib.util


def run_tests_on_mutant(mutant_file):
    # Dynamically import the mutant
    spec = importlib.util.spec_from_file_location("Polynomial", mutant_file)
    mutant_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mutant_module)

    # Replace the original Polynomial with the mutant version
    sys.modules['Polynomial'] = mutant_module

    # Run the tests
    result = pytest.main(['-v', 'polytest.py'])

    return result == 0  # Return True if all tests pass (mutant survives)


def main():
    mutants_dir = 'mutants'
    survived_mutants = []
    killed_mutants = []

    for mutant_file in os.listdir(mutants_dir):
        if mutant_file.endswith('.py'):
            full_path = os.path.join(mutants_dir, mutant_file)
            print(f"\nTesting mutant: {mutant_file}")
            if run_tests_on_mutant(full_path):
                survived_mutants.append(mutant_file)
                print(f"Mutant {mutant_file} survived!")
            else:
                killed_mutants.append(mutant_file)
                print(f"Mutant {mutant_file} was killed.")

    print("\nSummary:")
    print(f"Total mutants: {len(survived_mutants) + len(killed_mutants)}")
    print(f"Survived mutants: {len(survived_mutants)}")
    print(f"Killed mutants: {len(killed_mutants)}")
    print("\nSurvived mutants:")
    for mutant in survived_mutants:
        print(f"- {mutant}")


if __name__ == "__main__":
    main()
