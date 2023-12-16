import re


class Calculator:
    def __init__(self):
        self.operations = {"+": 0, "-": 0, "/": 1, "*": 1}

    @staticmethod
    def is_number(symbol):
        try:
            float(symbol)
            return True
        except ValueError:
            return False

    @staticmethod
    def input_to_tokens(input):
        tokens = re.findall(r'\d+\.\d+|\d+|[-+*/()]|\S', input)
        return [token.strip() for token in tokens]

    def tokens_to_rpn(self, tokens):
        answer = []
        stack = []
        unary_minus = False
        for index, symbol in enumerate(tokens):
            if Calculator.is_number(symbol):
                if unary_minus is True:
                    symbol = "-" + symbol
                    unary_minus = False
                answer.append(symbol)
            elif symbol == "(":
                stack.append(symbol)
            elif symbol == ")":
                while stack and stack[-1] != "(":
                    answer.append(stack.pop())
                if stack:
                    stack.pop()
                else:
                    raise ValueError("Нет открывающей скобки")
            elif symbol in self.operations:
                if symbol == "-" \
                    and (index != len(tokens) - 1 and Calculator.is_number(tokens[index + 1])) \
                        and (index == 0 or not Calculator.is_number(tokens[index - 1])):
                    unary_minus = True
                else:
                    while stack and stack[-1] != "(" and self.operations[stack[-1]] >= self.operations[symbol]:
                        answer.append(stack.pop())
                    stack.append(symbol)
            else:
                raise ValueError("Некорректный ввод")

        while len(stack) > 0:
            answer.append(stack.pop())
        return answer

    @staticmethod
    def calculate(rpn):
        stack = []
        for symbol in rpn:
            if Calculator.is_number(symbol):
                if float(symbol).is_integer():
                    stack.append(int(float(symbol)))
                else:
                    stack.append(float(symbol))
            else:
                if len(stack) < 2:
                    raise ValueError("Некорректный ввод")
                else:
                    second = stack.pop()
                    first = stack.pop()

                    if symbol == "+":
                        stack.append(first + second)
                    elif symbol == "-":
                        stack.append(first - second)
                    elif symbol == "*":
                        stack.append(first * second)
                    elif symbol == "/":
                        if second == 0:
                            raise ValueError("Деление на ноль")
                        else:
                            stack.append(first / second)

        output = sum(stack)
        if type(output) is not int:
            output = int(output) if output.is_integer() else output
        return output

    def apply(self, input):
        tokens = Calculator.input_to_tokens(input)
        rpn = self.tokens_to_rpn(tokens)
        return self.calculate(rpn)
