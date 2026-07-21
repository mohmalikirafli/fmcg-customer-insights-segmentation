from pathlib import Path
import nbformat as nbf

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'notebooks/01_fmcg_customer_insights.ipynb'
nb=nbf.v4.new_notebook(); nb['cells']=[
nbf.v4.new_markdown_cell('# FMCG Customer Insights\nSynthetic consumer segmentation and purchase-driver case study.'),
nbf.v4.new_markdown_cell('## Business questions\n1. Which consumer groups differ meaningfully?\n2. What predicts willingness to try new products?\n3. What actions follow for brand, channel, and innovation teams?'),
nbf.v4.new_code_cell("from pathlib import Path\nimport json, pandas as pd\nfrom IPython.display import Image, display\nROOT=Path.cwd().parent if Path.cwd().name=='notebooks' else Path.cwd()\ndf=pd.read_csv(ROOT/'data/processed/fmcg_consumer_scored.csv')\nmetrics=json.loads((ROOT/'outputs/tables/key_metrics.json').read_text())\ndf.shape, metrics"),
nbf.v4.new_markdown_cell('## Segment evidence'),
nbf.v4.new_code_cell("pd.read_csv(ROOT/'outputs/tables/segment_sizes.csv')"),
nbf.v4.new_code_cell("display(Image(filename=str(ROOT/'outputs/figures/02_segment_profile_heatmap.png')))"),
nbf.v4.new_markdown_cell('## Channel behaviour'),
nbf.v4.new_code_cell("pd.read_csv(ROOT/'outputs/tables/channel_by_segment_pct.csv',index_col=0)"),
nbf.v4.new_markdown_cell('## Purchase-intention drivers'),
nbf.v4.new_code_cell("pd.read_csv(ROOT/'outputs/tables/purchase_intention_drivers.csv').head(15)"),
nbf.v4.new_markdown_cell('## Recommendations\n- Digital Trend Explorers: creator seeding, reviews, social commerce, and trial.\n- Quality & Wellness Enthusiasts: credible benefits and premium innovation.\n- Convenience Loyalists: availability, trust, and frictionless repurchase.\n- Value Seekers: pack-price architecture, bundles, and targeted promotions.\n\nThese hypotheses require validation with observed market data.')]
OUT.parent.mkdir(parents=True,exist_ok=True); nbf.write(nb,OUT); print(OUT)
