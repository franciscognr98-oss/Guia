
import streamlit as st
import html

st.set_page_config(
    page_title="Guía",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #102A43;
    --blue: #246BCE;
    --blue-dark: #174F9C;
    --pale: #EAF3FC;
    --line: #D7E2EE;
    --muted: #61758A;
}

html, body, [data-testid="stAppViewContainer"] {
    background: #F3F6FA;
    color: var(--navy);
    font-family: Inter, sans-serif;
}

[data-testid="stHeader"] {
    background: #F3F6FA;
}

.block-container {
    max-width: 1120px;
    padding: 2rem 2rem 4rem;
}

h1, h2, h3, p, label {
    color: var(--navy);
}

h1 {
    font-size: 2rem;
    font-weight: 800;
}

.panel {
    background: white;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 22px 26px;
    margin: 18px 0;
    box-shadow: 0 3px 12px rgba(16,42,67,.035);
}

.eyebrow {
    font-size: .76rem;
    font-weight: 800;
    letter-spacing: .09em;
    color: var(--blue);
    margin-bottom: 8px;
}

.instruction {
    font-size: 1rem;
    line-height: 1.65;
    color: #243B53;
}

.result {
    background: #E8F1FB;
    border: 1px solid #B8D0EA;
    border-left: 5px solid var(--blue);
    border-radius: 12px;
    padding: 18px 22px;
    margin: 18px 0;
    color: var(--navy);
    font-size: 1rem;
    line-height: 1.6;
}

.result .tag {
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .1em;
    color: var(--blue);
    margin-bottom: 5px;
}

.result p {
    margin: 0;
    color: var(--navy);
    font-weight: 600;
}

div[data-testid="stRadio"] > label {
    font-weight: 700;
    color: var(--navy);
    font-size: 1rem;
    margin-bottom: 10px;
}

div[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 10px;
    flex-wrap: wrap;
}

div[data-testid="stRadio"] div[role="radiogroup"] label {
    background: white;
    border: 1.5px solid #C9D7E6;
    border-radius: 11px;
    padding: 11px 18px;
    margin: 0;
    min-height: 46px;
    cursor: pointer;
}

div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
    border-color: var(--blue);
    background: #F0F6FD;
}

div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
    background: #E7F0FB;
    border: 2px solid var(--blue);
    color: #123B66;
    font-weight: 700;
}

div[data-testid="stRadio"] div[role="radiogroup"] label p {
    color: inherit;
    margin: 0;
}

div[data-testid="stRadio"] div[role="radiogroup"] label > div:first-child {
    display: none;
}

div[data-testid="stRadio"] input {
    display: none;
}

