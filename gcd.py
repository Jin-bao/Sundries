def gcd(n:int, m:int) -> int:
  while n > 0:
    m, n = n, m%n
  return m