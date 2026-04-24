import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="AppComparendo", layout="wide")

st.title("🚛 Estado de Conductores - SIMIT")

try:
    df = pd.read_csv("cache_simit.csv")

    df["estado"] = df["saldo"].apply(
        lambda x: "❌ NO APTO" if x > 0 else "✅ APTO"
    )

    st.dataframe(df, use_container_width=True)

    # 📥 Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)

    st.download_button(
        "📥 Descargar Excel",
        output.getvalue(),
        "reporte_simit.xlsx"
    )

except:
    st.warning("⚠️ No hay datos. Ejecuta el scraper primero.")
