from pathlib import Path
import json
import pandas as pd
from data_cleaning import load_data


def calculate_kpis(df: pd.DataFrame) -> dict:
    active = df.loc[df.IsActiveMember == 1, 'Exited'].mean()
    inactive = df.loc[df.IsActiveMember == 0, 'Exited'].mean()
    one = df.loc[df.NumOfProducts == 1, 'Exited'].mean()
    multi = df.loc[df.NumOfProducts >= 2, 'Exited'].mean()
    premium = df[df.PremiumRisk == 1]
    sticky = df[(df.IsActiveMember == 1) & (df.NumOfProducts >= 2) & (df.HasCrCard == 1)]
    return {
        'customers': len(df),
        'overall_churn_rate': round(df.Exited.mean() * 100, 2),
        'active_churn_rate': round(active * 100, 2),
        'inactive_churn_rate': round(inactive * 100, 2),
        'engagement_retention_ratio': round(inactive / active, 2),
        'active_vs_inactive_churn_gap_pp': round((inactive - active) * 100, 2),
        'one_product_churn_rate': round(one * 100, 2),
        'multi_product_churn_rate': round(multi * 100, 2),
        'product_depth_retention_lift_pp': round((one - multi) * 100, 2),
        'high_balance_threshold': round(df.Balance.quantile(.75), 2),
        'high_balance_disengagement_rate': round(((df.Balance >= df.Balance.quantile(.75)) & (df.IsActiveMember == 0)).mean() * 100, 2),
        'premium_risk_customers': len(premium),
        'premium_risk_churn_rate': round(premium.Exited.mean() * 100, 2),
        'sticky_customer_rate': round(len(sticky) / len(df) * 100, 2),
        'sticky_customer_churn_rate': round(sticky.Exited.mean() * 100, 2),
    }


def segment_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby('EngagementProfile', observed=False)
            .agg(customers=('CustomerId', 'size'), churn_rate=('Exited', 'mean'), avg_balance=('Balance', 'mean'), avg_products=('NumOfProducts', 'mean'))
            .reset_index().sort_values('churn_rate', ascending=False))


def run_analysis(data_path, output_dir):
    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    df = load_data(data_path)
    kpis = calculate_kpis(df)
    df.to_csv(output_dir / 'enriched_customers.csv', index=False)
    (output_dir / 'metrics.json').write_text(json.dumps({'kpis': kpis, 'profiles': segment_summary(df).to_dict('records')}, indent=2, default=float))
    return df, kpis


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    _, kpis = run_analysis(root / 'data' / 'European_Bank.csv', root / 'outputs')
    print(json.dumps(kpis, indent=2))
