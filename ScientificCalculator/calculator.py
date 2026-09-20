import ast
import math
import operator


class SafeCalculator:
    """Safe scientific expression evaluator."""

    def __init__(self):
        self.angle_mode = "DEG"

        self.binary_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
        }

        self.unary_operators = {
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
        }

    def _angle(self, value):
        """Convert an input angle according to the current mode."""
        if self.angle_mode == "DEG":
            return math.radians(value)
        return value

    def _sin(self, value):
        return math.sin(self._angle(value))

    def _cos(self, value):
        return math.cos(self._angle(value))

    def _tan(self, value):
        return math.tan(self._angle(value))

    def _asin(self, value):
        result = math.asin(value)
        return math.degrees(result) if self.angle_mode == "DEG" else result

    def _acos(self, value):
        result = math.acos(value)
        return math.degrees(result) if self.angle_mode == "DEG" else result

    def _atan(self, value):
        result = math.atan(value)
        return math.degrees(result) if self.angle_mode == "DEG" else result

    def _factorial(self, value):
        if value < 0 or not float(value).is_integer():
            raise ValueError("Factorial requires a non-negative integer.")
        if value > 170:
            raise ValueError("Number is too large.")
        return math.factorial(int(value))

    def _functions(self):
        return {
            "sin": self._sin,
            "cos": self._cos,
            "tan": self._tan,
            "asin": self._asin,
            "acos": self._acos,
            "atan": self._atan,
            "log": math.log10,
            "ln": math.log,
            "sqrt": math.sqrt,
            "abs": abs,
            "factorial": self._factorial,
        }

    def evaluate(self, expression):
        """Evaluate an expression using a restricted AST."""
        expression = expression.strip()

        if not expression:
            return 0

        # Calculator-friendly replacements
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("−", "-")
        expression = expression.replace("^", "**")

        try:
            tree = ast.parse(expression, mode="eval")
            return self._evaluate_node(tree.body)
        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero.")
        except OverflowError:
            raise ValueError("Result is too large.")
        except ValueError:
            raise
        except Exception:
            raise ValueError("Invalid expression.")

    def _evaluate_node(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                if not math.isfinite(node.value):
                    raise ValueError("Invalid number.")
                return node.value
            raise ValueError("Invalid value.")

        if isinstance(node, ast.BinOp):
            if type(node.op) not in self.binary_operators:
                raise ValueError("Operator not allowed.")

            left = self._evaluate_node(node.left)
            right = self._evaluate_node(node.right)

            # Prevent unreasonable exponentiation
            if isinstance(node.op, ast.Pow):
                if abs(right) > 1000:
                    raise ValueError("Exponent is too large.")

            return self.binary_operators[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp):
            if type(node.op) not in self.unary_operators:
                raise ValueError("Operator not allowed.")

            value = self._evaluate_node(node.operand)
            return self.unary_operators[type(node.op)](value)

        if isinstance(node, ast.Name):
            constants = {
                "pi": math.pi,
                "e": math.e,
            }

            if node.id in constants:
                return constants[node.id]

            raise ValueError(f"Unknown value: {node.id}")

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Invalid function.")

            functions = self._functions()

            if node.func.id not in functions:
                raise ValueError(f"Unknown function: {node.func.id}")

            if len(node.args) != 1:
                raise ValueError("Function requires one argument.")

            argument = self._evaluate_node(node.args[0])

            return functions[node.func.id](argument)

        raise ValueError("Invalid expression.")
