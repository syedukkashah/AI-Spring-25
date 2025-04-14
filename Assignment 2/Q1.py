#explanation is commented
def find_peak(N: int) -> int:
    if N==0: #handles edge case (if N=0, only possible idx is 0 so peak must be = 0)
        return 0

    x = N//2 #init starting pos to middle to reduce num of steps
    while True: #infinite loop until peak is found
        current = query(x) #queries elevation at current pos x

        left = query(x-1) if x> 0 else float('-inf') #float(-inf) is used for non-existent neighbors to avoid querying invalid indices
        right = query(x+1) if x<N else float('-inf')

        if current >= left and current >= right:
            return x

        if left > current: #moves left if left neighbor has higher elevation
            x-=1
        elif right > current: #moves right if right neighbor has higher elevation
            x+=1

