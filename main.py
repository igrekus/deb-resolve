import sys

import apt
import apt_pkg

from args import parse_args

if "APT" not in apt_pkg.config:
    apt_pkg.init_config()
apt_pkg.init_system()

apt_pkg.config.set("APT::Install-Recommends", "0")
apt_pkg.config.set("APT::Install-Suggests", "0")


def get_dep_type(dpkg, installed: bool = False):
    if isinstance(dpkg, apt.Package):
        if installed and dpkg.installed:
            return dpkg.installed.dependencies
        if not installed and dpkg.candidate:
            return dpkg.candidate.dependencies
        return []
    return dpkg.dependencies


def get_dep_pkgs(ndep, installed: bool = False):
    target_versions = ndep.installed_target_versions if installed else ndep.target_versions
    return {version.package for version in target_versions}


def recurse_deps(pkgs, levels: int = 1, installed: bool = False) -> set:
    if not pkgs:
        return set()
    total_deps = set()
    for _ in range(levels):
        dep_list = set()
        for dpkg in pkgs:
            dependencies = get_dep_type(dpkg, installed)
            for deps in dependencies:
                if len(deps) > 1:
                    for ndep in deps:
                        dep_list |= get_dep_pkgs(ndep, installed)
                    continue
                dep_list |= get_dep_pkgs(deps[0], installed)
        total_deps |= dep_list
        pkgs = dep_list

    print(
        f"Recurse Levels: {levels}, Recursive List Size: {len(total_deps)}, "
        f"Recurse Type: {'Installed' if installed else 'All Packages'}"
    )
    return total_deps


def main():
    args = parse_args()
    requested_packages = args.packages

    c = apt.Cache()
    packages = [c[name] for name in requested_packages]

    if not args.all_deps:
        for pkg in packages:
            pkg.mark_install()

        res = c.get_changes()

        print('debs to install:')
        for p in res:
            print(p.versions[0])
    else:
        installed_deps = recurse_deps([packages], levels=1, installed=True)
        all_deps = recurse_deps([packages], levels=1, installed=False)

    # print('all', deps_a)
    # print('installed', deps_i)
    # print('diff', set(deps_a) - set(deps_i))

    sys.exit(0)


if __name__ == '__main__':
    main()
