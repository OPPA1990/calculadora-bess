import streamlit as st

def formatear_moneda(valor):
    """Formatea el número como moneda en MXN usando comas como separador de miles."""
    return f"{valor:,.2f} MXN"

def calcular_ahorro(gasto_mensual, tarifa):
    """Calcula el ahorro mensual y anual en base al gasto mensual y la tarifa seleccionada."""
    factores = {
        "GDMTH": 0.28,  # Ahorros por peak shaving y reducción de demanda
        "DIT": 0.22,    # Ahorros por arbitraje energético y respaldo
        "DIST": 0.15    # Menor variabilidad en picos, pero aún con potencial
    }
    factor = factores.get(tarifa, 0.15)
    ahorro_mensual = gasto_mensual * factor
    ahorro_anual = ahorro_mensual * 12
    return ahorro_mensual, ahorro_anual

st.set_page_config(page_title="Calculadora BESS", page_icon="⚡", layout="centered", initial_sidebar_state="collapsed")

# CSS personalizado
st.markdown(
    """
    <style>
    /* Fondo y color de texto global */
    [data-testid="stAppViewContainer"] {
        background-color: #000000;
        color: #FFFFFF;
        padding-top: 2rem;
    }
    
    /* Encabezados en color azul de la marca */
    h1, h2, h3, h4, h5, h6 {
        color: #27a8e0;
    }
    
    /* Ocultar la barra de herramientas de Streamlit y el footer */
    [data-testid="stToolbar"] {
        visibility: hidden;
    }
    footer { 
        visibility: hidden;
    }
    
    /* Estilo para contenedores tipo tarjeta (resultados) */
    .card {
        background-color: #FFFFFF;
        color: #000000;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    }
    
    /* Contenedor del formulario */
    .form-container {
        background-color: #111111;
        border-radius: 10px;
        padding: 2em;
        max-width: 600px;
        margin: auto;
        box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.1);
    }
    
    /* Estilos para los inputs y selects dentro del formulario */
    .form-container input,
    .form-container select {
        width: 100%;
        background-color: #222222;
        color: #FFFFFF;
        border: none;
        border-radius: 5px;
        padding: 0.75em;
        margin-bottom: 1em;
        font-size: 1em;
    }
    
    .form-container input::placeholder,
    .form-container select::placeholder {
        color: #aaaaaa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título y descripción inicial
st.title("🔋 Calculadora de Ahorro Energético BESS")
st.write("Descubre cuánto puedes **ahorrar anualmente** al integrar sistemas de almacenamiento de energía en tu empresa.")

# Formulario interactivo
with st.form("formulario_calculadora"):
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    
    nombre = st.text_input("Nombre completo", placeholder="Ingresa tu nombre completo")
    email = st.text_input("Correo corporativo", placeholder="Ingresa tu correo corporativo")
    telefono = st.text_input("Teléfono (10 dígitos)", placeholder="Ej. 5512345678")
    empresa = st.text_input("Empresa", placeholder="Nombre de la empresa")
    
    gasto_mensual_raw = st.number_input("Gasto mensual en electricidad (MXN)", min_value=100000, max_value=10000000, step=10000)
    gasto_mensual = gasto_mensual_raw  # Valor numérico para cálculo
    st.caption(f"**Valor ingresado:** {gasto_mensual:,.0f} MXN")
    
    estado = st.selectbox("Estado", [
        "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua", "Ciudad de México",
        "Coahuila", "Colima", "Durango", "Estado de México", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Michoacán",
        "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa",
        "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
    ])
    
    tarifa = st.selectbox("Tarifa eléctrica", ["GDMTH", "DIT", "DIST"])
    
    submit = st.form_submit_button("Calcular ahorro")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Procesar y mostrar resultados
if submit:
    if not telefono.isdigit() or len(telefono) != 10:
        st.error("⚠️ El número de teléfono debe contener exactamente 10 dígitos numéricos.")
    else:
        ahorro_mensual, ahorro_anual = calcular_ahorro(gasto_mensual, tarifa)
        ahorro_mensual_fmt = formatear_moneda(ahorro_mensual)
        ahorro_anual_fmt = formatear_moneda(ahorro_anual)
        
        html_results = f"""
        <div class='card'>
            <h2>📊 Resultados del cálculo</h2>
            <p><strong>Ahorro mensual estimado:</strong> {ahorro_mensual_fmt}</p>
            <p><strong>Ahorro anual estimado:</strong> {ahorro_anual_fmt}</p>
            <h3>📝 Datos del contacto</h3>
            <p><strong>Nombre:</strong> {nombre}</p>
            <p><strong>Correo:</strong> {email}</p>
            <p><strong>Teléfono:</strong> {telefono}</p>
            <p><strong>Empresa:</strong> {empresa}</p>
            <p><strong>Estado:</strong> {estado}</p>
            <p><strong>Tarifa:</strong> {tarifa}</p>
        </div>
        """
        st.markdown(html_results, unsafe_allow_html=True)