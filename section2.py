import csv

def clean_header(field):
    field = field.strip()
    return (
        field.replace("Ã©", "é")
             .replace("Ã¨", "è")
             .replace("Ã»", "û")
             .replace("Ã", "à")
             .replace("Â", "")
             .replace("CoÃ»t", "Coût")
             .replace("BÃ©nÃ©fice", "Bénéfice")
    )

def load_actions_from_csv(filename):
    actions = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        headers = [clean_header(h) for h in headers]

        name_idx = headers.index("Actions #")
        cost_idx = headers.index("Coût par action (en euros)")
        profit_idx = headers.index("Bénéfice (après 2 ans)")

        for row in reader:
            try:
                name = row[name_idx].strip()
                cost = float(row[cost_idx].strip())
                profit_percent = float(row[profit_idx].strip().replace('%', '').replace(',', '.'))
                profit = cost * (profit_percent / 100)

                if cost > 0 and profit > 0:
                    # Arrondir le coût à l'entier pour simplifier (sac à dos)
                    actions.append((name, int(cost), profit))
            except:
                continue
    return actions

def knapsack(actions, max_budget=500):
    n = len(actions)
    dp = [[0] * (max_budget + 1) for _ in range(n + 1)]

    # Remplissage de la table dynamique
    for i in range(1, n + 1):
        name, cost, profit = actions[i - 1]
        for w in range(max_budget + 1):
            if cost <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - cost] + profit)
            else:
                dp[i][w] = dp[i - 1][w]

    # Reconstruction du portefeuille optimal
    w = max_budget
    selected_actions = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            name, cost, profit = actions[i - 1]
            selected_actions.append((name, cost, profit))
            w -= cost

    return selected_actions, dp[n][max_budget]

if __name__ == "__main__":
    filename = "actions.csv"
    actions = load_actions_from_csv(filename)
    portfolio, total_profit = knapsack(actions)

    print("Meilleure combinaison d'actions (optimisée) :")
    for name, cost, profit in reversed(portfolio):
        print(f"{name} - Coût: {cost}€, Bénéfice: {round(profit, 2)}€")

    total_cost = sum(cost for _, cost, _ in portfolio)
    print(f"\nCoût total: {total_cost}€")
    print(f"Bénéfice total après 2 ans: {round(total_profit, 2)}€")
