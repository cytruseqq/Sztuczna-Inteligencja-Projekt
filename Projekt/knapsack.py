import random

def optimal_for_types(items, budget, required_types):
    # Grupuj przedmioty po typie
    groups = {}
    for item in items:
        t = item['type']
        if t in required_types:
            if t not in groups:
                groups[t] = []
            groups[t].append(item)
    
    # Lista grup w kolejności required_types
    group_list = [groups.get(t, []) for t in required_types]
    
    n = len(group_list)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        group = group_list[i-1]
        for j in range(budget + 1):
            max_val = 0
            for item in group:
                if item['price'] <= j:
                    max_val = max(max_val, item['value'] + dp[i-1][j - item['price']])
            dp[i][j] = max_val
    
    return dp[n][budget]

def fitness(solution, items, budget):
    total_value = 0
    total_price = 0
    for i, include in enumerate(solution):
        if include:
            total_value += items[i]['value']
            total_price += items[i]['price']
    if total_price > budget:
        return 0
    return total_value

def harmony_search(items, budget, required_types, HMS=10, HMCR=0.9, PAR=0.3, iterations=100):
    # Grupuj przedmioty po typie
    items_by_type = {}
    for item in items:
        t = item['type']
        if t not in items_by_type:
            items_by_type[t] = []
        items_by_type[t].append(item)
    
    # Dla wymaganych typów, wybierz dokładnie jeden z każdego
    n_required = len(required_types)
    if n_required == 0:
        return []  # Brak wymaganych typów
    
    # Inicjalizuj HM z losowymi wyborami
    HM = []
    for _ in range(HMS):
        sol = []
        for t in required_types:
            if t in items_by_type and items_by_type[t]:
                chosen = random.choice(items_by_type[t])
                sol.append(chosen)
        HM.append(sol)
    
    # Fitness
    def fitness_sol(sol):
        total_value = sum(item['value'] for item in sol)
        total_price = sum(item['price'] for item in sol)
        if total_price > budget:
            return 0
        return total_value
    
    HM_fitness = [fitness_sol(s) for s in HM]
    
    for _ in range(iterations):
        # Nowa harmonia: dla każdego typu, wybierz z HM lub losowo
        new_sol = []
        for t in required_types:
            if random.random() < HMCR:
                # Wybierz z HM
                idx = random.randint(0, HMS-1)
                if t in [item['type'] for item in HM[idx]]:
                    # Znajdź przedmiot tego typu w HM[idx]
                    for item in HM[idx]:
                        if item['type'] == t:
                            chosen = item
                            break
                else:
                    chosen = random.choice(items_by_type[t]) if t in items_by_type and items_by_type[t] else None
            else:
                chosen = random.choice(items_by_type[t]) if t in items_by_type and items_by_type[t] else None
            if chosen:
                new_sol.append(chosen)
        
        new_fitness = fitness_sol(new_sol)
        # Zastąp najgorsze
        min_idx = HM_fitness.index(min(HM_fitness))
        if new_fitness > HM_fitness[min_idx]:
            HM[min_idx] = new_sol
            HM_fitness[min_idx] = new_fitness
    
    # Zwróć unikalne rozwiązania
    unique = []
    seen = set()
    for sol in HM:
        key = tuple(sorted(item['name'] for item in sol))
        if key not in seen:
            unique.append(sol)
            seen.add(key)
    return unique

def knapsack(items, budget, required_types=None):
    # required_types: lista typów wybranych przez użytkownika
    if required_types is None:
        required_types = list(set(item['type'] for item in items))
    required_types = set(required_types)
    solutions = harmony_search(items, budget, required_types)
    optimal_value = optimal_for_types(items, budget, required_types)
    scored = []
    for sol in solutions:
        # Sprawdź, czy zestaw zawiera dokładnie po jednym z każdego wybranego typu
        types_in_sol = [item['type'] for item in sol]
        # Każdy typ dokładnie raz, tylko te wybrane przez użytkownika
        if sorted(types_in_sol) == sorted(required_types):
            heuristic_value = sum(item['value'] for item in sol)
            total_price = sum(item['price'] for item in sol)
            if optimal_value > 0:
                score = (heuristic_value / optimal_value) * 100
            else:
                score = 0
            if total_price <= budget and sol:
                scored.append((score, sol, total_price))
    scored.sort(reverse=True, key=lambda x: x[0])
    return scored