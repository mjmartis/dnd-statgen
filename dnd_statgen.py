import argparse
import math
import random

STEPS=100000

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
                    default=18,
                    help='The maximum value of any ability score.')
parser.add_argument('--min',
                    type=int,
                    default=6,
                    help='The minimum value of any ability score.')
parser.add_argument('--var',
                    type=float,
                    default=9.0,
                    help='The variance of the ability scores.')

def main():
    args = parser.parse_args()
    print('Using:', *[k + '=' + str(v) for k, v in vars(args).items()])

    # Generate inital scores as close as possible to "all average".

    # Start with each score as the average. Since scores are ints,
    # this can leave some of the total unallocated.
    ss = [int(args.total / args.num) for _ in range(args.num)]

    # Randomly allocate remainder.
    if args.total % args.num != 0:
        idxs = list(range(args.num))
        for _ in range(args.num - args.total % args.num):
            del idxs[random.randrange(0, len(idxs))]

        for i in idxs:
            ss[i] += 1
            if ss[i] > args.max:
                print('Could not achieve total =', args.total)
                exit(1)

    # Twiddle scores until the variance is correct.
    avg = args.total / args.num
    var = sum((s - avg)**2 for s in ss) / args.num
    for _ in range(STEPS):
        if math.isclose(var, args.var):
            break

        i, j = [random.randrange(0, args.num) for _ in range(2)]
        if i == j:
            continue
        elif ss[i] > ss[j]:
            i, j = j, i

        # Pull two scores towards each other to decrease variance.
        if var > args.var and ss[i] != ss[j] and ss[i] < args.max and ss[j] > args.min:
            var -= ((ss[i] - avg)**2 + (ss[j] - avg)**2) / args.num
            ss[i] += 1
            ss[j] -= 1
            var += ((ss[i] - avg)**2 + (ss[j] - avg)**2) / args.num
        # Pull two scores away from each other to increase variance.
        elif var < args.var and ss[i] > args.min and ss[j] < args.max:
            var -= ((ss[i] - avg)**2 + (ss[j] - avg)**2) / args.num
            ss[i] -= 1
            ss[j] += 1
            var += ((ss[i] - avg)**2 + (ss[j] - avg)**2) / args.num

    # Allow for the minimum amount of deviation from requested variance.
    if abs(var - args.var) > 1 / args.num:
        print('Could not achieve var =', args.var)
        exit(1)

    print('Result:', ' '.join(str(s) for s in ss))
    if not math.isclose(var, args.var):
        print('Actual var =', var)

    # Debug print.
    #print('Actual total =', sum(ss))
    #print('Actual avg =', sum(ss) / args.num) 
    #print('Actual var =', sum((s - avg)**2 for s in ss) / args.num)

if __name__ == "__main__":
    main()
