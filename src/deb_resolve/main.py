import sys

import apt
import apt_pkg

from .args import parse_args

if "APT" not in apt_pkg.config:
    apt_pkg.init_config()
apt_pkg.init_system()

apt_pkg.config.set("APT::Install-Recommends", "0")
apt_pkg.config.set("APT::Install-Suggests", "0")


def _get_deps(package: apt.Package, installed: bool = False) -> list[apt.package.Dependency]:
    if installed and package.installed:
        return package.installed.dependencies
    if not installed and package.candidate:
        return package.candidate.dependencies
    return []


def _get_dep_packages(dependency, installed: bool = False) -> set[apt.Package]:
    target_versions = dependency.installed_target_versions if installed else dependency.target_versions
    return {version.package for version in target_versions}


def _recurse_deps(packages: list[apt.Package], levels: int = 1, installed: bool = False) -> set[apt.Package]:
    if not packages:
        return set()
    total_deps = set()
    for _ in range(levels):
        dep_list = set()
        for pkg in packages:
            dependencies = _get_deps(pkg, installed)
            for deps in dependencies:
                if len(deps) > 1:
                    for ndep in deps:
                        dep_list |= _get_dep_packages(ndep, installed)
                    continue
                dep_list |= _get_dep_packages(deps[0], installed)
        total_deps |= dep_list
        packages = dep_list

    return total_deps


def main() -> None:
    args = parse_args()
    requested_packages = args.packages

    c = apt.Cache()
    try:
        packages = [c[name] for name in requested_packages]
    except KeyError as ex:
        print(ex)
        sys.exit(2)

    if not args.all_deps:
        for pkg in packages:
            pkg.mark_install()

        changes = c.get_changes()

        if not changes:
            print('all packages are already installed')

        for package in changes:
            print(package.versions[0])

    else:
        all_deps = _recurse_deps(packages, levels=args.level, installed=False)

        for package in all_deps:
            print(' '.join(str(v) for v in package.versions))


if __name__ == '__main__':
    main()
