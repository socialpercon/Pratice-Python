def t(n=990, sum_=0):
    if n == 0:
        return sum_
    return t(n-1, n+sum_)
t()
