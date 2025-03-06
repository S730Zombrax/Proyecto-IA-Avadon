import streamlit as st
from neural_chatbot import NeuralChatbot
import plotly.express as px
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Chatbot de Compatibilidad Sanguínea",
    page_icon="🩸",
    layout="wide"
)

# Inicializar estados de la sesión
if 'chatbot' not in st.session_state:
    with st.spinner('Iniciando el asistente con IA...'):
        try:
            st.session_state.chatbot = NeuralChatbot()
        except Exception as e:
            st.error(f"Error al inicializar el chatbot: {str(e)}")
            st.session_state.chatbot = None

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = {}
if 'current_message' not in st.session_state:
    st.session_state.current_message = ""

try:
    # Agregar CSS personalizado para que el div ocupe todo el ancho
    st.markdown("""
        <style>
            .full-width-div {
                position: relative;
                width: 100vw;
                left: 50%;
                transform: translateX(-50%);
                background-color: #e02424;
                height: 10px;
            }
            .blood-type-button {
                display: inline-block;
                padding: 10px 20px;
                margin: 5px;
                border-radius: 5px;
                border: 1px solid #e02424;
                cursor: pointer;
                text-align: center;
            }
            .blood-type-button:hover {
                background-color: #e02424;
                color: white;
            }
            .compatibility-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            .compatibility-table th, .compatibility-table td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            .compatibility-table th {
                background-color: #f8f9fa;
            }
        </style>
    """, unsafe_allow_html=True)

    # Logo y título
    st.image("assets/logo.svg", width=100)
    st.title("Chatbot de Compatibilidad Sanguínea")

    # Dividir la pantalla en dos columnas
    col1, col2 = st.columns([3, 2])

    with col1:
        # Chat container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for idx, message in enumerate(st.session_state.messages):
            if message['role'] == 'user':
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                message_id = message.get('id', f"msg_{idx}")
                st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)

                if message_id not in st.session_state.feedback:
                    st.markdown('<div class="feedback-container">', unsafe_allow_html=True)
                    fcol1, fcol2, _ = st.columns([1, 1, 10])
                    with fcol1:
                        if st.button("👍", key=f"pos_{message_id}", help="Me gustó esta respuesta"):
                            st.session_state.feedback[message_id] = 'positive'
                            st.rerun()
                    with fcol2:
                        if st.button("👎", key=f"neg_{message_id}", help="No me gustó esta respuesta"):
                            st.session_state.feedback[message_id] = 'negative'
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    feedback = st.session_state.feedback[message_id]
                    st.markdown(
                        f'<div class="feedback-received">{"👍 ¡Gracias por tu feedback!" if feedback == "positive" else "👎 Gracias por tu feedback"}</div>',
                        unsafe_allow_html=True
                    )
        st.markdown('</div>', unsafe_allow_html=True)

        # Input section
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        chat_input = st.text_input('Pregunta sobre compatibilidad sanguínea...', key='chat_input')
        if st.button('Enviar', key='send_button'):
            if chat_input.strip():
                try:
                    st.session_state.messages.append({"role": "user", "content": chat_input})
                    if st.session_state.chatbot:
                        response = st.session_state.chatbot.get_response(chat_input)
                        message_id = f"msg_{len(st.session_state.messages)}"
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response,
                            "id": message_id
                        })
                    else:
                        st.error("El chatbot no está inicializado correctamente.")
                    st.session_state.current_message = ""
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al procesar la pregunta: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Selección de tipo de sangre
        st.subheader("Seleccionar Tipo de Sangre")
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        cols = st.columns(4)
        for i, blood_type in enumerate(blood_types):
            with cols[i % 4]:
                st.button(blood_type, key=f"blood_type_{blood_type}")

        # Tabla de compatibilidad
        st.subheader("Tabla de Compatibilidad")
        compatibility_data = {
            'BLOOD TYPE': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
            'CAN DONATE TO': [
                'A+, AB+',
                'A+, A-, AB+, AB-',
                'B+, AB+',
                'B+, B-, AB+, AB-',
                'AB+',
                'AB+, AB-',
                'O+, A+, B+, AB+',
                'All blood types'
            ]
        }
        compatibility_df = pd.DataFrame(compatibility_data)
        st.table(compatibility_df)

    # Original Data Visualization - integrated into a new expander
    with st.expander("📊 Visualización de Datos"):
        # Datos de ejemplo para los gráficos
        blood_types_data = {
            'Tipo': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
            'Porcentaje': [34, 6, 9, 2, 3, 1, 38, 7]
        }
        df = pd.DataFrame(blood_types_data)

        # Gráfico de distribución de tipos de sangre
        fig_pie = px.pie(df, values='Porcentaje', names='Tipo',
                        title='Distribución de Tipos de Sangre en la Población',
                        color_discrete_sequence=px.colors.qualitative.Set3)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            title_x=0.5,
            title_font_size=20,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # Compatibilidad de donantes
        compatibility_data = {
            'Receptor': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
            'Donantes_Compatibles': [2, 1, 2, 1, 4, 2, 1, 1]
        }
        df_comp = pd.DataFrame(compatibility_data)

        fig_bar = px.bar(df_comp, x='Receptor', y='Donantes_Compatibles',
                         title='Número de Tipos de Sangre Compatibles por Receptor',
                         color='Receptor',
                         color_discrete_sequence=px.colors.qualitative.Set3)
        fig_bar.update_layout(
            title_x=0.5,
            title_font_size=20,
            xaxis_title="Tipo de Sangre Receptor",
            yaxis_title="Número de Donantes Compatibles",
            showlegend=False,
            bargap=0.2
        )
        st.plotly_chart(fig_bar, use_container_width=True)


    # Original Information Section
    with st.expander("ℹ️ Información sobre tipos de sangre"):
        st.markdown("""
        ### Tipos de sangre
        - **Grupo A**: A+ y A-
        - **Grupo B**: B+ y B-
        - **Grupo AB**: AB+ y AB-
        - **Grupo O**: O+ y O-

        ### Datos importantes
        - O- es el donante universal
        - AB+ es el receptor universal
        - Los tipos negativos pueden donar a sus correspondientes positivos
        - El factor Rh negativo solo puede recibir de tipos negativos
        """)

except Exception as e:
    st.error(f"Error en la aplicación: {str(e)}")