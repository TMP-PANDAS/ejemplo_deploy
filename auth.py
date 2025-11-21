import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Cargar configuración de usuarios
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Crear objeto autenticador
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Widget de login
authenticator.login(location='main')

if st.session_state.get('authentication_status'):
    authenticator.logout(location='main')
    st.write(f'Bienvenido *{st.session_state["name"]}*')
    
    # Aquí va tu dashboard
    st.title('Mi Dashboard Protegido')
    st.write('Contenido solo para usuarios autenticados')
    
elif st.session_state.get('authentication_status') == False:
    st.error('Usuario/contraseña incorrectos')
elif st.session_state.get('authentication_status') is None:
    st.warning('Por favor ingresa tu usuario y contraseña')
