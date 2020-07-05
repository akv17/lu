import argparse

from lu.main import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        type=str,
        help='source file'
    )
    parser.add_argument(
        '--r',
        type=int,
        help='number of registers',
        required=False
    )
    parser.add_argument(
        '--m',
        type=int,
        help='memory size',
        required=False
    )
    args = parser.parse_args()
    main(fp=args.f, n_registers=args.r, mem_size=args.m)
