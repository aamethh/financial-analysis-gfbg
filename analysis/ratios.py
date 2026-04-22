import pandas as pd

df = pd.read_excel("data/gfbg_dataset.xlsx")
df.columns = ['Metrica', '2023', '2024', '2025', 'YoY']

def get(metrica, year):
    return df.loc[df['Metrica'].str.contains(metrica, case=False, na=False), year].values[0]

years = ['2023', '2024', '2025']
results = []

for y in years:
    activos     = get('Activos', y)
    prestamos   = get('stamos', y)
    depositos   = get('sit', y)
    patrimonio  = get('atrimonio', y)
    utilidad    = get('tilidad', y)
    aum         = get('AUM', y)

    roa              = utilidad / activos
    roe              = utilidad / patrimonio
    loan_to_deposit  = prestamos / depositos
    capital_mult     = activos / patrimonio
    aum_to_assets    = aum / activos
    aum_to_loans     = aum / prestamos

    results.append({
        'Año':                   y,
        'ROA (%)':               round(roa * 100, 2),
        'ROE (%)':               round(roe * 100, 2),
        'Loan-to-Deposit (%)':   round(loan_to_deposit * 100, 2),
        'Multiplicador Capital': round(capital_mult, 2),
        'AUM / Activos (%)':     round(aum_to_assets * 100, 2),
        'AUM / Préstamos (%)':   round(aum_to_loans * 100, 2),
    })

ratios = pd.DataFrame(results).set_index('Año')
print(ratios.T.to_string())
