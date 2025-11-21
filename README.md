## 1. **Solución Simple con `streamlit-authenticator`** 

```python
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
   
```

**Archivo `config.yaml`:**

```yaml
credentials:
  usernames:
    beto:
      email: beto@gmail.com
      name: Alberto Aguilar
      password: $2b$12$mQQ/c78QQHlpgLlww7lL9.LDgcuXwx1QGAjayuLkpNuIC2ZWVnLRC
    james:
      email: james@gmail.com
      name: James Hetfield
      password: $2b$12$hashed_password_here

cookie:
  name: dashboard_cookie
  key: random_signature_key  # Cambia esto por una clave segura
  expiry_days: 30
```

**Generar contraseñas hasheadas:**

```python
import streamlit_authenticator as stauth

passwords = ['1234', 'password456']
hashed_passwords = [stauth.utilities.hasher.Hasher.hash(password) for password in passwords]
print(hashed_passwords)
```

Instala con: `pip install streamlit-authenticator`

## 2. **Solución Básica Manual** (Sin dependencias)

```python
import streamlit as st
import hashlib

# Función para verificar credenciales
def check_password():
    # Retorna True si el usuario ingresó la contraseña correcta
    
    def password_entered():
        # Verifica la contraseña ingresada
        usuarios = {
            "admin": hashlib.sha256("admin123".encode()).hexdigest(),
            "usuario1": hashlib.sha256("pass123".encode()).hexdigest()
        }
        
        if st.session_state["username"] in usuarios:
            if hashlib.sha256(st.session_state["password"].encode()).hexdigest() == usuarios[st.session_state["username"]]:
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # No guardar password
                return
        
        st.session_state["password_correct"] = False

    # Primera ejecución, mostrar inputs
    if "password_correct" not in st.session_state:
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password", on_change=password_entered)
        return False
    
    # Password incorrecta
    elif not st.session_state["password_correct"]:
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password", on_change=password_entered)
        st.error("Usuario o contraseña incorrectos")
        return False
    
    # Password correcta
    else:
        return True

# Verificar autenticación
if check_password():
    st.title("Dashboard Protegido")
    st.write(f"Bienvenido, {st.session_state.get('username', 'Usuario')}!")
    
    # Tu dashboard aquí
    st.metric("Métrica 1", "100")
    
    # Botón de logout
    if st.button("Cerrar sesión"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

```

## 3. **Con Base de Datos (PostgreSQL/SQLite/MySQL)**

Para aplicaciones más robustas, se puede usar una base de datos:

```python
import streamlit as st
import sqlite3
import hashlib

def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
    result = c.fetchone()
    conn.close()
    return result is not None
```
