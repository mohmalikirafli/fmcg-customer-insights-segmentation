from pathlib import Path
import json, numpy as np, pandas as pd, matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/'data/raw/fmcg_consumer_survey_synthetic.csv'; PROC=ROOT/'data/processed'; FIG=ROOT/'outputs/figures'; TAB=ROOT/'outputs/tables'
for p in [PROC,FIG,TAB]: p.mkdir(parents=True,exist_ok=True)
df=pd.read_csv(RAW)
constructs=['price_sensitivity','quality_orientation','health_orientation','sustainability_orientation','digital_influence','convenience_orientation','brand_trust','new_product_intention']
for c in constructs:
    cols=[f'{c}_{i}' for i in range(1,4)]
    df[cols]=df[cols].apply(lambda s:s.fillna(s.median()))
    df[c]=df[cols].mean(axis=1)
df['promotion_response']=df['promotion_response'].fillna(df['promotion_response'].median())
features=constructs[:-1]+['promotion_response']
X=StandardScaler().fit_transform(df[features])
scores=[]
for k in range(2,7): scores.append({'k':k,'silhouette_score':silhouette_score(X,KMeans(k,random_state=42,n_init=20).fit_predict(X))})
labels=KMeans(4,random_state=42,n_init=30).fit_predict(X)
cent=pd.DataFrame(X,columns=features).assign(cluster=labels).groupby('cluster').mean()
name_map={cent['price_sensitivity'].idxmax():'Value Seekers',cent['digital_influence'].idxmax():'Digital Trend Explorers',cent['convenience_orientation'].idxmax():'Convenience Loyalists'}
remaining=[i for i in cent.index if i not in name_map]; name_map[remaining[0]]='Quality & Wellness Enthusiasts'
df['segment']=pd.Series(labels).map(name_map)
seg_order=['Value Seekers','Digital Trend Explorers','Convenience Loyalists','Quality & Wellness Enthusiasts']
size=df['segment'].value_counts().reindex(seg_order).rename_axis('segment').reset_index(name='n'); size['share_pct']=(100*size.n/len(df)).round(1)
profiles=df.groupby('segment')[features+['monthly_fmcg_spend_idr','purchase_frequency_per_month']].mean().reindex(seg_order).round(2)
channel=pd.crosstab(df.segment,df.primary_shopping_channel,normalize='index').mul(100).reindex(seg_order).round(1)
category=pd.crosstab(df.segment,df.most_purchased_category,normalize='index').mul(100).reindex(seg_order).round(1)
rels=[]
for c in constructs:
    items=df[[f'{c}_{i}' for i in range(1,4)]].astype(float); k=items.shape[1]
    alpha=k/(k-1)*(1-items.var(ddof=1).sum()/items.sum(axis=1).var(ddof=1))
    rels.append({'construct':c,'cronbach_alpha':round(alpha,3)})
threshold=df.new_product_intention.quantile(.65); y=(df.new_product_intention>=threshold).astype(int)
num=['age','household_size','monthly_fmcg_spend_idr','purchase_frequency_per_month']+features[:-1]
cat=['gender','region','monthly_income_band','primary_shopping_channel','most_purchased_category']
pre=ColumnTransformer([('num',Pipeline([('imp',SimpleImputer(strategy='median')),('sc',StandardScaler())]),num),('cat',Pipeline([('imp',SimpleImputer(strategy='most_frequent')),('oh',OneHotEncoder(handle_unknown='ignore'))]),cat)])
model=Pipeline([('pre',pre),('lr',LogisticRegression(max_iter=2000,C=.7))])
Xtr,Xte,ytr,yte=train_test_split(df[num+cat],y,test_size=.25,random_state=42,stratify=y); model.fit(Xtr,ytr); auc=roc_auc_score(yte,model.predict_proba(Xte)[:,1])
names=model.named_steps['pre'].get_feature_names_out(); coefs=model.named_steps['lr'].coef_[0]
drivers=pd.DataFrame({'feature':names,'coefficient':coefs}).sort_values('coefficient',key=abs,ascending=False)
size.to_csv(TAB/'segment_sizes.csv',index=False); profiles.to_csv(TAB/'segment_profiles.csv'); channel.to_csv(TAB/'channel_by_segment_pct.csv'); category.to_csv(TAB/'category_by_segment_pct.csv'); pd.DataFrame(scores).to_csv(TAB/'silhouette_scores.csv',index=False); pd.DataFrame(rels).to_csv(TAB/'reliability_summary.csv',index=False); drivers.to_csv(TAB/'purchase_intention_drivers.csv',index=False); df.to_csv(PROC/'fmcg_consumer_scored.csv',index=False)
metrics={'n_respondents':len(df),'n_segments':4,'silhouette_score_k4':round([s['silhouette_score'] for s in scores if s['k']==4][0],3),'driver_model_roc_auc':round(auc,3),'high_intention_share_pct':round(100*y.mean(),1),'median_monthly_spend_idr':int(df.monthly_fmcg_spend_idr.median())}; (TAB/'key_metrics.json').write_text(json.dumps(metrics,indent=2))
plt.figure(figsize=(8,4.5)); plt.bar(size.segment,size.share_pct); plt.xticks(rotation=20,ha='right'); plt.ylabel('Share (%)'); plt.tight_layout(); plt.savefig(FIG/'01_segment_sizes.png',dpi=160); plt.close()
z=(profiles[features]-profiles[features].mean())/profiles[features].std(ddof=0); plt.figure(figsize=(10,4.8)); plt.imshow(z,aspect='auto'); plt.colorbar(label='Standardised profile'); plt.xticks(range(len(features)),[x.replace('_',' ').title() for x in features],rotation=35,ha='right'); plt.yticks(range(4),seg_order); plt.tight_layout(); plt.savefig(FIG/'02_segment_profile_heatmap.png',dpi=160); plt.close()
channel.plot(kind='bar',stacked=True,figsize=(9,5)); plt.ylabel('Share (%)'); plt.xticks(rotation=20,ha='right'); plt.legend(title='Primary channel',bbox_to_anchor=(1.02,1)); plt.tight_layout(); plt.savefig(FIG/'03_channel_by_segment.png',dpi=160); plt.close()
plt.figure(figsize=(8,4.5)); plt.bar(seg_order,profiles.monthly_fmcg_spend_idr/1e6); plt.ylabel('Average monthly spend (IDR million)'); plt.xticks(rotation=20,ha='right'); plt.tight_layout(); plt.savefig(FIG/'04_spend_by_segment.png',dpi=160); plt.close()
top=drivers.head(12).sort_values('coefficient'); plt.figure(figsize=(8,5)); plt.barh(top.feature.str.replace('num__','').str.replace('cat__',''),top.coefficient); plt.xlabel('Logistic regression coefficient'); plt.tight_layout(); plt.savefig(FIG/'05_purchase_intention_drivers.png',dpi=160); plt.close()
ss=pd.DataFrame(scores); plt.figure(figsize=(7,4)); plt.plot(ss.k,ss.silhouette_score,marker='o'); plt.xlabel('Number of clusters'); plt.ylabel('Silhouette score'); plt.tight_layout(); plt.savefig(FIG/'06_silhouette_scores.png',dpi=160); plt.close()
print(json.dumps(metrics,indent=2))
