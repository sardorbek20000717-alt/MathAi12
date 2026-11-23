import sympy as sp
import pytesseract
from PIL import Image
from pathlib import Path
import re

x = sp.symbols("x")

def tozalash(misol):
    misol = misol.replace("Xx", "x")
    misol = misol.replace("X", "x")
    misol = misol.replace("×", "*")
    misol = misol.replace("÷", "/")
    misol = misol.replace("−", "-")
    misol = misol.replace(" ", "")
    misol = re.sub(r"(\d)(x)", r"\1*x", misol)
    misol = re.sub(r"(\d)\(", r"\1*(", misol)
    return misol

def yechish(misol):
    misol = tozalash(misol)

    if "=" not in misol:
        print("❌ Tenglama topilmadi.")
        return

    chap, ong = misol.split("=", 1)

    chap_sp = sp.sympify(chap, locals={"x": x})
    ong_sp = sp.sympify(ong, locals={"x": x})

    tenglama = sp.Eq(chap_sp, ong_sp)
    javob = sp.solve(tenglama, x)

    print("\n📚 BOSQICHMA-BOSQICH YECHIM")
    print("-----------------------------")
    print("Misol:", misol)

    if javob:
        qiymat = javob[0]

        # Oddiy chiziqli tenglamalar uchun
        if chap_sp.has(x) and not ong_sp.has(x):
            a = chap_sp.coeff(x)
            b = chap_sp.subs(x, 0)

            print(f"\n1-qadam: {a}x + {b} = {ong_sp}")
            print(f"2-qadam: {a}x = {ong_sp} - ({b})")

            natija = ong_sp - b
            print(f"3-qadam: {a}x = {natija}")

            print(f"4-qadam: x = {natija} / {a}")
            print(f"\n✅ Javob: x = {qiymat}")

        else:
            print("\nYechim:", javob)
            print(f"✅ Javob: x = {qiymat}")

    else:
        print("❌ Yechim topilmadi.")


print("================================")
print("       PHOTO MATH AI 4.0")
print("================================")

while True:
    print("\n1. Misol yozish")
    print("2. Rasmdan misol o'qish")
    print("3. Chiqish")

    tanlov = input("Tanlang: ")

    try:
        if tanlov == "1":
            misol = input("Misol: ")
            yechish(misol)

        elif tanlov == "2":
            rasm = input("Rasm manzili: ")
            fayl = Path(rasm).expanduser()

            if not fayl.exists():
                print("❌ Rasm topilmadi!")
                continue

            matn = pytesseract.image_to_string(
                Image.open(fayl),
                config="--psm 6"
            )

            print("\n📷 OCR natijasi:")
            print(matn)

            misollar = [
                q.strip()
                for q in matn.splitlines()
                if "=" in q
            ]

            if not misollar:
                print("❌ Tenglama topilmadi!")
                continue

            misol = misollar[0]
            print("\n🔧 Tuzatilgan misol:", tozalash(misol))

            yechish(misol)

        elif tanlov == "3":
            print("Dastur yopildi.")
            break

        else:
            print("❌ Noto'g'ri tanlov!")

    except Exception as e:
        print("\n❌ Xatolik:", e)
