def is_critical(row):
    return (
        row["cvss"] is not None
        and row["cvss"] >= 7
        and row["epss"] is not None
        and row["epss"] >= 0.7
    )
