import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

file_name = 'clientescamera.csv'
alarm_file_name = 'alarmes.csv'

# Carregar ou criar o CSV de clientes
def load_or_create_csv(file_name):
    try:
        data = pd.read_csv(file_name, parse_dates=['DATA LIMITE', 'DATA ENTREGA'])
    except FileNotFoundError:
        data = pd.DataFrame(columns=[
            'CLIENTES', 'ESTADO (UF)', 'TIPO DE SERVIÇO', 'DATA LIMITE',
            'DATA ENTREGA', 'EDITOR RESPONSÁVEL', 'OBSERVAÇÃO', 'DRONE PARCEIRO', 'DRIVE'
        ])
        data.to_csv(file_name, index=False)
    return data

# Salvar dados no CSV de clientes
def save_to_csv(data, file_name):
    data.to_csv(file_name, index=False)

# Carregar ou criar o CSV de alarmes
def load_or_create_alarm_csv(file_name):
    try:
        alarm_data = pd.read_csv(file_name, parse_dates=['DATA'])
    except FileNotFoundError:
        alarm_data = pd.DataFrame(columns=['DATA', 'MENSAGEM', 'CLIENTE', 'TIPO DE SERVIÇO', 'EDITOR', 'FREQUÊNCIA'])
        alarm_data.to_csv(file_name, index=False)
    return alarm_data

# Salvar dados no CSV de alarmes
def save_alarm_to_csv(data, file_name):
    data.to_csv(file_name, index=False)

# Inicializar o arquivo de alarmes se não existir
def initialize_alarm_file(file_name):
    try:
        pd.read_csv(file_name)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['DATA', 'MENSAGEM', 'CLIENTE', 'TIPO DE SERVIÇO', 'EDITOR', 'FREQUÊNCIA'])
        df.to_csv(file_name, index=False)

# Função para cadastrar um novo cliente
def cadastrar_cliente():
    with st.form(key='cliente_form'):
        cliente = st.text_input('CLIENTES')
        estado = st.text_input('ESTADO (UF)')
        tipo_servico = st.text_input('TIPO DE SERVIÇO')
        data_limite = st.date_input('DATA LIMITE')
        data_entrega = st.date_input('DATA ENTREGA')
        editor_responsavel = st.text_input('EDITOR RESPONSÁVEL')
        observacao = st.text_input('OBSERVAÇÃO')
        drone_parceiro = st.text_input('DRONE PARCEIRO')
        drive = st.text_input('DRIVE')
        submit_button = st.form_submit_button(label='Cadastrar')

        if submit_button:
            novo_cliente = {
                'CLIENTES': cliente,
                'ESTADO (UF)': estado,
                'TIPO DE SERVIÇO': tipo_servico,
                'DATA LIMITE': pd.to_datetime(data_limite),
                'DATA ENTREGA': pd.to_datetime(data_entrega),
                'EDITOR RESPONSÁVEL': editor_responsavel,
                'OBSERVAÇÃO': observacao,
                'DRONE PARCEIRO': drone_parceiro,
                'DRIVE': drive
            }
            st.session_state['clientes_data'] = pd.concat([st.session_state['clientes_data'], pd.DataFrame([novo_cliente])], ignore_index=True)
            save_to_csv(st.session_state['clientes_data'], file_name)
            st.session_state['last_data_limite'] = data_limite
            st.session_state['last_data_entrega'] = data_entrega
            st.session_state['last_cliente'] = cliente
            st.session_state['last_tipo_servico'] = tipo_servico
            st.session_state['last_editor_responsavel'] = editor_responsavel
            st.success('Cliente cadastrado com sucesso!')

# Função para definir alarmes
def definir_alarme():
    if 'last_data_limite' in st.session_state and 'last_data_entrega' in st.session_state:
        with st.form(key='alarme_form'):
            st.write("Defina os alertas para as datas")

            # Data Limite
            alarme_data_limite = st.date_input('Data do Alarme para DATA LIMITE', value=st.session_state['last_data_limite'])
            alarme_msg_limite = st.text_input('Mensagem do Alarme para DATA LIMITE')
            frequencia_limite = st.selectbox('Frequência do Alarme para DATA LIMITE', ['Diário', 'Semanal', 'Mensal', 'Avulso'])

            # Data Entrega
            alarme_data_entrega = st.date_input('Data do Alarme para DATA ENTREGA', value=st.session_state['last_data_entrega'])
            alarme_msg_entrega = st.text_input('Mensagem do Alarme para DATA ENTREGA')
            frequencia_entrega = st.selectbox('Frequência do Alarme para DATA ENTREGA', ['Diário', 'Semanal', 'Mensal', 'Avulso'])

            submit_button = st.form_submit_button(label='Definir Alarmes')

            if submit_button:
                # Função para adicionar alarmes recorrentes
                def adicionar_alarme(data_inicial, mensagem, frequencia, cliente, tipo_servico, editor):
                    data_alarme = pd.to_datetime(data_inicial)
                    while data_alarme <= datetime.now() + pd.DateOffset(months=12):  # Limite de um mês para criar alarmes
                        st.session_state['alarmes'].append({
                            'DATA': data_alarme,
                            'MENSAGEM': mensagem,
                            'CLIENTE': cliente,
                            'TIPO DE SERVIÇO': tipo_servico,
                            'EDITOR': editor,
                            'FREQUÊNCIA': frequencia
                        })
                        if frequencia == 'Diário':
                            data_alarme += timedelta(days=1)
                        elif frequencia == 'Semanal':
                            data_alarme += timedelta(weeks=1)
                        elif frequencia == 'Mensal':
                            data_alarme += pd.DateOffset(months=1)
                        else:  # Avulso
                            break

                # Adicionar alarmes para Data Limite
                if alarme_data_limite and alarme_msg_limite:
                    adicionar_alarme(alarme_data_limite, alarme_msg_limite, frequencia_limite, st.session_state['last_cliente'], st.session_state['last_tipo_servico'], st.session_state['last_editor_responsavel'])

                # Adicionar alarmes para Data Entrega
                if alarme_data_entrega and alarme_msg_entrega:
                    adicionar_alarme(alarme_data_entrega, alarme_msg_entrega, frequencia_entrega, st.session_state['last_cliente'], st.session_state['last_tipo_servico'], st.session_state['last_editor_responsavel'])

                st.success('Alarmes ajustados com sucesso!')
                del st.session_state['last_data_limite']
                del st.session_state['last_data_entrega']
                del st.session_state['last_cliente']
                del st.session_state['last_tipo_servico']
                del st.session_state['last_editor_responsavel']
                save_alarm_to_csv(pd.DataFrame(st.session_state['alarmes']), alarm_file_name)

