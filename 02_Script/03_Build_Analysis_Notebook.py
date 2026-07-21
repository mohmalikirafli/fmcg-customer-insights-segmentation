"""Build a concise, reproducible Jupyter notebook for the portfolio."""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "02_Script" / "FMCG_Customer_Insights_Analysis.ipynb"

notebook = nbf.v4.new_notebook()
notebook["metadata"]["kernelspec"] = {
    "display_name": "Python 3", "language": "python", "name": "python3"
}
notebook["cells"] = [
    nbf.v4.new_markdown_cell(
        "# FMCG Customer Insights: Consumer Segmentation and Purchase Drivers\n\n"
        "This portfolio case study uses synthetic, reproducibly generated data."
    ),
    nbf.v4.new_markdown_cell(
        "## Business questions\n"
        "1. Which consumer groups differ meaningfully?\n"
        "2. What predicts high new-product intention?\n"
        "3. What actions follow for brand, channel, and innovation teams?"
    ),
    nbf.v4.new_code_cell(
        "from pathlib import Path\nimport json, pandas as pd\n"
        "from IPython.display import Image, display\n"
        "ROOT = Path.cwd().parent if Path.cwd().name == '02_Script' else Path.cwd()\n"
        "DATA = ROOT/'03_Data'/'processed'/'fmcg_consumer_scored.csv'\n"
        "TABLES = ROOT/'04_Output'/'tables'\nFIGURES = ROOT/'04_Output'/'figures'\n"
        "data = pd.read_csv(DATA)\nmetrics = json.loads((TABLES/'key_metrics.json').read_text())\n"
        "data.shape, metrics"
    ),
    nbf.v4.new_markdown_cell("## Segment evidence"),
    nbf.v4.new_code_cell("pd.read_csv(TABLES/'segment_sizes.csv')"),
    nbf.v4.new_code_cell("display(Image(filename=str(FIGURES/'02_segment_profile_heatmap.png')))"),
    nbf.v4.new_markdown_cell("## Channel behavior"),
    nbf.v4.new_code_cell("pd.read_csv(TABLES/'channel_by_segment_pct.csv', index_col=0)"),
    nbf.v4.new_code_cell("display(Image(filename=str(FIGURES/'03_channel_by_segment.png')))"),
    nbf.v4.new_markdown_cell("## Purchase-intention drivers"),
    nbf.v4.new_code_cell("pd.read_csv(TABLES/'purchase_intention_drivers.csv').head(15)"),
    nbf.v4.new_code_cell("display(Image(filename=str(FIGURES/'07_purchase_intention_roc_curve.png')))"),
    nbf.v4.new_markdown_cell(
        "## Business recommendations\n"
        "- Digital Trend Explorers: social discovery, reviews, and launch trials.\n"
        "- Quality & Wellness Enthusiasts: credible benefits and premium innovation.\n"
        "- Convenience Loyalists: availability and frictionless repeat purchase.\n"
        "- Value Seekers: bundles, price ladders, and targeted promotions."
    ),
]
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
nbf.write(notebook, OUTPUT)
print(f"Notebook created at {OUTPUT}")
