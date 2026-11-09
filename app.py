import streamlit as st

st.set_page_config(page_title="Guía", page_icon="🧭", layout="wide")

st.markdown("""
<style>
:root{--navy:#102A43;--blue:#246BCE;--pale:#EAF3FC;--line:#D5E1EC;--gray:#627487}
html,body,[data-testid="stAppViewContainer"]{background:#F5F8FC;color:var(--navy)}
.block-container{max-width:1050px;padding-top:2rem;padding-bottom:3rem}
h1,h2,h3,p,label,[data-testid="stMarkdownContainer"]{color:var(--navy)}
.section-card{background:white;border:1px solid var(--line);border-radius:14px;padding:20px 24px;margin:12px 0 18px}
.step-label{color:var(--blue);font-size:.78rem;font-weight:750;letter-spacing:.06em;margin-bottom:8px}
.result-card{background:var(--pale);border:1px solid #B9D3EE;border-left:5px solid var(--blue);color:var(--navy);border-radius:12px;padding:18px 20px;margin:18px 0}
.result-title{color:var(--blue);font-weight:800;margin-bottom:6px}
div.stButton>button{background:var(--blue);color:white;border:0;border-radius:9px}
div.stButton>button:hover{background:#174F9C;color:white}
</style>
""", unsafe_allow_html=True)

def pregunta(texto, opciones, key):
    return st.radio(texto, opciones, key=key, horizontal=True)

def resultado(texto):
    st.markdown(f'<div class="result-card"><div class="result-title">RESULTADO</div>{texto}</div>', unsafe_allow_html=True)

def tarjeta(etiqueta, texto):
    st.markdown(f'<div class="section-card"><div class="step-label">{etiqueta}</div>{texto}</div>', unsafe_allow_html=True)

st.title("Guía")
procedimiento = pregunta("¿Qué procedimiento realizas?", ["A) Validación", "B) Barrido"], "procedimiento")

if procedimiento == "A) Validación":
    tipo = pregunta("Selecciona el tipo de validación", ["A.1) Validación de red", "A.2) Validación de comercios"], "tipo_validacion")

    if tipo == "A.1) Validación de red":
        tarjeta("A.1) VALIDACIÓN DE RED", "Recorre la red en Google Maps y compárala con Experience Builder. Revisa el histórico de Street View.")
        streetview = pregunta("¿Hay Street View?", ["Sí", "No"], "red_streetview")
        if streetview == "No":
            elemento = pregunta("¿Qué caso corresponde?", ["Zona sin Street View", "Calle sin Street View"], "red_sin_sv")
            resultado("Realizar procedimiento para polígonos sin Street View." if elemento == "Zona sin Street View" else "Realizar procedimiento para líneas sin Street View.")
        else:
            patron = pregunta("¿Observas algún patrón sobre la red?", ["Sí", "No"], "red_patron")
            if patron == "Sí":
                todas = pregunta("¿Todas las acometidas que corresponden al patrón aparecen en Experience Builder?", ["Sí", "No"], "red_todas")
                if todas == "Sí":
                    resultado("Se descarta.")
                else:
                    visible = pregunta("¿La acometida faltante es visible?", ["Sí", "No"], "red_visible")
                    if visible == "Sí":
                        resultado("Pasa a OYM.")
                    else:
                        condicion = pregunta("¿Qué condición se presenta?", ["Algún objeto obstaculiza la visión", "Hay construcción"], "red_condicion")
                        if condicion == "Algún objeto obstaculiza la visión":
                            resultado("Sin suficiente información. Asigna en Workforce.")
                        else:
                            resultado("Realizar procedimiento Experience Builder → PowerApp → SharePoint → Workforce para redes sin acometidas.")
            else:
                tarjeta("REVISIÓN DEL HISTÓRICO", "Verifica el histórico y descarta la presencia de huellas en el pavimento y/o banqueta.")
                resultado("Descarta la red si no encontraste indicios de acometidas ocultas o acometidas visibles no levantadas en GIS.")

    else:
        tarjeta("A.2) VALIDACIÓN DE COMERCIOS", "Busca el comercio en Google Maps. Revisa el histórico de Street View.")
        streetview = pregunta("¿Hay Street View?", ["Sí", "No"], "comercio_streetview")
        if streetview == "No":
            caso = pregunta("¿Qué caso corresponde?", ["Zona sin Street View", "Calle sin Street View"], "comercio_sin_sv")
            resultado("Realizar procedimiento para polígonos sin Street View." if caso == "Zona sin Street View" else "Realizar procedimiento para líneas sin Street View.")
        else:
            acometida = pregunta("¿Hay acometida?", ["Sí", "No"], "comercio_acometida")
            if acometida == "Sí":
                levantada = pregunta("¿Está levantada en GIS?", ["Sí", "No"], "comercio_gis")
                if levantada == "Sí":
                    resultado("Se descarta.")
                else:
                    visible = pregunta("¿Es visible?", ["Sí", "No"], "comercio_visible")
                    if visible == "Sí":
                        resultado("Pasa a OYM. Adjunta evidencia.")
                    else:
                        condicion = pregunta("¿Qué condición se presenta?", ["Algún objeto obstaculiza la visión", "Hay construcción"], "comercio_condicion")
                        if condicion == "Algún objeto obstaculiza la visión":
                            resultado("Sin suficiente información. Adjunta evidencia y asigna en Workforce.")
                        else:
                            resultado("Se confirma. Realizar procedimiento Experience Builder → PowerApp → SharePoint → Workforce para comercios.")
            else:
                tarjeta("REVISIÓN DEL HISTÓRICO", "Verifica el histórico y revisa si hay huellas en el pavimento y/o banqueta.")
                huella = pregunta("¿Hay huella?", ["Sí", "No"], "comercio_huella")
                if huella == "Sí":
                    resultado("Realiza el procedimiento Experience Builder → PowerApp → SharePoint → Workforce para comercios.")
                else:
                    resultado("Descarta.")

