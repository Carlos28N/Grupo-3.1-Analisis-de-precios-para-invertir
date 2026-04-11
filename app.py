import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("6. Precios de carros (2).csv", on_bad_lines='skip')

df.columns = df.columns.str.strip()
df = df.dropna(how='all')

columnas_numericas = ['Price', 'Mileage', 'Year', 'Engine Size']
for col in columnas_numericas:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=['Price', 'Brand'])

df = df[df['Year'] <= 2026]
df = df[df['Price'] > 0]

df.to_csv("dataset_limpio.csv", index=False)

print("¡Listo! Tu dataset ha sido purificado y guardado como 'dataset_limpio.csv'")
print(df.head()) 
