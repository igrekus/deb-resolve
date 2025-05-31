import argparse

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('apt packages', nargs='+',
                        help='apt packages to resolve dependencies for')
    parser.add_argument('--all-deps', action='store_true',
                        help='recursively find all dependencies')
    parser.add_argument('--installed', action='store_true',
                        help='find dependencies for an installed package (use with --all-deps)')
    parser.add_argument('--level', type=int, default=1,
                        help='recurse dependency tree up to level')

    args = parser.parse_args()
    if args.installed and not args.all_deps:
        print('use --installed with --all-deps')
        exit(1)

    return args
