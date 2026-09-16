from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid', context='notebook')


def create_charts(df, output_dir):
    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    activity = df.groupby('ActivityLabel').Exited.mean().reindex(['Active', 'Inactive']) * 100
    products = df.groupby('NumOfProducts').Exited.mean() * 100
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].bar(activity.index, activity.values, color=['#14B8A6', '#F97366'])
    axes[0].set(title='Churn rate by activity', ylabel='Churn rate (%)'); axes[0].set_ylim(0, 35)
    axes[1].bar(products.index.astype(str), products.values, color='#17324D')
    axes[1].set(title='Churn rate by product count', xlabel='Products', ylabel='Churn rate (%)'); axes[1].set_ylim(0, 110)
    fig.tight_layout(); fig.savefig(output_dir / 'engagement_product_churn.png', dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    profile = df.groupby('EngagementProfile').Exited.mean().sort_values() * 100
    ax.barh(profile.index, profile.values, color='#14B8A6')
    ax.set(title='Churn rate across engagement profiles', xlabel='Churn rate (%)')
    fig.tight_layout(); fig.savefig(output_dir / 'profile_churn.png', dpi=180); plt.close(fig)
