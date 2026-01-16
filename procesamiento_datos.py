import pandas as pd
import numpy as np

# ==========================================
# 1. CONFIGURACION
# ==========================================
archivo_publicos = 'donantes_publicos.csv'
archivo_privados = 'donantes_privados.csv'
nombre_archivo_salida = 'dataset_final.csv'

# ==========================================
# 2. DICCIONARIO DE DONANTES (Códigos -> Nombres Reales)
# ==========================================
diccionario_donantes = {
    # --- PAÍSES (Oficiales) ---
    'Germany': 'Alemania', 'DEU': 'Alemania',
    'Spain': 'España', 'ESP': 'España',
    'United States': 'Estados Unidos', 'USA': 'Estados Unidos',
    'France': 'Francia', 'FRA': 'Francia',
    'Canada': 'Canadá', 'CAN': 'Canadá',
    'Japan': 'Japón', 'JPN': 'Japón',
    'Italy': 'Italia', 'ITA': 'Italia',
    'United Kingdom': 'Reino Unido', 'GBR': 'Reino Unido',
    'Sweden': 'Suecia', 'SWE': 'Suecia',
    'Switzerland': 'Suiza', 'CHE': 'Suiza',
    'Netherlands': 'Países Bajos', 'NLD': 'Países Bajos',
    'Norway': 'Noruega', 'NOR': 'Noruega',
    'Australia': 'Australia', 'AUS': 'Australia',
    'Ireland': 'Irlanda', 'IRL': 'Irlanda',
    'EU Institutions': 'Unión Europea', 'EU': 'Unión Europea',
    'Korea': 'Corea del Sur', 'KOR': 'Corea del Sur',
    'Denmark': 'Dinamarca', 'DNK': 'Dinamarca',
    'Belgium': 'Bélgica', 'BEL': 'Bélgica',
    'Austria': 'Austria', 'AUT': 'Austria',
    'Finland': 'Finlandia', 'FIN': 'Finlandia',
    
    # --- PRIVADOS (Códigos OCDE - ACTUALIZADO) ---
    '9PRIV1601': 'Fundación Bill & Melinda Gates',
    '9PRIV1626': 'Fundación Gordon y Betty Moore',
    '9PRIV1627': 'Fundación Ford',
    '9PRIV1628': 'Wellcome Trust',
    '9PRIV1639': 'Fundación La Caixa',
    '9PRIV1640': 'Fundación Bloomberg',
    '9PRIV1641': 'Fundación Susan T. Buffett',
    '9PRIV1644': 'Fundación Botnar',
    '9PRIV1646': 'Bezos Earth Fund',
    '9PRIV1611': 'Children\'s Investment Fund (CIFF)',
    '9PRIV1629': 'Fundación UBS Optimus',
    
    # --- DONANTES SECRETOS REVELADOS ---
    '9PRIV1643': 'Open Society Foundations',
    '9PRIV1650': 'Good Ventures Foundation',
    '9PRIV1636': 'Jacobs Foundation',
    '9PRIV1618': 'Fundación David y Lucile Packard',
    '9PRIV1619': 'Fundación MacArthur',
    '9PRIV1637': 'Arcadia Fund',
    '9PRIV1638': 'Fundación Margaret A. Cargill',
    '9PRIV1645': 'Fundación CHANEL'
}

def obtener_nombre_donante(texto_original, codigo_original):
    # 1. Intentamos buscar por el código exacto
    codigo = str(codigo_original).strip()
    if codigo in diccionario_donantes:
        return diccionario_donantes[codigo]
    
    # 2. Intentamos buscar por el nombre texto
    nombre = str(texto_original).strip()
    if nombre in diccionario_donantes:
        return diccionario_donantes[nombre]
    
    # 3. Si no está en la lista y es un código privado raro, lo dejamos bonito
    if 'PRIV' in codigo:
        return f"Donante Privado ({codigo})"
        
    # 4. Si todo falla, devolvemos el nombre original si es largo, o el código
    return nombre if len(nombre) > 2 else codigo

# ==========================================
# 3. FUNCIONES DE SECTOR Y ODS
# ==========================================
def traducir_sector(valor_sector):
    codigo = str(valor_sector).strip()
    if codigo.startswith('11'): return 'Educación'
    if codigo.startswith('12'): return 'Salud'
    if codigo.startswith('13'): return 'Salud Reproductiva y Población'
    if codigo.startswith('14'): return 'Agua y Saneamiento'
    if codigo.startswith('15'): return 'Gobierno y Sociedad Civil (DDHH)'
    if codigo.startswith('16'): return 'Servicios Sociales y Pobreza'
    if codigo.startswith('21'): return 'Transporte'
    if codigo.startswith('23'): return 'Energía'
    if codigo.startswith('31'): return 'Agricultura y Pesca'
    if codigo.startswith('32'): return 'Industria'
    if codigo == '400' or codigo.startswith('400'): return 'Proyectos Multisectoriales'
    if codigo.startswith('41'): return 'Protección Ambiental'
    if codigo.startswith('43'): return 'Multisector / Transversal'
    if codigo.startswith('51'): return 'Apoyo Presupuestario'
    if codigo.startswith('91'): return 'Costos Administrativos'
    return 'Otros Sectores'

