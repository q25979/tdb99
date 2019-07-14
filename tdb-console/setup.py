from distutils.core import setup, Extension
from Cython.Build import cythonize

# setup(
#     name = 'api',
#     ext_modules = cythonize("run.py"),
#     # ext_modules = cythonize("app/model/*.py"),
#     # ext_modules = cythonize("app/api/*.py"),
#     # ext_modules = cythonize("app/api/admin/*.py"),
#     # ext_modules = cythonize("app/api/member/*.py"),
#     # ext_modules = cythonize("app/compensation/*.py"),
# )

# setup(
#     name='console',
#     ext_modules=cythonize("app/*.py"),
# )


setup(
    name='console',
    ext_modules=cythonize("app/views/*.py", compiler_directives={'always_allow_keywords': True}),
)

setup(
    name='console',
    ext_modules=cythonize("app/template_helpers/*.py", compiler_directives={'always_allow_keywords': True}),
)

