import csv
import os
from typing import List, Tuple, Dict


def load_dataset(file_path: str) -> List[Tuple[str, int, float]]:
    actions = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                name = row["name"]
                price = float(row["price"])
                profit = float(row["profit"])
                if price > 0 and profit > 0:
                    actions.append((name, int(price), profit))
            except:
                continue
    return actions


def knapsack(actions: List[Tuple[str, int, float]], max_budget: int = 500):
    n = len(actions)
    dp = [[0] * (max_budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name, cost, profit = actions[i - 1]
        for w in range(max_budget + 1):
            if cost <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - cost] + profit)
            else:
                dp[i][w] = dp[i - 1][w]

    # Reconstruction
    w = max_budget
    selected = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            name, cost, profit = actions[i - 1]
            selected.append((name, cost, profit))
            w -= cost

    return selected, dp[n][max_budget]


def load_sienna_solution1(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if "Sienna bought:" in line:
            index = lines.index(line) + 1
            break
    return [lines[index].strip()] if index < len(lines) else []

def load_sienna_solution2(file_path: str) -> List[str]:
    actions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("Share-"):
                parts = line.split()
                actions.append(parts[0].strip())
    return actions


def compare_portfolios(algo_portfolio, sienna_actions, dataset_name):
    algo_names = {name for name, _, _ in algo_portfolio}
    algo_cost = sum(cost for _, cost, _ in algo_portfolio)
    algo_profit = sum(profit for _, _, profit in algo_portfolio)

    matching = algo_names.intersection(sienna_actions)
    only_algo = algo_names - set(sienna_actions)
    only_sienna = set(sienna_actions) - algo_names

    print(f"\n===== {dataset_name} =====")
    print(f"\nPortfolio généré par l'algorithme :")
    for name, cost, profit in algo_portfolio:
        print(f"{name} - Coût : {cost}€, Bénéfice : {round(profit, 2)}€")
    print(f"\nTotal Coût : {algo_cost}€, Bénéfice : {round(algo_profit, 2)}€")

    print("\nComparaison avec le portefeuille de Sienna :")
    print(f"Actions communes : {sorted(matching)}")
    print(f"Actions uniquement dans l'algo : {sorted(only_algo)}")
    print(f"Actions uniquement dans Sienna : {sorted(only_sienna)}")


if __name__ == "__main__":
    dataset1 = load_dataset("dataset1_Python+P7.csv")
    dataset2 = load_dataset("dataset2_Python+P7.csv")

    # Algo
    portfolio1, _ = knapsack(dataset1)
    portfolio2, _ = knapsack(dataset2)

    # Sienna
    sienna1 = load_sienna_solution1("solution1_Python+P7.txt")
    sienna2 = load_sienna_solution2("solution2_Python+P7.txt")

    # Comparaison
    compare_portfolios(portfolio1, sienna1, "DATASET 1")
    compare_portfolios(portfolio2, sienna2, "DATASET 2")
