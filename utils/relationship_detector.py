def detect_relationships(dataframes):
    relationships = []
    for name_a, df_a in dataframes.items():
        for name_b, df_b in dataframes.items():
            if name_a == name_b:
                continue
            for col_a in df_a.columns:
                for col_b in df_b.columns:
                    if df_a[col_a].dtype == df_b[col_b].dtype:
                        match_ratio = df_a[col_a].isin(df_b[col_b]).mean()
                        if 0.85 < match_ratio < 1.05:
                            relationships.append((name_a, col_a, name_b, col_b))
    return relationships
