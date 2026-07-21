from pathlib import Path
import numpy as np, pandas as pd

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'data/raw/fmcg_consumer_survey_synthetic.csv'
rng=np.random.default_rng(20260721); n=800
segments=['Value Seekers','Digital Trend Explorers','Convenience Loyalists','Quality & Wellness Enthusiasts']
weights=[.30,.25,.23,.22]
means={
'Value Seekers':[4.4,3.3,3.0,2.8,3.2,3.5,3.1,3.0],
'Digital Trend Explorers':[3.2,3.8,3.5,3.4,4.6,4.1,3.2,4.6],
'Convenience Loyalists':[3.1,3.9,3.3,3.0,2.8,4.6,4.5,3.2],
'Quality & Wellness Enthusiasts':[2.7,4.6,4.5,4.0,3.5,3.7,4.4,4.1]}
channels={
'Value Seekers':[.38,.20,.18,.24], 'Digital Trend Explorers':[.18,.15,.59,.08],
'Convenience Loyalists':[.50,.28,.16,.06], 'Quality & Wellness Enthusiasts':[.20,.35,.35,.10]}
base_spend={'Value Seekers':680000,'Digital Trend Explorers':920000,'Convenience Loyalists':1080000,'Quality & Wellness Enthusiasts':1260000}
base_freq={'Value Seekers':8,'Digital Trend Explorers':9,'Convenience Loyalists':10,'Quality & Wellness Enthusiasts':9}
constructs=['price_sensitivity','quality_orientation','health_orientation','sustainability_orientation','digital_influence','convenience_orientation','brand_trust','new_product_intention']
rows=[]
for i,s in enumerate(rng.choice(segments,n,p=weights),1):
    age=int(np.clip(rng.normal({'Value Seekers':29,'Digital Trend Explorers':25,'Convenience Loyalists':38,'Quality & Wellness Enthusiasts':34}[s],7),18,55))
    income=rng.choice(['< IDR 5M','IDR 5–10M','IDR 10–20M','> IDR 20M'],p={'Value Seekers':[.34,.37,.21,.08],'Digital Trend Explorers':[.25,.40,.26,.09],'Convenience Loyalists':[.10,.31,.38,.21],'Quality & Wellness Enthusiasts':[.08,.25,.40,.27]}[s])
    row={'respondent_id':f'R{i:04d}','age':age,'gender':rng.choice(['Woman','Man'],p=[.57,.43]),'region':rng.choice(['Java','Sumatra','Kalimantan','Sulawesi','Bali & Nusa Tenggara'],p=[.57,.19,.08,.10,.06]),'monthly_income_band':income,'household_size':int(np.clip(rng.poisson(2.2)+1,1,7)),'primary_shopping_channel':rng.choice(['Minimarket','Supermarket','E-commerce','Traditional market'],p=channels[s]),'most_purchased_category':rng.choice(['Personal care','Home care','Food & beverages']),'monthly_fmcg_spend_idr':int(np.clip(rng.lognormal(np.log(base_spend[s]),.24)//10000*10000,250000,3500000)),'purchase_frequency_per_month':int(np.clip(round(rng.normal(base_freq[s],2)),2,18)),'promotion_response':int(np.clip(round(rng.normal(4.3 if s=='Value Seekers' else 3.3,.7)),1,5))}
    for c,m in zip(constructs,means[s]):
        latent=rng.normal(m,.5)
        for j in range(1,4): row[f'{c}_{j}']=int(np.clip(round(.8*latent+.2*3+rng.normal(0,.35)),1,5))
    rows.append(row)
df=pd.DataFrame(rows)
for col in ['monthly_income_band','promotion_response','sustainability_orientation_3']:
    df.loc[rng.choice(df.index,8,replace=False),col]=np.nan
OUT.parent.mkdir(parents=True,exist_ok=True); df.to_csv(OUT,index=False); print(f'Generated {len(df)} rows')
