from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
p=Path(__file__).resolve().parent
df=pd.read_csv(p/'tariff_policy_preview.csv')
features=['Previous Tariff (%)','New Tariff (%)','Tariff Change (%)']
clean=df.dropna(subset=features).copy()
X=StandardScaler().fit_transform(clean[features])
model=IsolationForest(n_estimators=200,contamination=0.2,random_state=42)
clean['Anomaly Score']=model.fit(X).decision_function(X)
clean['Statistical Flag']=['Unusual' if v==-1 else 'Typical' for v in model.predict(X)]
clean[['HS Code','Product Category']+features+['Anomaly Score','Statistical Flag']].to_csv(p/'tariff_ml_results.csv',index=False)
print(clean['Statistical Flag'].value_counts())
