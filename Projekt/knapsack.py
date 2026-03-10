def knapsack(items, budget):

    n = len(items)

    dp = [[0]*(budget+1) for _ in range(n+1)]

    for i in range(1, n+1):

        price = items[i-1]["price"]
        value = items[i-1]["value"]

        for w in range(budget+1):

            if price <= w:

                dp[i][w] = max(
                    value + dp[i-1][w-price],
                    dp[i-1][w]
                )

            else:
                dp[i][w] = dp[i-1][w]

    result = []
    w = budget

    for i in range(n,0,-1):

        if dp[i][w] != dp[i-1][w]:

            result.append(items[i-1])
            w -= items[i-1]["price"]

    return result