import argparse

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('packages', nargs='+',
                        help='.deb to resolve dependencies for')
    parser.add_argument('--all-deps', action='store_true', type=bool,
                        help='recursively fetch all dependencies (experimental)')

    return parser.parse_args()
