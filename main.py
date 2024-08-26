import streamlit as st
import streamlit_authenticator as stauth

COOKIE_EXPIRY_DAYS = 30

def main():
  authenticator = stauth.Authenticate(
    {'usernames': {'test': {'name': 'testando', 'password': 'blabla'}}},
     'random_cookie_name',
     'random_signature_key',

     COOKIE_EXPIRY_DAYS,
  )

  if 'clicou_registrar' not in st.session_state:
    st.session_state['clicou_registrar'] = False
  
  if st.session_state['clicou_registrar'] == False:
    login_form(authenticator=authenticator)

def login_form(authenticator):
  name, authentication_status, username = authenticator.login('Login')
  if authentication_status:
    authenticator.logout('Logout', main)
    st.title('Área do Dashboard')
    st.write(f'*{name} está logado!')
  elif authentication_status == False:
    st.error('Usúario/Senha incorretos.')
  elif authentication_status == None:
    st.error('Por favor informe um usúario e senha')
    clicou_em_registrar = st.button("Registrar")
    if clicou_em_registrar:
      st.session_state['clicou_registrar'] = True
      st.rerun()

def confirm_message():
  hashed_password = stauth.Hasher([st.session_state.password]).generate()
  if st.session_state.password != st.session_state.confirm_password:
    st.warning('Senhas não conferem')
  elif 'consulta_nome()':
    st.warning('Nome de usúario já existe.')
  else:
    'add_registro()'
    st.success('Registro efetuado!')

def usuario_form():
  with st.form(key="formulario", clear_on_submit=True):
    nome = st.text_input("Nome", key="nome")
    username = st.text_input("Usúario", key="user")
    password = st.text_input("Senha", key="password", type="password")
    confirm_password = st.text_input("Confirme a senha", key="confirm_password", type="confirm_password")
    submit = st.form_submit_button("Salvar", on_click=confirm_message)
    clicou_em_fazer_login = st.button("Fazer Login")
    if clicou_em_fazer_login:
      st.session_state['clicou_registrar'] = False
      st.rerun()

if __name__ == '__main__':
  main()