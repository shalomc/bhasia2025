def list_installed_packages():
    try:
        import importlib.metadata
        installed_packages = importlib.metadata.distributions()
    except ImportError:
        installed_packages = []
    packages_list = [(package.metadata['Name'],
                      str(package.version),
                      str(package.metadata['Summary']),
                      str(package._path)
                      )
                      for package in installed_packages]
    packages_list_sorted = [(p00, p01, p02, p03 ) for p00, p01, p02, p03
                in sorted(packages_list, key=lambda y: y[0].lower())]
    return packages_list_sorted

list_installed_packages()
