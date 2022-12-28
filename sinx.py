def factorial(n:int) -> int:
  if n <= 1:
    return 1
  return n*factorial(n-1)

def sinx(x:float, order:int=9) -> float:
  sinx = 0
  for n in range( int((order+1)/2) ):
    sinx += (-1)**n * x**(2*n+1) / factorial(2*n+1)
  return sinx

if __name__ == '__main__':
  print(sinx(0.5, 7))