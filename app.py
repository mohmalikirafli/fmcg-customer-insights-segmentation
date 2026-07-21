from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data/processed/fmcg_consumer_scored.csv'
st.set_page_config(page_title='FMCG Customer Insights',layout='wide')
st.title('FMCG Customer Insights Dashboard')
st.caption('Synthetic portfolio case study — not a real market estimate')
if not DATA.exists():
    st.warning('Run `python src/generate_data.py` and `python src/analyze.py` first.')
    st.stop()
df=pd.read_csv(DATA)
segments=sorted(df.segment.dropna().unique())
selected=st.sidebar.multiselect('Consumer segment',segments,default=segments)
view=df[df.segment.isin(selected)]
a,b,c=st.columns(3)
a.metric('Consumers',f'{len(view):,}')
b.metric('Median monthly spend',f"IDR {view.monthly_fmcg_spend_idr.median()/1e6:.2f}M")
c.metric('Average purchase frequency',f"{view.purchase_frequency_per_month.mean():.1f}×/month")
left,right=st.columns(2)
with left:
    share=view.segment.value_counts().rename_axis('segment').reset_index(name='consumers')
    st.plotly_chart(px.bar(share,x='segment',y='consumers',title='Segment size'),use_container_width=True)
with right:
    channel=pd.crosstab(view.segment,view.primary_shopping_channel,normalize='index').mul(100).reset_index().melt('segment',var_name='channel',value_name='share')
    st.plotly_chart(px.bar(channel,x='segment',y='share',color='channel',title='Primary shopping channel',barmode='stack'),use_container_width=True)
traits=['price_sensitivity','quality_orientation','health_orientation','sustainability_orientation','digital_influence','convenience_orientation','brand_trust','new_product_intention']
profile=view.groupby('segment')[traits].mean().reset_index().melt('segment',var_name='trait',value_name='score')
st.plotly_chart(px.line(profile,x='trait',y='score',color='segment',markers=True,title='Consumer attitude profiles'),use_container_width=True)
st.dataframe(view[['respondent_id','segment','age','monthly_income_band','primary_shopping_channel','monthly_fmcg_spend_idr','new_product_intention']],use_container_width=True)
