from pathlib import Path
import numpy as np
import pandas as pd


def load_data(path: str | Path) -> pd.DataFrame:
    """Load and validate the source customer data."""
    df = pd.read_csv(path)
    required = {'CustomerId','Geography','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary','Exited'}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f'Missing required columns: {sorted(missing)}')
    if df.CustomerId.duplicated().any():
        raise ValueError('CustomerId must be unique')
    for col in ['HasCrCard','IsActiveMember','Exited']:
        if not df[col].isin([0, 1]).all():
            raise ValueError(f'{col} must contain only 0/1 values')
    return enrich_data(df)


def enrich_data(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    q75 = out['Balance'].quantile(.75)
    out['ActivityLabel'] = out['IsActiveMember'].map({1: 'Active', 0: 'Inactive'})
    out['ChurnLabel'] = out['Exited'].map({1: 'Exited', 0: 'Retained'})
    out['HighBalance'] = (out['Balance'] >= q75).astype(int)
    out['PremiumRisk'] = ((out['HighBalance'] == 1) & (out['IsActiveMember'] == 0)).astype(int)
    out['EngagementProfile'] = np.select([
        (out.IsActiveMember == 1) & (out.NumOfProducts >= 2),
        (out.IsActiveMember == 0) & (out.Balance >= q75),
        (out.IsActiveMember == 1) & (out.NumOfProducts == 1),
        (out.IsActiveMember == 0) & (out.NumOfProducts == 1),
    ], ['Active multi-product','Inactive high-balance','Active low-product','Inactive low-product'], default='Other')
    out['RelationshipStrengthIndex'] = (out.IsActiveMember * 50 + np.minimum(out.NumOfProducts, 2) / 2 * 35 + out.HasCrCard * 15).round(1)
    return out


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    df = load_data(root / 'data' / 'European_Bank.csv')
    print(df.shape)
    print(df[['ActivityLabel','EngagementProfile','PremiumRisk']].head())
