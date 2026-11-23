
import sympy as sp
import pytesseract
from PIL import Image
from pathlib import Path
import re

x = sp.symbols("x")


# =====================================
# 1. MISOLNI TOZALASH
# =====================================
def tozalash(m):
    m = m.strip()
    m = m.replace("×", "*").replace("÷", "/")
    m = m.replace("−", "-").replace("^", "**")
    m = m.replace("√", "sqrt")
    m = m.replace(" ", "")
    m = m.replace("X", "x")

    m = re.sub(r"(\d)(x)", r"\1*\2", m)
    m = re.sub(r"(\d)\(", r"\1*(", m)
    m = re.sub(r"\)\(", r")*(", m)
    m = re.sub(r"(x)\(", r"\1*(", m)

    return m


def lokal():
    return {
        "x": x,
        "sqrt": sp.sqrt,
        "pi": sp.pi,
        "E": sp.E,
        "sin": lambda a: sp.sin(sp.pi*a/180),
        "cos": lambda a: sp.cos(sp.pi*a/180),
        "tan": lambda a: sp.tan(sp.pi*a/180),
        "cot": lambda a: sp.cot(sp.pi*a/180),
        "log": sp.log,
        "abs": sp.Abs
    }


# =====================================
# 2. CHIZIQLI TENGLAMA
# =====================================
def chiziqli_qadamlar(m):
    chap, ong = m.split("=", 1)

    chap = sp.sympify(chap, locals=lokal())
    ong = sp.sympify(ong, locals=lokal())

    tenglama = sp.Eq(chap, ong)
    if sp.Poly(chap - ong, x).degree() != 1:
        return False

    a = sp.expand(chap - ong).coeff(x)
    b = sp.expand(chap - ong).subs(x, 0)

    if a == 0:
        return False

    print("\n📚 BOSQICHMA-BOSQICH YECHIM")
    print("--------------------------------")
    print("Boshlang'ich:", m)

    print("\n1-qadam: x qatnashgan hadni ajratamiz.")
    print(f"{a}*x = {-b}")

    print("\n2-qadam: x oldidagi koeffitsiyentga bo'lamiz.")
    print(f"x = {-b} / {a}")

    javob = sp.solve(tenglama, x)[0]

    print("\n3-qadam: Hisoblaymiz.")
    print(f"x = {javob}")
    print("\n✅ YAKUNIY JAVOB:", javob)

    return True


# =====================================
# 3. KVADRAT TENGLAMA
# =====================================
def kvadrat_yech(m):
    chap, ong = m.split("=", 1)

    chap = sp.sympify(chap, locals=lokal())
    ong = sp.sympify(ong, locals=lokal())

    p = sp.Poly(sp.expand(chap - ong), x)

    if p.degree() != 2:
        return False

    a, b, c = p.all_coeffs()

    D = sp.simplify(b**2 - 4*a*c)

    print("\n📘 KVADRAT TENGLAMA")
    print("--------------------------------")
    print("Standart ko'rinish: ax² + bx + c = 0")
    print(f"a = {a}, b = {b}, c = {c}")

    print("\n1-qadam: Diskriminantni topamiz.")
    print("D = b² - 4ac")
    print(f"D = {sp.expand(D)}")

    print("\n2-qadam: Diskriminantni hisoblaymiz.")
    print("D =", D)

    if D < 0:
        print("\nHaqiqiy ildiz mavjud emas.")
    else:
        print("\n3-qadam: Ildizlarni topamiz.")
        print("x = (-b ± √D) / 2a")

        javob = sp.solve(sp.Eq(chap, ong), x)

        for i, v in enumerate(javob, 1):
            print(f"x{i} = {v}")

        print("\n✅ JAVOB:", javob)

    return True


# =====================================
# 4. UMUMIY HISOBLASH
# =====================================
def hisobla(m):
    try:
        m = tozalash(m)

        if not m:
            print("Misol kiritilmadi.")
            return

        if "=" in m:
            if chiziqli_qadamlar(m):
                return

            if kvadrat_yech(m):
                return

            chap, ong = m.split("=", 1)
            javob = sp.solve(
                sp.Eq(
                    sp.sympify(chap, locals=lokal()),
                    sp.sympify(ong, locals=lokal())
                ), x
            )
            print("\nTenglama yechimi:", javob)
            return

        natija = sp.sympify(m, locals=lokal())
        natija = sp.simplify(natija)

        print("\n🧠 MATH AI HISOBLASH")
        print("--------------------------------")
        print("Misol:", m)
        print("Natija:", natija)

        if not natija.free_symbols:
            print("Taxminiy qiymat:", natija.evalf())

    except Exception as e:
        print("\n❌ Xatolik:", e)


# =====================================
# 5. OCR — RASMDAN MISOL O'QISH
# =====================================
def rasm_oqish():
    manzil = input("Rasm manzili: ")
    fayl = Path(manzil).expanduser()

    if not fayl.exists():
        print("Rasm topilmadi!")
        return

    try:
        matn = pytesseract.image_to_string(
            Image.open(fayl),
            config="--psm 6"
        )

        qatorlar = [
            q.strip()
            for q in matn.splitlines()
            if q.strip()
        ]

        if not qatorlar:
            print("Misol topilmadi!")
            return

        print("\n📷 O'QILGAN MATN:")
        for i, q in enumerate(qatorlar, 1):
            print(f"{i}. {q}")

        tanlov = input(
            "\nMisol raqamini tanlang (Enter = 1): "
        ).strip() or "1"

        idx = int(tanlov) - 1
        hisobla(qatorlar[idx])

    except Exception as e:
        print("OCR xatosi:", e)


# =====================================
# 6. MENYU
# =====================================
print("====================================")
print("         MATH AI 8.0")
print("====================================")
print("Algebra | Kvadrat tenglama")
print("Kasr | Ildiz | Daraja")
print("Trigonometriya | OCR")
print("====================================")

while True:
    print("\n1. Misol yechish")
    print("2. Rasmdan misol o'qish")
    print("3. Chiqish")

    tanlov = input("\nTanlang: ")

    if tanlov == "1":
        m = input("Misol: ")
        hisobla(m)

    elif tanlov == "2":
        rasm_oqish()

    elif tanlov == "3":
        print("Math AI yopildi.")
        break

    else:
        print("Noto'g'ri tanlov!")

