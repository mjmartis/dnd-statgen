import random
import sys

SIM_COUNT = 1000000

def d(ma, mi=1): return max(random.randint(1, ma), mi)
# Use the following to reroll instead of using a floor:
#def d(ma, mi=1): return random.randint(mi, ma)

def roll3d6(): return d(6) + d(6) + d(6)

def roll2d6plus6(): return 6 + d(6) + d(6)

def roll4d6kh3(): return sum(sorted(d(6) for _ in range(4))[1:])

def roll4d6kh3m2(): return sum(sorted(d(6, 2) for _ in range(4))[1:])

def rolldyn(mi, ma, n):
  d1, d2 = [sum(d(ma, mi) for _ in range(n)) for _ in range(2)]
  return 12 + d1 - d2

MS = {
  '3d6': roll3d6,
  '4d6kh3': roll4d6kh3,
  '2d6+6': roll2d6plus6,
  '4d6kh3m2': roll4d6kh3m2,
  'dyn1d6': lambda: rolldyn(1, 6, 1),
  'dyn2d4': lambda: rolldyn(1, 4, 2),
  'dyn1d8': lambda: rolldyn(1, 8, 1),
  'dyn1d8m2': lambda: rolldyn(2, 8, 1),
}

if len(sys.argv) != 2 or sys.argv[1] not in MS:
  print(f'Usage: {sys.argv[0]} mode')
  print(f'mode must be one of: {", ".join(MS.keys())}')
  exit(1)

m = MS[sys.argv[1]]
rs = {}
for _ in range(SIM_COUNT):
  r = m()
  rs[r] = rs.get(r, 0) + 1

count = float(SIM_COUNT)
mean = sum(n * fq for n, fq in rs.items()) / count
var = sum((n - mean)**2 * fq for n, fq in rs.items()) / count
stddev = var**0.5

print('Rolls:')
for n, fq in sorted(rs.items()):
    print(f'  {n:<2}: {fq / count:.2%}')
print(f'Mean: {mean:0.2f}')
print(f'Std dev: {stddev:0.2f}')