# Função para visualizar dados e alarmes
def visualizar_dados():
    st.subheader('Base de Dados de Clientes')
    st.dataframe(st.session_state['clientes_data'])

    st.subheader('Alarmes')
    alarmes_df = pd.DataFrame(st.session_state['alarmes'])
    if not alarmes_df.empty:
        st.dataframe(alarmes_df)
    else:
        st.write('Nenhum alarme ajustado.')

    st.subheader('Calendário de Alarmes Interativo')
    if not alarmes_df.empty:
        alarmes_df['DATA'] = pd.to_datetime(alarmes_df['DATA'])
        alarmes_df['Dias até o Alarme'] = (alarmes_df['DATA'] - pd.Timestamp.now()).dt.days
        alarmes_df_filtrados = alarmes_df[alarmes_df['Dias até o Alarme'] <= 30]  # Filtrar para os próximos 30 dias
        eventos = alarmes_df_filtrados.groupby(['DATA', 'CLIENTE', 'TIPO DE SERVIÇO', 'MENSAGEM']).size().reset_index(
            name='count')

        fig = px.treemap(eventos, path=['DATA', 'CLIENTE', 'TIPO DE SERVIÇO', 'MENSAGEM'], values='count',
                         title='Treemap de Alarmes',
                         labels={"DATA": "Data", "count": "Número de Ocorrências",
                                 "MENSAGEM": "Descrição do Alarme",
                                 "CLIENTE": "Nome do Cliente", "TIPO DE SERVIÇO": "Tipo de Serviço"})

        # Exibindo o treemap sempre
        st.plotly_chart(fig, use_container_width=True)

        mostrar_coluna_interativa = st.checkbox("Mostrar Coluna Interativa")
        if mostrar_coluna_interativa:
            # Adicionando uma coluna interativa para marcar se o serviço foi entregue
            eventos['Entregue'] = eventos.apply(
                lambda row: st.checkbox(f"{row['DATA']} - {row['CLIENTE']}: {row['MENSAGEM']}", key=row.name),
                axis=1)

            # Adicionando um botão para aplicar as marcações realizadas
            aplicar_marcações = st.button("Aplicar Marcações")

            if aplicar_marcações:
                # Exibindo a mensagem "Tarefa entregue!"
                st.success("Tarefa entregue!")

                # Ordenando a coluna interativa
                eventos = eventos.sort_values(by=['DATA', 'CLIENTE', 'TIPO DE SERVIÇO', 'MENSAGEM'])

                # Excluindo alarmes marcados como entregues
                for idx, row in eventos.iterrows():
                    if row['Entregue']:
                        alarmes_df = alarmes_df[~((alarmes_df['DATA'] == row['DATA']) &
                                                  (alarmes_df['CLIENTE'] == row['CLIENTE']) &
                                                  (alarmes_df['TIPO DE SERVIÇO'] == row['TIPO DE SERVIÇO']) &
                                                  (alarmes_df['MENSAGEM'] == row['MENSAGEM']))]

                # Salvando as alterações no arquivo CSV de alarmes
                save_alarm_to_csv(alarmes_df, alarm_file_name)

                # Atualizando a página para que o usuário veja as modificações
                st.experimental_rerun()
        else:
            st.write('A coluna interativa está oculta. Marque a caixa de seleção acima para mostrar.')

# Função principal
def main():
    st.title('Gerenciamento de Clientes e Alarmes')

    if 'clientes_data' not in st.session_state:
        st.session_state['clientes_data'] = load_or_create_csv(file_name)

    if 'alarmes' not in st.session_state:
        st.session_state['alarmes'] = load_or_create_alarm_csv(alarm_file_name).to_dict('records')

    tab1, tab2 = st.tabs(['Cadastro e Ajuste de Alarmes', 'Visualização de Dados e Alarmes'])

    with tab1:
        st.header('Cadastrar Cliente')
        cadastrar_cliente()
        if 'last_data_limite' in st.session_state and 'last_data_entrega' in st.session_state:
            st.header('Definir Alarme')
            definir_alarme()

    with tab2:
        visualizar_dados()

    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
    if uploaded_file is not None:
        st.session_state['clientes_data'] = pd.read_csv(uploaded_file, parse_dates=['DATA LIMITE', 'DATA ENTREGA'])
        st.success('Arquivo CSV carregado com sucesso!')

if __name__ == '__main__':
    main()
