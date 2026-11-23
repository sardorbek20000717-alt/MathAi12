
import sympy as sp
import pytesseract
from PIL import Image
from pathlib import Path
import re
import math

x, y = sp.symbols("x y")


# =====================================
# 1. MISOLNI TOZALASH
# =====================================
def tozalash(m):
    m = m.strip()
    m = m.replace("×", "*").replace("÷", "/")
    m = m.replace("−", "-").replace("^", "**")
    m = m.replace("√", "sqrt")
    m = m.replace("X", "x")
    m = m.replace(" ", "")
    m = re.sub(r"(\d)([xy])", r"\1*\2", m)
    m = re.sub(r"(\d)\(", r"\1*(", m)
    m = re.sub(r"\)\(", r")*(", m)
    m = re.sub(r"([xy])\(", r"\1*(", m)
    return m


def lokal():
    return {
        "x": x, "y": y,
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
# 2. TENGLAMALAR
# =====================================
def tenglama(m):
    try:
        chap, ong = m.split("=", 1)
        chap = sp.sympify(chap, locals=lokal())
        ong = sp.sympify(ong, locals=lokal())
        teng = sp.Eq(chap, ong)

        if y in (chap - ong).free_symbols:
            print("\nIkki noma'lumli tenglama uchun SISTEMA bo'limidan foydalaning.")
            return

        p = sp.Poly(sp.expand(chap - ong), x)
        daraja = p.degree()

        print("\n📚 TENGLAMA YECHIMI")
        print("--------------------------------")
        print("Boshlang'ich:", m)

        if daraja == 1:
            a, b = p.all_coeffs()
            print("\n1-qadam: x ni ajratamiz.")
            print(f"{a}*x = {-b}")
            print("\n2-qadam: koeffitsiyentga bo'lamiz.")
            print(f"x = {-b}/{a}")
            print("\n3-qadam: hisoblaymiz.")
            print("x =", sp.solve(teng, x))

        elif daraja == 2:
            a, b, c = p.all_coeffs()
            D = sp.simplify(b**2 - 4*a*c)

            print("\n1-qadam: Diskriminant.")
            print("D = b² - 4ac")
            print("D =", D)

            if D < 0:
                print("Haqiqiy ildiz mavjud emas.")
            else:
                print("\n2-qadam: Ildiz formulasini qo'llaymiz.")
                print("x = (-b ± √D) / 2a")
                print("\n3-qadam: Natija.")
                print("x =", sp.solve(teng, x))

        else:
            print("\nYechim:", sp.solve(teng, x))

    except Exception as e:
        print("Tenglama xatosi:", e)


# =====================================
# 3. TENGLAMALAR SISTEMASI
# =====================================
def sistema():
    try:
        print("\nBirinchi tenglama:")
        a = input("1) ")
        print("Ikkinchi tenglama:")
        b = input("2) ")

        a = tozalash(a)
        b = tozalash(b)

        def parse(q):
            chap, ong = q.split("=", 1)
            return sp.Eq(
                sp.sympify(chap, locals=lokal()),
                sp.sympify(ong, locals=lokal())
            )

        print("\n📘 SISTEMA YECHIMI")
        print("1-qadam: Tenglamalarni yozamiz.")
        print("2-qadam: Birgalikda yechamiz.")

        javob = sp.solve((parse(a), parse(b)), (x, y))

        print("3-qadam: Natija.")
        print(javob)

    except Exception as e:
        print("Sistema xatosi:", e)


# =====================================
# 4. ALGEBRA VA KO'PHADLAR
# =====================================
def algebra():
    try:
        m = tozalash(input("Ifoda: "))
        q = sp.sympify(m, locals=lokal())

        print("\n📗 ALGEBRA")
        print("Ifoda:", q)
        print("1. Yoyish:", sp.expand(q))
        print("2. Ko'paytuvchilarga ajratish:", sp.factor(q))
        print("3. Soddalashtirish:", sp.simplify(q))

    except Exception as e:
        print("Algebra xatosi:", e)


# =====================================
# 5. FOIZ VA PROPORSIYA
# =====================================
def foiz():
    try:
        son = float(input("Son: "))
        foiz_qiymat = float(input("Foiz (%): "))

        print("\n📊 FOIZ HISOBLASH")
        print("1-qadam: Sonni foizga ko'paytiramiz.")
        print("2-qadam: 100 ga bo'lamiz.")
        print(f"\n{son} ning {foiz_qiymat}% i = "
              f"{son * foiz_qiymat / 100:g}")

    except Exception as e:
        print("Foiz xatosi:", e)


def proporsiya():
    try:
        a = float(input("a = "))
        b = float(input("b = "))
        c = float(input("c = "))

        if a == 0:
            print("a nol bo'lmasligi kerak.")
            return

        d = b * c / a

        print("\n📊 PROPORSIYA")
        print(f"a : b = c : x")
        print(f"x = b*c/a = {d:g}")

    except Exception as e:
        print("Proporsiya xatosi:", e)


# =====================================
# 6. GEOMETRIYA
# =====================================
def geometriya():
    while True:
        print("\n📐 GEOMETRIYA")
        print("1. Uchburchak")
        print("2. Kvadrat")
        print("3. To'g'ri to'rtburchak")
        print("4. Aylana va doira")
        print("5. Pifagor teoremasi")
        print("6. Kub hajmi")
        print("7. Parallelepiped hajmi")
        print("8. Orqaga")

        tanlov = input("Tanlang: ")

        try:
            if tanlov == "1":
                a = float(input("1-tomon: "))
                b = float(input("2-tomon: "))
                c = float(input("3-tomon: "))

                if min(a, b, c) <= 0 or max(a, b, c) >= sum((a, b, c)) - max(a, b, c):
                    print("Bunday uchburchak mavjud emas.")
                    continue

                p = a + b + c
                s = p / 2
                yuza = math.sqrt(s*(s-a)*(s-b)*(s-c))

                print("Perimetr:", p)
                print("Yuza (Geron formulasi):", yuza)

            elif tanlov == "2":
                a = float(input("Tomon: "))
                print("Perimetr:", 4*a)
                print("Yuza:", a*a)

            elif tanlov == "3":
                a = float(input("Uzunlik: "))
                b = float(input("En: "))
                print("Perimetr:", 2*(a+b))
                print("Yuza:", a*b)

            elif tanlov == "4":
                r = float(input("Radius: "))
                print("Aylana uzunligi:", 2*math.pi*r)
                print("Doira yuzasi:", math.pi*r*r)

            elif tanlov == "5":
                a = float(input("Birinchi katet: "))
                b = float(input("Ikkinchi katet: "))
                print("Gipotenuza:", math.sqrt(a*a+b*b))

            elif tanlov == "6":
                a = float(input("Kub tomoni: "))
                print("Kub hajmi:", a**3)

            elif tanlov == "7":
                a = float(input("Uzunlik: "))
                b = float(input("En: "))
                c = float(input("Balandlik: "))
                print("Hajm:", a*b*c)

            elif tanlov == "8":
                break

            else:
                print("Noto'g'ri tanlov!")

        except Exception as e:
            print("Geometriya xatosi:", e)


# =====================================
# 7. OCR
# =====================================
def rasm_oqish():
    try:
        manzil = input("Rasm manzili: ")
        fayl = Path(manzil).expanduser()

        if not fayl.exists():
            print("Rasm topilmadi!")
            return

        matn = pytesseract.image_to_string(
            Image.open(fayl),
            config="--psm 6"
        )

        qatorlar = [q.strip() for q in matn.splitlines()
                    if q.strip()]

        if not qatorlar:
            print("Misol topilmadi!")
            return

        for i, q in enumerate(qatorlar, 1):
            print(f"{i}. {q}")

        tanlov = input("Misol raqami (Enter=1): ").strip() or "1"
        m = qatorlar[int(tanlov)-1]

        print("O'qilgan misol:", m)
        hisobla(m)

    except Exception as e:
        print("OCR xatosi:", e)


# =====================================
# 8. HISOBLASH
# =====================================
def hisobla(m):
    try:
        m = tozalash(m)

        if "=" in m:
            tenglama(m)
            return

        natija = sp.sympify(m, locals=lokal())

        print("\n🧠 MATH AI NATIJASI")
        print("Misol:", m)
        print("Javob:", sp.simplify(natija))

        if not natija.free_symbols:
            print("Taxminiy:", natija.evalf())

    except Exception as e:
        print("Hisoblash xatosi:", e)


# =====================================
# 9. ASOSIY MENYU
# =====================================
print("====================================")
print("          MATH AI 9.0")
print("====================================")
print("Algebra | Tenglamalar | Sistema")
print("Kasr | Ildiz | Daraja | Foiz")
print("Geometriya | OCR | Proporsiya")
print("====================================")

while True:
    print("\n1. Misol yechish")
    print("2. Rasmdan misol o'qish")
    print("3. Algebra va ko'phadlar")
    print("4. Tenglamalar sistemasi")
    print("5. Foiz")
    print("6. Proporsiya")
    print("7. Geometriya")
    print("8. Chiqish")

    tanlov = input("\nTanlang: ")

    if tanlov == "1":
        hisobla(input("Misol: "))

    elif tanlov == "2":
        rasm_oqish()

    elif tanlov == "3":
        algebra()

    elif tanlov == "4":
        sistema()

    elif tanlov == "5":
        foiz()

    elif tanlov == "6":
        proporsiya()

    elif tanlov == "7":
        geometriya()

    elif tanlov == "8":
        print("Math AI 9.0 yopildi.")
        break

    else:
        print("Noto'g'ri tanlov!")

