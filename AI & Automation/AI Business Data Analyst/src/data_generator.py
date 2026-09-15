import numpy as np
import pandas as pd

PRODUCT_CATALOG = {
    "Laptop": {"base_price": 900, "base_cost": 650},
    "Monitor": {"base_price": 250, "base_cost": 160},
    "Keyboard": {"base_price": 80, "base_cost": 40},
    "Mouse": {"base_price": 40, "base_cost": 18},
    "Headphones": {"base_price": 150, "base_cost": 85},
}

QUANTITY_RANGES = {
    "Laptop": (1, 4),
    "Monitor": (1, 5),
    "Keyboard": (1, 8),
    "Mouse": (1, 10),
    "Headphones": (1, 6),
}

def generate_business_data(n: int = 1000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    products = rng.choice(list(PRODUCT_CATALOG.keys()), n)
    date_range = pd.date_range("2026-01-01", "2026-12-31")
    dates = pd.to_datetime(rng.choice(date_range, n))
    regions = rng.choice(["North", "Center", "South"], n)

    price_variation = rng.uniform(0.90, 1.10, n)
    cost_variation = rng.uniform(0.95, 1.05, n)

    units = [
        rng.integers(QUANTITY_RANGES[p][0], QUANTITY_RANGES[p][1] + 1)
        for p in products
    ]

    unit_prices = [
        PRODUCT_CATALOG[p]["base_price"] * variation
        for p, variation in zip(products, price_variation)
    ]

    unit_costs = [
        PRODUCT_CATALOG[p]["base_cost"] * variation
        for p, variation in zip(products, cost_variation)
    ]

    df = pd.DataFrame({
        "date": dates,
        "product": products,
        "region": regions,
        "units": units,
        "unit_price": unit_prices,
        "unit_cost": unit_costs,
    }).sort_values("date").reset_index(drop=True)

    laptop_south = (
        (df["product"] == "Laptop")
        & (df["region"] == "South")
    )

    eligible = df[laptop_south]
    if not eligible.empty:
        discounted_idx = eligible.sample(
            frac=0.20,
            random_state=seed,
        ).index
        df.loc[discounted_idx, "unit_price"] *= 0.65

    headphone_cost = (
        (df["product"] == "Headphones")
        & (df["date"] >= "2026-07-01")
    )
    df.loc[headphone_cost, "unit_cost"] *= 1.30

    return df
