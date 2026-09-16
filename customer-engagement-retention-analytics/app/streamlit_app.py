from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from data_cleaning import load_data
from analysis import calculate_kpis

st.set_page_config(page_title='Retention Intelligence | European Bank', page_icon='◆', layout='wide', initial_sidebar_state='expanded')

# ---- Visual system ---------------------------------------------------------
st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
:root { --navy:#102A43; --blue:#1976D2; --teal:#11A683; --coral:#E76F51; --amber:#F4A261; --ink:#243B53; --muted:#627D98; --line:#D9E2EC; --paper:#F6F9FC; }
html, body, [class*="css"] { font-family:'DM Sans', sans-serif; }
.stApp { background:var(--paper); }
.block-container { padding-top:2rem; padding-bottom:3rem; max-width:1450px; }
[data-testid="stSidebar"] { background:#102A43; }
[data-testid="stSidebar"] * { color:#F0F4F8 !important; }
[data-testid="stSidebar"] .stCaption { color:#B8C7D9 !important; }
[data-testid="stSidebar"] hr { border-color:#486581; }
h1,h2,h3 { font-family:'Manrope', sans-serif; color:var(--navy); letter-spacing:-.03em; }
h1 { font-size:2.35rem; margin-bottom:.25rem; }
h2 { font-size:1.45rem; margin-top:1.5rem; }
.hero { background:linear-gradient(115deg,#102A43 0%,#1B4965 62%,#1976D2 100%); color:white; padding:2rem 2.2rem; border-radius:18px; box-shadow:0 10px 28px rgba(16,42,67,.16); margin-bottom:1.25rem; }
.hero h1 { color:white; margin:0; font-size:2.35rem; }
.hero p { color:#D9E2EC; margin:.5rem 0 0; font-size:1.02rem; }
.eyebrow { color:#8FE3C7; font-size:.76rem; font-weight:700; letter-spacing:.13em; text-transform:uppercase; margin-bottom:.6rem; }
.section-label { color:var(--muted); font-size:.76rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase; margin:1.35rem 0 .45rem; }
.kpi { background:white; border:1px solid var(--line); border-radius:14px; padding:1rem 1.1rem; min-height:116px; box-shadow:0 4px 14px rgba(16,42,67,.04); }
.kpi .label { color:var(--muted); font-size:.78rem; font-weight:600; }
.kpi .value { color:var(--navy); font-family:'Manrope',sans-serif; font-size:1.65rem; font-weight:800; margin-top:.25rem; }
.kpi .hint { color:var(--muted); font-size:.75rem; margin-top:.25rem; }
.callout { background:#E8F7F2; border-left:4px solid var(--teal); border-radius:8px; padding:.85rem 1rem; color:#174A42; margin:.7rem 0 1rem; }
.risk-callout { background:#FFF4EF; border-left:4px solid var(--coral); border-radius:8px; padding:.85rem 1rem; color:#743426; margin:.7rem 0 1rem; }
div[data-testid="stMetric"] { background:white; border:1px solid var(--line); border-radius:14px; padding:1rem; }
.stTabs [data-baseweb="tab-list"] { gap:2rem; }
.stTabs [data-baseweb="tab"] { font-weight:600; color:var(--muted); }
.stTabs [aria-selected="true"] { color:var(--blue) !important; border-bottom-color:var(--blue) !important; }
button[kind="primary"] { background:var(--blue); border-color:var(--blue); }
[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; }
</style>
''', unsafe_allow_html=True)

@st.cache_data
def get_data():
    return load_data(ROOT / 'data' / 'European_Bank.csv')

df = get_data(); kpis = calculate_kpis(df)

# ---- Sidebar ---------------------------------------------------------------
with st.sidebar:
    st.markdown('## ◆ RETENTION\n## INTELLIGENCE')
    st.caption('European Bank | Customer behavior workspace')
    st.divider()
    st.markdown('### Audience filters')
    geos = st.multiselect('Geography', sorted(df.Geography.unique()), sorted(df.Geography.unique()))
    activity = st.multiselect('Engagement status', ['Active', 'Inactive'], ['Active', 'Inactive'])
    products = st.slider('Product count', int(df.NumOfProducts.min()), int(df.NumOfProducts.max()), (1, 4))
    min_balance = st.slider('Minimum balance', 0.0, float(df.Balance.max()), 0.0, 5000.0, format='$%.0f')
    min_salary = st.slider('Minimum estimated salary', 0.0, float(df.EstimatedSalary.max()), 0.0, 5000.0, format='$%.0f')
    risk_only = st.checkbox('Show premium-risk customers only')
    st.divider()
    st.caption('High balance = sample 75th percentile or above. Premium risk = high balance + inactive status.')

view = df[df.Geography.isin(geos) & df.ActivityLabel.isin(activity) & df.NumOfProducts.between(*products) & (df.Balance >= min_balance) & (df.EstimatedSalary >= min_salary)].copy()
if risk_only: view = view[view.PremiumRisk == 1]

# ---- Header ----------------------------------------------------------------
st.markdown('''<div class="hero"><div class="eyebrow">Customer retention strategy · 2025 snapshot</div><h1>Retention Intelligence</h1><p>Turn engagement and relationship depth into practical retention priorities.</p></div>''', unsafe_allow_html=True)

# KPI strip
st.markdown('<div class="section-label">Portfolio pulse</div>', unsafe_allow_html=True)
kpis_view = [
    ('Customers in view', f'{len(view):,}', 'Current filter scope'),
    ('Churn rate', f'{view.Exited.mean()*100:.1f}%' if len(view) else '—', 'Observed in selected audience'),
    ('Engagement gap', f'{kpis["active_vs_inactive_churn_gap_pp"]:.1f} pp', 'Inactive vs active churn'),
    ('Depth lift', f'{kpis["product_depth_retention_lift_pp"]:.1f} pp', '1 product vs 2+ products'),
    ('Premium risk pool', f'{kpis["premium_risk_customers"]:,}', f'{kpis["premium_risk_churn_rate"]:.1f}% churn'),
]
cols = st.columns(5)
for col, (label, value, hint) in zip(cols, kpis_view):
    col.markdown(f'<div class="kpi"><div class="label">{label}</div><div class="value">{value}</div><div class="hint">{hint}</div></div>', unsafe_allow_html=True)

if not len(view):
    st.warning('No customers match the selected filters. Relax one or more thresholds.')
    st.stop()

# ---- Tabs ------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(['Overview', 'Risk segments', 'Customer list'])

plot_base = dict(template='simple_white', font=dict(family='DM Sans', color='#243B53'), paper_bgcolor='white', plot_bgcolor='white', margin=dict(l=20,r=20,t=55,b=30), height=360)

with tab1:
    st.markdown('<div class="section-label">Executive readout</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="callout"><b>What stands out:</b> inactive customers churn at <b>{kpis["inactive_churn_rate"]:.1f}%</b> versus <b>{kpis["active_churn_rate"]:.1f}%</b> for active customers. Product depth is also associated with lower churn, but three- and four-product records require investigation before being treated as a success pattern.</div>', unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        a = view.groupby('ActivityLabel', as_index=False).Exited.mean(); a['Churn rate'] = a.pop('Exited') * 100
        fig = px.bar(a, x='ActivityLabel', y='Churn rate', color='ActivityLabel', text='Churn rate', color_discrete_map={'Active':'#11A683','Inactive':'#E76F51'}, title='Engagement is the clearest retention signal')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside'); fig.update_layout(showlegend=False, yaxis_range=[0, max(35, a['Churn rate'].max()+8)], **plot_base)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        p = view.groupby('NumOfProducts', as_index=False).Exited.mean(); p['Churn rate'] = p.pop('Exited') * 100
        fig = px.bar(p, x='NumOfProducts', y='Churn rate', text='Churn rate', color='Churn rate', color_continuous_scale=['#D9F2EC','#1976D2'], title='Relationship depth changes observed churn')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside'); fig.update_layout(coloraxis_showscale=False, yaxis_range=[0, max(110, p['Churn rate'].max()+8)], **plot_base)
        st.plotly_chart(fig, use_container_width=True)
    left, right = st.columns(2)
    with left:
        geo = view.groupby('Geography', as_index=False).Exited.mean(); geo['Churn rate'] = geo.pop('Exited') * 100
        fig = px.bar(geo, x='Geography', y='Churn rate', text='Churn rate', color='Geography', color_discrete_sequence=['#1976D2','#11A683','#F4A261'], title='Geographic variation')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside'); fig.update_layout(showlegend=False, **plot_base)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig = px.scatter(view.sample(min(len(view), 2500), random_state=7), x='Balance', y='EstimatedSalary', color='ChurnLabel', symbol='ActivityLabel', hover_data=['CustomerId','Geography','NumOfProducts'], color_discrete_map={'Retained':'#11A683','Exited':'#E76F51'}, title='Financial value and engagement are different signals')
        fig.update_layout(**plot_base); st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown('<div class="section-label">Prioritization lens</div>', unsafe_allow_html=True)
    profile = view.groupby('EngagementProfile', as_index=False).agg(Customers=('CustomerId','size'), ChurnRate=('Exited','mean'), AvgBalance=('Balance','mean'))
    profile['ChurnRate'] *= 100
    left, right = st.columns([1.15, .85])
    with left:
        fig = px.bar(profile.sort_values('ChurnRate'), x='ChurnRate', y='EngagementProfile', orientation='h', text='ChurnRate', color='ChurnRate', color_continuous_scale=['#D9F2EC','#1976D2','#E76F51'], title='Observed churn by engagement profile')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside'); fig.update_layout(coloraxis_showscale=False, **plot_base); st.plotly_chart(fig, use_container_width=True)
    with right:
        st.markdown('<div class="risk-callout"><b>At-risk premium customers</b><br>High balance does not guarantee loyalty. Focus on inactive customers before broad cross-sell activity.</div>', unsafe_allow_html=True)
        st.metric('High-balance threshold', f'${kpis["high_balance_threshold"]:,.0f}')
        st.metric('Premium-risk churn', f'{kpis["premium_risk_churn_rate"]:.1f}%')
        st.metric('Sticky-customer churn', f'{kpis["sticky_customer_churn_rate"]:.1f}%')
    st.dataframe(profile.assign(ChurnRate=profile.ChurnRate.map(lambda x: f'{x:.1f}%'), AvgBalance=profile.AvgBalance.map(lambda x: f'${x:,.0f}')), use_container_width=True, hide_index=True)

with tab3:
    st.markdown('<div class="section-label">Action queue</div>', unsafe_allow_html=True)
    st.markdown('Customers below are ordered to support retention review. Use the sidebar to narrow the audience, then download the resulting list.')
    risk = view[view.PremiumRisk == 1].copy().sort_values(['Exited','Balance'], ascending=[False,False])
    display_cols = ['CustomerId','Geography','Age','Balance','EstimatedSalary','NumOfProducts','HasCrCard','Exited','RelationshipStrengthIndex']
    if len(risk):
        st.dataframe(risk[display_cols].head(100), use_container_width=True, hide_index=True)
        st.download_button('Download premium-risk list (CSV)', risk[display_cols].to_csv(index=False).encode(), 'premium_risk_customers.csv', 'text/csv', type='primary')
    else:
        st.info('No high-balance disengaged customers match the current filters. Try widening the audience.')

with st.expander('Methodology and data quality'):
    st.write(f'Validated {len(df):,} unique customer records with {int(df.isna().sum().sum())} missing cells. Activity, credit-card ownership, and churn fields are binary and validated. All metrics are descriptive associations, not causal estimates.')
    st.write('Relationship Strength Index = 50 points for active membership + up to 35 points for product depth + 15 points for credit-card ownership. It is a transparent prioritization aid, not a credit or eligibility score.')
