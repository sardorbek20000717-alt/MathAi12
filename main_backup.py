import math
import re
import sympy as sp

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

# ==========================================
# MATH AI 12.0
# ==========================================

x, y = sp.symbols("x y")


# ==========================================
# MATEMATIK FUNKSIYALAR
# ==========================================

def lokal():
    return {
        "x": x,
        "y": y,
        "sqrt": sp.sqrt,
        "pi": sp.pi,
        "E": sp.E,
        "sin": lambda a: sp.sin(sp.pi * a / 180),
        "cos": lambda a: sp.cos(sp.pi * a / 180),
        "tan": lambda a: sp.tan(sp.pi * a / 180),
        "cot": lambda a: sp.cot(sp.pi * a / 180),
        "log": sp.log,
        "ln": sp.log,
        "abs": sp.Abs
    }


def tozalash(m):
    m = m.strip()
    m = m.replace("×", "*")
    m = m.replace("÷", "/")
    m = m.replace("−", "-")
    m = m.replace("^", "**")
    m = m.replace("√", "sqrt")
    m = m.replace("X", "x")
    m = m.replace(" ", "")

    m = re.sub(r"(\d)([xy])", r"\1*\2", m)
    m = re.sub(r"(\d)", r"\1*(", m)
    m = re.sub(r"\(", r")*(", m)
    m = re.sub(r"([xy])\(", r"\1*(", m)

    return m


# ==========================================
# HISOBLASH
# ==========================================

def hisoblash(misol):
    misol = tozalash(misol)

    if not misol:
        return "❌ Misol kiritilmadi."

    try:
        if "=" not in misol:
            natija = sp.sympify(misol, locals=lokal())
            natija = sp.simplify(natija)

            javob = "🧮 HISOBLASH\n\n"
            javob += f"Misol: {misol}\n\n"
            javob += f"Javob: {natija}"

            if not natija.free_symbols:
                try:
                    javob += f"\nTaxminiy: {natija.evalf()}"
                except:
                    pass

            return javob

        chap, ong = misol.split("=", 1)

        chap_s = sp.sympify(chap, locals=lokal())
        ong_s = sp.sympify(ong, locals=lokal())

        tenglama = sp.Eq(chap_s, ong_s)

        if y in (chap_s - ong_s).free_symbols:
            javob = sp.solve(tenglama, (x, y))
            return (
                "🔗 SISTEMA / 2 NOMA'LUM\n\n"
                f"Tenglama: {misol}\n\n"
                f"Natija: {javob}"
            )

        p = sp.Poly(sp.expand(chap_s - ong_s), x)

        if p.degree() == 1:
            a, b = p.all_coeffs()

            natija = sp.solve(tenglama, x)

            return (
                "📘 CHIZIQLI TENGLAMA\n\n"
                f"Boshlang'ich:\n{misol}\n\n"
                "1-qadam:\n"
                f"{a}x = {-b}\n\n"
                "2-qadam:\n"
                f"x = {-b}/{a}\n\n"
                "3-qadam:\n"
                f"✅ x = {natija}"
            )

        if p.degree() == 2:
            a, b, c = p.all_coeffs()
            D = sp.simplify(b**2 - 4*a*c)
            natija = sp.solve(tenglama, x)

            return (
                "📕 KVADRAT TENGLAMA\n\n"
                f"Boshlang'ich:\n{misol}\n\n"
                "1-qadam: Diskriminant\n"
                "D = b² - 4ac\n\n"
                f"D = {D}\n\n"
                "2-qadam:\n"
                "x = (-b ± √D) / 2a\n\n"
                f"✅ Javob: {natija}"
            )

        natija = sp.solve(tenglama, x)

        return (
            "📚 TENGLAMA\n\n"
            f"Misol: {misol}\n\n"
            f"Yechim: {natija}"
        )

    except Exception as e:
        return f"❌ Xatolik.\n\nMisolni tekshiring.\n\n{e}"


# ==========================================
# FOIZ
# ==========================================

def foiz_hisobla(son, foiz):
    try:
        son = float(son)
        foiz = float(foiz)

        natija = son * foiz / 100

        return (
            "📊 FOIZ\n\n"
            f"{son} ning {foiz}% i\n\n"
            f"= {natija:g}"
        )
    except:
        return "❌ Sonlarni to'g'ri kiriting."


# ==========================================
# PROPORSIYA
# a : b = c : x
# ==========================================

def proporsiya_hisobla(a, b, c):
    try:
        a = float(a)
