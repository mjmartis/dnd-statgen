import argparse
import math
import random

STEPS=10000

parser = argparse.ArgumentParser(description='Generate random DnD ability scores.')
parser.add_argument('--num',
                    type=int,
                    default=6,
                    help='The total number of ability scores.')
parser.add_argument('--total',
                    type=int,
                    default=72,
                    help='The total sum of all ability scores.')
parser.add_argument('--max',
                    type=int,
                    default=17,
                    help='The maximum value of any ability score.')
parser.add_argument('--min',
                    type=int,
                    default=7,
                    help='The minimum value of any ability score.')
parser.add_argument('--var',
                    type=float,
                    default=9.0,
                    help='The variance of the ability scores.')

def main():
    args = parser.parse_args()
    print(f'Using:', *[k + '=' + str(v) for k, v in vars(args).items()])

    # Generate inital scores as close as possible to "all average".

    # Start with each score as the average. Since scores are ints,
    # this can leave some of the total unallocated.
    ss = [int(args.total / args.num) for _ in range(args.num)]

    # Randomly allocate remainder.
    for i in random.sample(range(args.num), args.total % args.num):
       ss[i] += 1
       if ss[i] > args.max:
           print(f'Could not achieve total={args.total}')
           exit(1)

    # Twiddle scores until the variance is correct.
    avg = args.total / args.num
    var = sum((s - avg)**2 for s in ss) / args.num
    best_ss = ss.copy()
    best_var = var
    for _ in range(STEPS):
        if math.isclose(best_var, args.var):
            break

        # Choose two scores with the second no less than the first.
        i, j = random.sample(range(args.num), 2)
        if ss[i] > ss[j]:
            i, j = j, i

        # Pull the scores towards each other to decrease variance.
        if var > args.var and ss[i] != ss[j] and ss[i] < args.max and ss[j] > args.min:
            var -= ((ss[i] - avg)**2 + (ss[j] - avg)**2) / args.num
            ss[i] += 1
            ss[j] -= 1
            var += ((ss[i] - avg)**2 + (ss[j] - avg)**2) / args.num
        # Push the scores away from each other to increase variance.
        elif var < args.var and ss[i] > args.min and ss[j] < args.max:
            var -= ((ss[i] - avg)**2 + (ss[j] - avg)**2) / args.num
            ss[i] -= 1
            ss[j] += 1
            var += ((ss[i] - avg)**2 + (ss[j] - avg)**2) / args.num

        # Keep scores with variance closest to requested.
        if abs(var - args.var) < abs(best_var - args.var):
            best_ss = ss.copy()
            best_var = var

    print(f'Result: {" ".join(str(s) for s in sorted(best_ss, reverse=True))}')
    if not math.isclose(best_var, args.var):
        print(f'Actual var={best_var}')

    # Debug print.
    #print(f'Actual total={sum(best_ss)}')
    #print(f'Actual avg={sum(best_ss) / args.num}')
    #print(f'Actual var={sum((s - avg)**2 for s in best_ss) / args.num}')

if __name__ == "__main__":
    main()