else:
    tarjeta("B) BARRIDO", "Recorre las calles, únicamente las que tienen red de ENGIE. Identifica zonas sin Street View. Compara lo que observas en Street View de Google Maps con lo que se encuentra en Experience Builder. Identifica patrones en la ubicación de las acometidas y revisa cuidadosamente el histórico de Street View. Revisa el pavimento para identificar huellas por instalación.")
    streetview = pregunta("¿La zona que recorriste tiene Street View?", ["Sí", "No"], "barrido_streetview")
    if streetview == "No":
        caso = pregunta("¿Qué caso corresponde?", ["Zona sin Street View", "Calle sin Street View"], "barrido_sin_sv")
        resultado("Realizar procedimiento para polígonos sin Street View." if caso == "Zona sin Street View" else "Realizar procedimiento para líneas sin Street View.")
    else:
        patron = pregunta("¿Observaste algún patrón?", ["Sí", "No"], "barrido_patron")
        if patron == "Sí":
            todas = pregunta("¿Todas las acometidas que corresponden al patrón aparecen en Experience Builder?", ["Sí", "No"], "barrido_todas")
            if todas == "Sí":
                resultado("Traza una línea de inspección (procedimiento para reporte de zonas barridas).")
            else:
                visible = pregunta("¿La acometida faltante es visible?", ["Sí", "No"], "barrido_visible")
                if visible == "Sí":
                    resultado("Traza una línea de inspección para pasar a OYM.")
                else:
                    condicion = pregunta("¿Qué condición se presenta?", ["Algún objeto obstaculiza la visión", "Hay construcción"], "barrido_condicion")
                    if condicion == "Algún objeto obstaculiza la visión":
                        resultado("Traza una línea de inspección como Sin suficiente información y asigna en Workforce.")
                    else:
                        resultado("Traza una línea de inspección. Realizar procedimiento Experience Builder → PowerApp → SharePoint → Workforce para líneas de inspección.")
        else:
            tarjeta("REVISIÓN DEL HISTÓRICO", "Verifica el histórico y descarta la presencia de huellas en el pavimento y/o banqueta.")
            resultado("Traza una línea de inspección y realiza el procedimiento para zonas barridas si no encontraste indicios de acometidas ocultas o acometidas visibles no levantadas en GIS.")

if st.button("Reiniciar guía"):
    st.rerun()
