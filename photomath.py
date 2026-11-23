import sympy as sp
import pytesseract
from PIL import Image
from pathlib import Path

x = sp.symbols("x")

print("==============================")
print("       PHOTO MATH AI")
print("==============================")

while True:
    print("\n1. Misol yozish")
    print("2. Rasmdan misol o'qish")
    print("3. Chiqish")

    tanlov = input("Tanlang: ")

    try:
        if tanlov == "1":
            misol = input("Misol: ")
            chap, ong = misol.split("=")
            tenglama = sp.Eq(
                sp.sympify(chap),
                sp.sympify(ong)
            )
            print("Javob:", sp.solve(tenglama, x))

        elif tanlov == "2":
            rasm = input("Rasm manzili: ")
            fayl = Path(rasm).expanduser()

            matn = pytesseract.image_to_string(Image.open(fayl))
            print("O'qilgan matn:", matn)
            misol = matn.splitlines()[0]
misol = misol.replace("Xx", "x").replace("X", "x")
misol = misol.replace(" ", "")            chap, ong = misol.split("=")

            tenglama = sp.Eq(
                sp.sympify(chap),
                sp.sympify(ong)
            )
            print("Javob:", sp.solve(tenglama, x))

        elif tanlov == "3":
            break

    except Exception as e:
        print("Xatolik:", e)	
