from playwright.sync_api import sync_playwright
import re
import time

def limpiar_valor(texto):
    try:
        return int(re.sub(r"[^\d]", "", texto))
    except:
        return 0

def consultar_simit_real(cedula):

    resultado = {
        "cedula": cedula,
        "saldo": 0,
        "comparendos": 0,
        "detalle": "Sin información",
        "error": None
    }

    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=False)  # 👈 LOCAL
            page = browser.new_page()

            page.goto("https://www.fcm.org.co/simit/#/estado-cuenta")

            page.wait_for_selector("input", timeout=20000)

            page.fill("input", str(cedula))
            time.sleep(1)

            page.keyboard.press("Enter")

            page.wait_for_timeout(6000)

            content = page.content().lower()

            if "no se encontraron" in content:
                resultado["detalle"] = "Sin comparendos"
                browser.close()
                return resultado

            valores = re.findall(r"\$\s?[\d\.]+", content)

            if valores:
                resultado["saldo"] = limpiar_valor(valores[0])

            if resultado["saldo"] > 0:

                filas = page.query_selector_all("table tr")

                detalles = []

                for fila in filas:
                    texto = fila.inner_text()

                    if "$" in texto:
                        detalles.append(texto.replace("\n", " | "))

                resultado["comparendos"] = len(detalles)
                resultado["detalle"] = " || ".join(detalles[:5])

            else:
                resultado["detalle"] = "Histórico sin deuda"

            browser.close()

    except Exception as e:
        resultado["error"] = str(e)

    return resultado
