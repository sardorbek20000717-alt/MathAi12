import math

print("================================")
print("      SMART CALCULATOR")
print("================================")
print("Misol kiriting:")
print("2 + 3")
print("sin(30)")
print("cos(60)")
print("tan(45)")
print("sqrt(25)")
print("log(100)")
print("Chiqish: exit")
print("================================")

while True:
    try:
        expression = input(">>> ")

        if expression.lower() == "exit":
            print("Calculator yopildi.")
            break

        expression = expression.replace("^", "**")

        result = eval(
            expression,
            {"__builtins__": {}},
            {
                "sin": lambda x: math.sin(math.radians(x)),
                "cos": lambda x: math.cos(math.radians(x)),
                "tan": lambda x: math.tan(math.radians(x)),
                "sqrt": math.sqrt,
                "log": math.log10,
                "ln": math.log,
                "pi": math.pi,
                "e": math.e,
                "abs": abs
            }
        )

        print("=", result)

    except Exception:
        print("❌ Xato! Misolni tekshiring.")

