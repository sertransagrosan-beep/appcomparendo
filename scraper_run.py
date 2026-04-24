from scraper import consultar_simit_real
import pandas as pd
import time
import random
from datetime import datetime

# 🔴 PON AQUÍ TUS CÉDULAS
cedulas = [
    "12345678",
    "87654321"
]

resultados = []

for cedula in cedulas:

    print(f"Consultando {cedula}...")

    data = consultar_simit_real(cedula)

    resultados.append({
        "cedula": cedula,
        "saldo": data["saldo"],
        "comparendos": data["comparendos"],
        "detalle": data["detalle"],
        "error": data["error"],
        "fecha": datetime.now()
    })

    time.sleep(random.uniform(4, 8))  # evita bloqueo

df = pd.DataFrame(resultados)
df.to_csv("cache_simit.csv", index=False)

print("✅ Consulta finalizada")
