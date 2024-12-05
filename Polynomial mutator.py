import ast
import astor
import random

class PolynomialMutator(ast.NodeTransformer):
    def __init__(self):
        self.mutations = []

    def visit_Num(self, node):
        # Coefficient Change (CC)
        if random.random() < 0.1:
            new_value = node.n + random.choice([-1, 1])
            self.mutations.append(f"CC: Changed {node.n} to {new_value}")
            return ast.Num(n=new_value)
        return node

    def visit_BinOp(self, node):
        # Arithmetic Operation Swap (AOS)
        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)) and random.random() < 0.1:
            ops = {ast.Add: ast.Sub(), ast.Sub: ast.Add(), ast.Mult: ast.Div(), ast.Div: ast.Mult()}
            new_op = ops[type(node.op)]
            self.mutations.append(f"AOS: Changed {type(node.op).__name__} to {type(new_op).__name__}")
            return ast.BinOp(left=node.left, op=new_op, right=node.right)
        return node

    def visit_Compare(self, node):
        # Comparison Operator Mutation (COM)
        if random.random() < 0.1:
            ops = {ast.Lt: ast.LtE(), ast.LtE: ast.Lt(), ast.Gt: ast.GtE(), ast.GtE: ast.Gt(),
                   ast.Eq: ast.NotEq(), ast.NotEq: ast.Eq()}
            if type(node.ops[0]) in ops:
                new_op = ops[type(node.ops[0])]
                self.mutations.append(f"COM: Changed {type(node.ops[0]).__name__} to {type(new_op).__name__}")
                node.ops[0] = new_op
        return node

def mutate_polynomial(source_code, num_mutants=5):
    mutants = []
    for i in range(num_mutants):
        tree = ast.parse(source_code)
        mutator = PolynomialMutator()
        mutated_tree = mutator.visit(tree)
        mutated_code = astor.to_source(mutated_tree)
        mutants.append((f"mutant_{i}.py", mutated_code, mutator.mutations))
    return mutants

# Example usage
polynomial_code = """
class Polynomial:
    def __init__(self, coefficients):
        self.coefficients = coefficients

    def __add__(self, other):
        max_length = max(len(self.coefficients), len(other.coefficients))
        padded_self = [0] * (max_length - len(self.coefficients)) + self.coefficients
        padded_other = [0] * (max_length - len(other.coefficients)) + other.coefficients
        result_coefficients = [a + b for a, b in zip(padded_self, padded_other)]
        return Polynomial(result_coefficients)

    def evaluate(self, x):
        result = 0
        for i, coef in enumerate(self.coefficients):
            result += coef * (x ** (len(self.coefficients) - i - 1))
        return result
"""

mutants = mutate_polynomial(polynomial_code)

for filename, code, mutations in mutants:
    print(f"Mutant: {filename}")
    print("Mutations applied:")
    for mutation in mutations:
        print(f"- {mutation}")
    print("Mutated code:")
    print(code)
    print("\n")

import os

output_dir = "mutants"
os.makedirs(output_dir, exist_ok=True)

for filename, code, _ in mutants:
    with open(os.path.join(output_dir, filename), "w") as f:
        f.write(code)
