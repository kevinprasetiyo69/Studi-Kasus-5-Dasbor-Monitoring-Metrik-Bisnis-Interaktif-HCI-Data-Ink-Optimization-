import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='Executive Performance Dashboard', layout='wide')

np.random.seed(42)
dates = pd.date_range(start='2026-01-01', periods=60, freq='D')
categories = ['Software', 'Hardware', 'Services']

data_records = []
for d in dates:
  for cat in categories:
    val = np.random.normal(50, 15)
    if d == dates[45] and cat == 'Software':
      val = 12.0
    data_records.append({
        'Tanggal': d,
        'Kategori': cat,
        'Revenue_Juta': max(5.0, val),
        'Target_Juta': 48.0,
    })

df = pd.DataFrame(data_records)

st.title('Executive Performance Dashboard')
st.caption(
    'Menerapkan prinsip HCI: Data-Ink Ratio, Pre-Attentive Attribute, & Detail'
    ' on Demand.'
)

st.sidebar.header('Filter & Kontrol (User Control)')
selected_cat = st.sidebar.multiselect(
    'Pilih Kategori:',
    options=categories,
    default=categories,
    help='Gunakan filter untuk menyederhanakan beban kognitif',
)

filtered_df = df[df['Kategori'].isin(selected_cat)]

st.subheader('1. Overview First (High Data-Ink Ratio)')
col1, col2, col3 = st.columns(3)

total_rev = filtered_df['Revenue_Juta'].sum()
avg_rev = filtered_df['Revenue_Juta'].mean()
anomalies_count = (filtered_df['Revenue_Juta'] < 20).sum()

col1.metric('Total Revenue', f'Rp {total_rev:,.0f} Jt')
col2.metric('Rata-rata Harian', f'Rp {avg_rev:.1f} Jt')
col3.metric('Anomali Kritis (Pre-Attentive)', f'{anomalies_count} Insiden')

st.markdown('---')

st.subheader('2. Zoom & Filter (Tren Penjualan & Deteksi Anomali)')

fig = go.Figure()

for cat in selected_cat:
  sub = filtered_df[filtered_df['Kategori'] == cat]
  fig.add_trace(
      go.Scatter(
          x=sub['Tanggal'],
          y=sub['Revenue_Juta'],
          mode='lines',
          name=cat,
          line=dict(width=2),
      )
  )

anomalies = filtered_df[filtered_df['Revenue_Juta'] < 20]
if not anomalies.empty:
  fig.add_trace(
      go.Scatter(
          x=anomalies['Tanggal'],
          y=anomalies['Revenue_Juta'],
          mode='markers',
          name='Peringatan Anomali',
          marker=dict(color='crimson', size=10, symbol='circle'),
          hoverinfo='text',
          text=[
              f'Peringatan: {row.Kategori} drop ke {row.Revenue_Juta:.1f} Jt'
              for row in anomalies.itertuples()
          ],
      )
  )

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
    yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Revenue (Juta Rp)'),
    margin=dict(l=40, r=40, t=20, b=40),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
)

st.plotly_chart(fig, use_container_width=True)

st.subheader('3. Details on Demand')
with st.expander('Klik untuk melihat rincian tabel transaksi data mentah'):
  st.dataframe(
      filtered_df.sort_values(by='Tanggal', ascending=False),
      use_container_width=True,
  )