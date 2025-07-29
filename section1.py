import csv
from itertools import combinations

# Nettoie les noms de colonnes mal encodés
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

# Charge les données et corrige les encodages
def load_actions_from_csv(filename):
    actions = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        headers = [clean_header(h) for h in headers]

        # Repérage des index
        name_idx = headers.index("Actions #")
        cost_idx = headers.index("Coût par action (en euros)")
        profit_idx = headers.index("Bénéfice (après 2 ans)")

        for row in reader:
            try:
                name = row[name_idx].strip()
                cost = float(row[cost_idx].strip())
                profit_percent = float(row[profit_idx].strip().replace('%', '').replace(',', '.'))
                profit = cost * (profit_percent / 100)

                # On garde uniquement les données valides
                if cost > 0 and profit > 0:
                    actions.append((name, cost, profit))
            except Exception as e:
                continue  # ignore les lignes invalides
    return actions

# Force brute : toutes les combinaisons possibles
def bruteforce_optimizer(actions, max_budget=500):
    best_combination = []
    best_profit = 0

    for i in range(1, len(actions) + 1):
        for subset in combinations(actions, i):
            total_cost = sum(action[1] for action in subset)
            total_profit = sum(action[2] for action in subset)

            if total_cost <= max_budget and total_profit > best_profit:
                best_combination = subset
                best_profit = total_profit

    return best_combination, best_profit

# Point d'entrée principal
if __name__ == "__main__":
    filename = "actions.csv"  # nom du fichier d'entrée
    actions = load_actions_from_csv(filename)

    if not actions:
        print("Aucune action valide chargée.")
    else:
        best_portfolio, max_profit = bruteforce_optimizer(actions)

        print("Meilleure combinaison d'actions :")
        for action in best_portfolio:
            print(f"{action[0]} - Coût: {action[1]}€, Bénéfice: {round(action[2], 2)}€")

        total_cost = sum(action[1] for action in best_portfolio)
        print(f"\nCoût total: {round(total_cost, 2)}€")
        print(f"Bénéfice total après 2 ans: {round(max_profit, 2)}€")
