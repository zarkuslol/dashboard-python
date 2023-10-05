import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide')

# Importar dados
data = pd.read_csv('./data/supermarket_sales.csv', sep=";", index_col=0, decimal=',')

# Tratamento da coluna Date
data['Date'] = pd.to_datetime(data['Date'])
data = data.sort_values(by='Date')

# Gerar coluna Month
data.loc[:, 'Month'] = data['Date'].apply(lambda x: f"{str(x.year)} - {str(x.month)}")

# Filtro dos dados com base no mês
month = st.sidebar.selectbox('Mês', data['Month'].unique())
data_filtered = data[data['Month'] == month]

# Colunas do dashboard
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Primeiro gráfico (Faturamento por mês por unidade)
fig_date = px.bar(data_filtered, x='Date', y='Total', color='City', title='Faturamento por mês por unidade')
col1.plotly_chart(fig_date, use_container_width=True)

# Segundo gráfico (Tipo de produto mais vendido)
fig_prod = px.bar(data_filtered, x='Total', y='Product line', color='City', title='Tipo de produto mais vendido')
col2.plotly_chart(fig_prod, use_container_width=True)

# Terceiro gráfico (Faturamento total por filial)
total_per_city = data_filtered.groupby("City")['Total'].sum().reset_index()
fig_city = px.bar(total_per_city, x='City', y='Total', title='Faturamento total por filial')
col3.plotly_chart(fig_city, use_container_width=True)

# Quarto gráfico (Desempenho das formas de pagamento)
payment = data_filtered.groupby('Payment')['Total'].sum().reset_index()
fig_payment = px.pie(payment, names='Payment', values='Total', title='Desempenho das formas de pagamento')
col4.plotly_chart(fig_payment, use_container_width=True)

# Quinto gráfico (Avaliação média por filial)
ratings = data_filtered.groupby('City')['Rating'].mean().reset_index()
fig_ratings = px.bar(ratings, x='City', y='Rating', title='Avaliação média por filial')
col5.plotly_chart(fig_ratings, use_container_width=True)
