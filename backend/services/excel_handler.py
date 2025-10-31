import pandas as pd
import backend.config as config 

def buscar_numero_parte(numeros_parte):
    mensaje = ""
    filas_resaltadas = []


    try:
        df1 = pd.read_excel(config.DATA_FILE, sheet_name="Hoja1", engine="openpyxl")
        df2 = pd.read_excel(config.DATA_FILE, sheet_name="Hoja2", engine="openpyxl")
        df3 = pd.read_excel(config.DATA_FILE, sheet_name="Hoja3", engine="openpyxl")
    except Exception as e:
        return f"Error al leer el archivo Excel: {str(e)}", []

    # Convertir a string y eliminar espacios extra
    df1 = df1.applymap(lambda x: str(x).strip() if pd.notna(x) else x)
    df2 = df2.applymap(lambda x: str(x).strip() if pd.notna(x) else x)
    df3 = df3.applymap(lambda x: str(x).strip() if pd.notna(x) else x)

    for numero_parte in numeros_parte:
        fila_df1 = df1[df1.iloc[:, 0].astype(str).str.strip() == numero_parte]

        if fila_df1.empty:
            mensaje += f"<div class='resultado'><h3>Número de parte '{numero_parte}' no encontrado en la base de datos.</h3></div>"
        else:
            resultados_ordenados = []

            for _, row in fila_df1.iterrows():
                molex_pn = row[0]
                version = row[1]   # Valor de la columna B
                valores_buscados = row[2:].dropna().tolist()
                
                # ✅ Contamos cuántas veces aparece cada valor en la búsqueda
                valores_buscados_contador = {val: valores_buscados.count(val) for val in set(valores_buscados)}
                
                resultados_coincidencias = set()

                for _, row_df2 in df2.iterrows():
                    valores_encontrados_contador = {}  # ✅ Contador de valores encontrados en esta fila

                    for value in row_df2.iloc[1:].dropna():
                        valores_encontrados_contador[value] = valores_encontrados_contador.get(value, 0) + 1

                    # ✅ Verificamos que cada valor buscado esté en la fila con la misma frecuencia
                    coincidencia_valida = all(
                        valores_encontrados_contador.get(val, 0) >= cantidad
                        for val, cantidad in valores_buscados_contador.items()
                    )

                    if coincidencia_valida:
                        resultados_coincidencias.add(row_df2.iloc[0])  # ✅ Guardamos el nombre del tester

                for tester in resultados_coincidencias:
                    fila_df3 = df3[df3.iloc[:, 0].astype(str).str.strip() == tester]

                    if not fila_df3.empty:
                        encontrado = any(numero_parte in str(cell) for cell in fila_df3.iloc[0, :])
                        if encontrado:
                            resultados_ordenados.append(f"{molex_pn} - {tester}: <span style='color:green; font-weight:bold;'>Confirmado</span>")
                        else:
                            resultados_ordenados.append(f"{molex_pn} - {tester}: <span style='color:red; font-weight:bold;'>Validar con Ingeniería de Pruebas en piso</span>")
                    else:
                        resultados_ordenados.append(f"{molex_pn} - {tester}: Tester no habilitado")

            if resultados_ordenados:
                resultados_ordenados = list(set(resultados_ordenados))
                resultados_ordenados.sort()
                # Usamos la variable 'version' como descripción en el título del resultado para mayor claridad
                mensaje += "<div class='resultado'><h3>Resultados para el número de parte '{0}' ({1}):</h3>".format(numero_parte, version)
                mensaje += f"<p><strong>Módulos:</strong> {', '.join(valores_buscados)}</p>"
                for resultado in resultados_ordenados:
                    mensaje += f"<br>{resultado}<br>"
                mensaje += "</div>"
            else:
                mensaje += (
                    "<div class='resultado'><h3>Resultados para el número de parte '{0}' ({1}):</h3>"
                    "<p><strong>No se encontró tester con módulos:</strong> {2}</p></div>"
                ).format(numero_parte, version, ', '.join(valores_buscados))



    return mensaje, filas_resaltadas

def buscar_modulo(modulo):
    mensaje = ""
    filas_resaltadas = []

    try:
        # ✅ Leer la hoja 2
        df = pd.read_excel(config.DATA_FILE, sheet_name="Hoja2", engine="openpyxl", dtype=str)
        df.fillna("", inplace=True)  # Evita errores por NaN
    except Exception as e:
        print(f"❌ Error al leer Hoja2: {e}")
        return f"Error al leer el archivo Excel: {str(e)}", []

    # ✅ Convertir todo a minúsculas y quitar espacios
    df = df.applymap(lambda x: str(x).strip().lower() if pd.notna(x) else "")
    modulo = str(modulo).strip().lower()

    # ✅ Buscar coincidencias (en cualquier columna a partir de la 3)
    coincidencias = []
    for _, fila in df.iterrows():
        valores = [str(v) for v in fila[2:].tolist()]
        if any(modulo in v for v in valores):
            coincidencias.append({
                "FA": fila.iloc[0],
                "EOL": fila.iloc[1]
            })

    # ✅ Generar mensaje HTML
    if coincidencias:
        mensaje += f"<div class='resultado'><h3>Resultados para el módulo '{modulo}':</h3>"
        mensaje += "<table border='1'><tr><th>FA</th><th>EOL</th></tr>"
        for c in coincidencias:
            mensaje += f"<tr><td>{c['FA']}</td><td>{c['EOL']}</td></tr>"
        mensaje += "</table></div>"
        filas_resaltadas = coincidencias
    else:
        mensaje += f"<div class='resultado'><h3>No se encontraron líneas con el módulo '{modulo}'.</h3></div>"

    print(f"🔎 Buscar módulo: '{modulo}', coincidencias encontradas: {len(coincidencias)}")
    return mensaje, filas_resaltadas

# Leer datos de una hoja del Excel
def leer_hoja(hoja):
    try:
        df = pd.read_excel(config.DATA_FILE, sheet_name=hoja, engine="openpyxl", dtype=str)  # ✅ Convertir todo a string
        df.fillna("", inplace=True)  # ✅ Reemplazar valores NaN con cadena vacía
        print(f"Hoja {hoja} cargada con {df.shape[0]} filas y {df.shape[1]} columnas")  # 👀 Depuración
        print(df.head().to_dict())  # 👀 Verificar datos en consola
        return df.values.tolist()  # Convertir DataFrame a lista de listas
    except Exception as e:
        print(f"Error al cargar hoja {hoja}: {e}")
        return {"error": str(e)}

# 🟢 Guardar cambios asegurando que se mantienen los encabezados
def guardar_cambios_excel(hoja, datos):
    try:
        df = pd.DataFrame(datos[1:], columns=datos[0])  # ✅ Mantiene encabezados

        with pd.ExcelWriter(config.DATA_FILE, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=hoja, index=False)

        return "Guardado correctamente con encabezados"
    except Exception as e:
        return f"Error: {str(e)}"
