# Print the version of Python used in this environment.
import sys
print(sys.version)
import pkg_resources

installed_packages = [(d.project_name, d.version) for d in pkg_resources.working_set]
installed_packages.sort()

for package, version in installed_packages:
    print(f"{package} - {version}")
