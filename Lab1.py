def coins(n, a, b, c):
    if n == 0:
        return 0
    if n < 0:
        return float('inf')
    
    use_all_copper = n
    use_silver = coins(n - a, a, b, c)
    use_gold = coins(n - b, a, b, c)
    use_platinum = coins(n - c, a, b, c)
    
    return min(use_all_copper, 1 + use_silver, 1 + use_gold, 1 + use_platinum)

def coins_memoized(n, a, b, c, memo): # memoized recursive implementation
    if n == 0:
        return 0
    if n < 0:
        return float('inf')
    
    if n in memo:
        return memo[n]
    
    use_copper = coins_memoized(n - 1, a, b, c, memo)
    use_silver = coins_memoized(n - a, a, b, c, memo)
    use_gold = coins_memoized(n - b, a, b, c, memo)
    use_platinum = coins_memoized(n - c, a, b, c, memo)
    
    result = min(use_copper, use_silver, use_gold, use_platinum) + 1
    memo[n] = result
    return result

def coin_change(n, a, b, c): # bottom-up implementation
    dp = [float('inf')] * (n + 1) # initialize array with infinity
    dp[0] = 0 # base case as 0 coins needed to make for 0
    
    for i in range(1, n + 1):
        dp[i] = min(dp[i], dp[i - 1] + 1)
        if i >= a:
            dp[i] = min(dp[i], dp[i - a] + 1)
        if i >= b:
            dp[i] = min(dp[i], dp[i - b] + 1)
        if i >= c:
            dp[i] = min(dp[i], dp[i - c] + 1)
    
    return dp[n]

def f(x, y, k, p, memo):
    if y == 0: # need 0 more consecutive wins, we've already achieved the streak
        return 1.0
    if x == 0: # if we have 0 games left and still need y > 0 wins, it's impossible
        return 0.0
    
    if (x, y) in memo:
        return memo[(x, y)]
    
    win_outcome = p * f(x - 1, y - 1, k, p, memo)
    lose_outcome = (1 - p) * f(x - 1, k, k, p, memo) # our current streak is broken, need to start over, needing k consecutive wins again
    
    result = win_outcome + lose_outcome # total probability is the sum of probabilities from both scenarios, addition only one will happen
    memo[(x, y)] = result 
    return result

def g(x, k, p, memo):
    if x < k: # if we've played fewer than k games, it's impossible to have a k streak yet
        return 0.0 
    if x == k: # if we've played k games, the only way to have achieved a k streak is to have won all k games
        return p ** k
    
    if x in memo:
        return memo[x]
    
    already_achieved = g(x - 1, k, p, memo) # already had it by game x-1 so game x doesn't matter anymore
    # first time ending at game x, requires three conditions
    prob_not_achieved_before = 1.0 - g(x - k - 1, k, p, memo) # didn't get it in games 1 to (x-k-1), ensures it's first time
    first_time_now = (p ** k) * (1 - p) * prob_not_achieved_before # win games (x-k+1) to x * lose game (x-k) * above condition
    
    result = already_achieved + first_time_now
    memo[x] = result
    return result