def mapear_ods(valor_sector):
    codigo = str(valor_sector).strip()
    if codigo.startswith('11'): return 'ODS 4: Educación de Calidad'
    elif codigo.startswith('12') or codigo.startswith('13'): return 'ODS 3: Salud y Bienestar'
    elif codigo.startswith('14'): return 'ODS 6: Agua Limpia'
    elif codigo.startswith('15'): return 'ODS 16: Paz, Justicia e Inst.'
    elif codigo.startswith('16'): return 'ODS 1: Fin de la Pobreza'
    elif codigo.startswith('23'): return 'ODS 7: Energía Asequible'
    elif codigo.startswith('31'): return 'ODS 2: Hambre Cero'
    elif codigo.startswith('41'): return 'ODS 13: Acción por el Clima'
    elif codigo.startswith('32'): return 'ODS 8: Trabajo Decente'
    elif codigo.startswith('5') or codigo.startswith('40') or codigo.startswith('43'): return 'ODS 17: Alianzas / Multisector'
    else: return 'ODS 17: Otros'

# ==========================================
# 4. PROCESAMIENTO
# ==========================================
print(">>> Procesando V10 Correccion: Descifrando Donantes Secretos...")

def cargar_y_limpiar(ruta, etiqueta_origen):
    try:
        df = pd.read_csv(ruta, on_bad_lines='skip', low_memory=False)
        df.columns = df.columns.str.lower().str.strip()
        df = df.loc[:, ~df.columns.duplicated()]
        df['origen_fondos'] = etiqueta_origen
        print(f"[OK] Cargado: {etiqueta_origen} ({len(df)} filas)")
        return df
    except FileNotFoundError:   # <--- AQUÍ FALTABAN LOS DOS PUNTOS
        print(f"[ERROR] No encuentro el archivo '{ruta}'")
        return pd.DataFrame()

df_oficial = cargar_y_limpiar(archivo_publicos, 'Oficial (Gobiernos)')
df_privado = cargar_y_limpiar(archivo_privados, 'Privado (Fundaciones)')

if not df_oficial.empty or not df_privado.empty:
    df_maestro = pd.concat([df_oficial, df_privado], ignore_index=True)

    # 1. ENCONTRAR COLUMNAS DE DONANTE
    posibles_nombres = ['donor name', 'donor_name', 'agency name', 'donor', 'donante']
    col_nombre = next((c for c in df_maestro.columns if c in posibles_nombres and 'code' not in c), 'donor')
    # Backup para el código
    col_codigo = 'donor' if 'donor' in df_maestro.columns else col_nombre

    # 2. APLICAR TRADUCCIÓN DE DONANTES
    df_maestro['nombre_donante'] = df_maestro.apply(
        lambda row: obtener_nombre_donante(row[col_nombre], row.get(col_codigo, '')), axis=1
    )

    # 3. SECTORES Y ODS
    posibles_sector = ['sector name', 'purpose name', 'sector', 'purpose_name']
    col_sector_codigo = next((c for c in df_maestro.columns if c in posibles_sector), None)
    
    if col_sector_codigo:
        df_maestro['nombre_sector'] = df_maestro[col_sector_codigo].apply(traducir_sector)
        df_maestro['ods_estimado'] = df_maestro[col_sector_codigo].apply(mapear_ods)
    else:
        df_maestro['nombre_sector'] = 'Desconocido'
        df_maestro['ods_estimado'] = 'Sin Informacion'

    # 4. LIMPIAR MONTOS
    posibles_monto = ['value', 'amount', 'obs_value', 'usd_disbursement']
    col_monto = next((c for c in df_maestro.columns if c in posibles_monto), None)
    if col_monto:
        df_maestro['monto_usd'] = pd.to_numeric(df_maestro[col_monto], errors='coerce').fillna(0)
    
    # ==========================================
    # 5. EXPORTACIÓN FINAL
    # ==========================================
    cols_deseadas = ['origen_fondos', 'nombre_donante', 'nombre_sector', 'ods_estimado', 'monto_usd', 
                     'time_period', 'recipient']
    
    cols_finales = [c for c in cols_deseadas if c in df_maestro.columns]
    
    df_maestro[cols_finales].to_csv(nombre_archivo_salida, index=False, encoding='utf-8-sig')
    
    print(f"\n[EXITO] Archivo FINAL creado: {nombre_archivo_salida}")
    print(">>> Se han traducido los códigos '9PRIV...' a nombres reales.")

else:
    print("[ERROR] Fallo la carga.")