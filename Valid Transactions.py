def getTransactions(transactionAmount, initialCapital):
    n = len(transactionAmount)
    if n == 0:
        return [-1, -1]
    
    # Build prefix sum array PS of size n + 1
    PS = [0] * (n + 1)
    for i in range(1, n + 1):
        PS[i] = PS[i-1] + transactionAmount[i-1]
        
    # Build Sparse Table for RMQ on PS (1-based indexing for indices 1 to n)
    K = n.bit_length()
    st = [[0] * (n + 1) for _ in range(K)]
    
    for i in range(1, n + 1):
        st[0][i] = PS[i]
        
    for j in range(1, K):
        length = 1 << (j - 1)
        for i in range(1, n - (1 << j) + 2):
            st[j][i] = min(st[j-1][i], st[j-1][i + length])
            
    def query_min(l, r):
        if l > r:
            return float('inf')
        j = (r - l + 1).bit_length() - 1
        return min(st[j][l], st[j][r - (1 << j) + 1])
        
    max_len = 0
    best_L = -1
    
    # Iterate through each possible starting index L
    for L in range(n):
        threshold = PS[L] - initialCapital
        
        # Binary search for the maximum valid R in [L, n-1]
        low, high = L, n - 1
        valid_R = -1
        
        while low <= high:
            mid = (low + high) // 2
            # Check if the minimum prefix sum in the range [L+1, mid+1] meets the threshold
            if query_min(L + 1, mid + 1) >= threshold:
                valid_R = mid
                low = mid + 1
            else:
                high = mid - 1
                
        if valid_R != -1:
            curr_len = valid_R - L + 1
            # Strictly greater length updates the result; ties keep the smaller starting index L
            if curr_len > max_len:
                max_len = curr_len
                best_L = L
                
    if max_len == 0:
        return [-1, -1]
    return [best_L, max_len]