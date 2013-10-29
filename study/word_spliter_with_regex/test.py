def t(n=500, sum=0):
    if n == 0:
        return sum
    return t(n-1, n+sum)

if __name__ == "__main__":
    t()