hr {
    border-color: var(--line);
}
</style>
""", unsafe_allow_html=True)


def preguntar(texto, opciones, clave):
    return st.radio(
        texto,
        opciones,
        key=clave,
        horizontal=True
    )


def panel(titulo, texto=None):
    contenido = (
        f'<div class="instruction">{html.escape(texto)}</div>'
        if texto else ""
    )

    st.markdown(
        f"""
        <div class="panel">
            <div class="eyebrow">{html.escape(titulo)}</div>
            {contenido}
        </div>
        """,
        unsafe_allow_html=True
    )


def resultado(texto):
    st.markdown(
        f"""
        <div class="result">
            <div class="tag">RESULTADO</div>
            <p>{html.escape(texto)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# INICIO

st.title("Guía")

procedimiento = preguntar(
    "¿Qué procedimiento realizas?",
    ["A) VALIDACIÓN", "B) BARRIDO"],
    "procedimiento"
)


# A) VALIDACIÓN

if procedimiento == "A) VALIDACIÓN":

    tipo = preguntar(
        "Selecciona el tipo de validación",
        [
            "A.1) VALIDACIÓN DE RED",
            "A.2) VALIDACIÓN DE COMERCIOS"
        ],
        "tipo_validacion"
    )

    # A.1 VALIDACIÓN DE RED

    if tipo == "A.1) VALIDACIÓN DE RED":

        panel(
            "A.1) VALIDACIÓN DE RED",
            "Recorre la red en Google Maps y compara con Experience Builder. "
            "Revisa el histórico de StreetView."
        )

        streetview = preguntar(
            "¿Hay StreetView?",
            ["Sí", "No"],
            "red_streetview"
        )

        if streetview == "No":

            tipo_elemento = preguntar(
                "Selecciona el elemento",
                [
                    "Zona sin StreetView",
                    "Calle sin StreetView"
                ],
                "red_elemento_sinstreetview"
            )

            if tipo_elemento == "Zona sin StreetView":
                resultado(
                    "Realizar procedimiento para polígonos sin StreetView."
                )
            else:
                resultado(
                    "Realizar procedimiento para líneas sin StreetView."
                )

        else:

            patron = preguntar(
                "¿Observas algún patrón sobre la red?",
                ["Sí", "No"],
                "red_patron"
            )

            if patron == "No":

                panel(
                    "REVISIÓN DEL HISTÓRICO",
                    "Verifica el histórico, descarta la presencia de huellas "
                    "en el pavimento y/o banqueta."
                )

                resultado(
                    "Descarta la red si no encontraste indicios de "
                    "acometidas ocultas o acometidas visibles no levantadas en GIS."
                )

            else:

                todas = preguntar(
                    "¿Todas las acometidas que corresponden al patrón "
                    "aparecen en Experience Builder?",
                    ["Sí", "No"],
                    "red_todas"
                )

                if todas == "Sí":

                    resultado("Se descarta.")

                else:

                    visible = preguntar(
                        "¿La acometida faltante es visible?",
                        ["Sí", "No"],
                        "red_visible"
                    )

                    if visible == "Sí":

                        resultado("Pasa a OYM.")

                    else:

                        condicion = preguntar(
                            "¿Qué condición se presenta?",
                            [
                                "Algún objeto obstaculiza la visión",
                                "Hay construcción"
                            ],
                            "red_condicion"
                        )

                        if condicion == "Algún objeto obstaculiza la visión":

                            resultado(
                                "Sin suficiente información y asigna en Workforce."
                            )

                        else:

                            resultado(
                                "Realizar procedimiento Experience Builder "
                                "→ PowerApp → SharePoint → Workforce "
                                "para redes sin acometidas."
                            )


    # A.2 VALIDACIÓN DE COMERCIOS

    else:

        panel(
            "A.2) VALIDACIÓN DE COMERCIOS",
            "Busca el comercio en Google Maps. "
            "Revisa el histórico de StreetView."
        )

        streetview = preguntar(
            "¿Hay StreetView?",
            ["Sí", "No"],
            "comercio_streetview"
        )

        if streetview == "No":

            panel(
                "REVISIÓN DEL HISTÓRICO",
                "Verifica el histórico, descarta la presencia de huellas "
                "en el pavimento y/o banqueta."
            )

            resultado(
                "Descarta el comercio si no encontraste indicios de "
                "acometida oculta o acometida visible no levantada en GIS."
            )

        else:

            acometida = preguntar(
                "¿Hay acometida?",
                ["Sí", "No"],
                "comercio_acometida"
            )

            if acometida == "No":

                panel(
                    "REVISIÓN DEL HISTÓRICO",
                    "Verifica el histórico, descarta la presencia de huellas "
                    "en el pavimento y/o banqueta."
                )

                resultado(
                    "Descarta el comercio si no encontraste indicios de "
                    "acometida oculta o acometida visible no levantada en GIS."
                )

            else:

                gis = preguntar(
                    "¿Está levantada en GIS?",
                    ["Sí", "No"],
                    "comercio_gis"
                )

                if gis == "Sí":

                    resultado("Se descarta.")

                else:

                    visible = preguntar(
                        "¿Es visible?",
                        ["Sí", "No"],
                        "comercio_visible"
                    )

                    if visible == "Sí":

                        resultado(
                            "Pasa a OYM (Adjunta evidencia)."
                        )

                    else:

                        condicion = preguntar(
                            "¿Qué condición se presenta?",
                            [
                                "Algún objeto obstaculiza la visión",
                                "Hay construcción"
                            ],
                            "comercio_condicion"
                        )

                        if condicion == "Algún objeto obstaculiza la visión":

                            resultado(
                                "Sin suficiente información "
                                "(Adjunta evidencia y asigna en Workforce)."
                            )

                        else:

                            resultado(
                                "Se confirma. Realizar procedimiento "
                                "Experience Builder → PowerApp → SharePoint "
                                "→ Workforce para comercios."
                            )


# B) BARRIDO

else:

    panel(
        "B) BARRIDO",
        "Recorre las calles, únicamente las que tienen red de ENGIE. "
        "Identifica zonas sin StreetView. Compara lo que observas en "
        "StreetView de Google Maps con lo que se encuentra en Experience Builder. "
        "Identifica patrones en la ubicación de las acometidas y revisa "
        "cuidadosamente el histórico de StreetView. Revisa el pavimento "
        "para identificar huellas por instalación."
    )

    streetview = preguntar(
        "¿La zona que recorriste tiene StreetView?",
        ["Sí", "No"],
        "barrido_streetview"
    )

    if streetview == "No":

        tipo_elemento = preguntar(
            "Selecciona el elemento",
            [
                "Zona sin StreetView",
                "Calle sin StreetView"
            ],
            "barrido_elemento_sinstreetview"
        )

        if tipo_elemento == "Zona sin StreetView":

            resultado(
                "Realizar procedimiento para polígonos sin StreetView."
            )

        else:

            resultado(
                "Realizar procedimiento para líneas sin StreetView."
            )

    else:

        patron = preguntar(
            "¿Observaste algún patrón?",
            ["Sí", "No"],
            "barrido_patron"
        )

        if patron == "No":

            panel(
                "REVISIÓN DEL HISTÓRICO",
                "Verifica el histórico, descarta la presencia de huellas "
                "en el pavimento y/o banqueta."
            )

            resultado(
                "Traza una línea de inspección y realiza el procedimiento "
                "para zonas barridas si no encontraste indicios de acometidas "
                "ocultas o acometidas visibles no levantadas en GIS."
            )

        else:

            todas = preguntar(
                "¿Todas las acometidas que corresponden al patrón "
                "aparecen en Experience Builder?",
                ["Sí", "No"],
                "barrido_todas"
            )

            if todas == "Sí":

                resultado(
                    "Traza una línea de inspección "
                    "(Procedimiento para reporte de zonas barridas)."
                )

            else:

                visible = preguntar(
                    "¿La acometida faltante es visible?",
                    ["Sí", "No"],
                    "barrido_visible"
                )

                if visible == "Sí":

                    resultado(
                        "Traza línea de inspección para pasar a OYM."
                    )

                else:

                    condicion = preguntar(
                        "¿Qué condición se presenta?",
                        [
                            "Algún objeto obstaculiza la visión",
                            "Hay construcción"
                        ],
                        "barrido_condicion"
                    )

                    if condicion == "Algún objeto obstaculiza la visión":

                        resultado(
                            "Traza línea de inspección como Sin suficiente "
                            "información y asigna en Workforce."
                        )

                    else:

                        resultado(
                            "Traza línea de inspección. Realizar procedimiento "
                            "Experience Builder → PowerApp → SharePoint "
                            "→ Workforce para líneas de inspección."
                        )
