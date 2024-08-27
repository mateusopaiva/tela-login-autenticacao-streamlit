import streamlit as st
import streamlit_authenticator as stauth
from dependencies import consulta, consulta_geral, add_registro, cria_tabela

def main():
  try:
    consulta_geral()
  except:
    cria_tabela()

  db_query = consulta_geral()

  registros = {'usernames': {}}
  for data in db_query:
    registros['usernames'][data[1]] = {'name': data[0], 'password': data[2]}

  COOKIE_EXPIRY_DAYS = 30
  authenticator = stauth.Authenticate(
      registros,
     'random_cookie_name',
     'random_signature_key',
     COOKIE_EXPIRY_DAYS,
  )

  if 'clicou_registrar' not in st.session_state:
    st.session_state['clicou_registrar'] = False
  
  if st.session_state['clicou_registrar'] == False:
    login_form(authenticator=authenticator)
  else:
    usuario_form()

def login_form(authenticator):
  name, authentication_status, username = authenticator.login('Login')
  if authentication_status:
    authenticator.logout('Logout', 'main')
    st.title('Área do Dashboard')
    st.write(f'*{name} está logado!')
  elif authentication_status == False:
    st.error('Usúario ou senha incorretos.')
  elif authentication_status == None:
    st.warning('Insira um nome de usuário e uma senha')
    clicou_em_registrar = st.button("Registrar")
    if clicou_em_registrar:
      st.session_state['clicou_registrar'] = True
      st.rerun()

def confirm_message():
  hashed_password = stauth.Hasher([st.session_state.password]).generate()
  if st.session_state.password != st.session_state.confirm_password:
    st.warning('Senhas não conferem')
  elif consulta(st.session_state.user):
    st.warning('Nome de usúario já existe.')
  else:
    add_registro(st.session_state.nome, st.session_state.user, hashed_password[0])
    st.success('Registro efetuado!')

def usuario_form():
  with st.form(key="formulario", clear_on_submit=True):
    nome = st.text_input("Nome", key="nome")
    username = st.text_input("Usúario", key="user")
    password = st.text_input("Senha", key="password", type="password")
    confirm_password = st.text_input("Confirme a senha", key="confirm_password", type="password")
    submit = st.form_submit_button("Salvar", on_click=confirm_message)
  clicou_em_fazer_login = st.button("Fazer Login")
  if clicou_em_fazer_login:
    st.session_state['clicou_registrar'] = False
    st.rerun()

if __name__ == '__main__':
  main()