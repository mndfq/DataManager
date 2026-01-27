from setuptools import setup, Extension
import pybind11
import os
import sys

# Get the absolute path to the parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Create build directory in parent folder
build_dir = os.path.join(parent_dir, "build")
os.makedirs(build_dir, exist_ok=True)

# Tell setuptools to build in the parent directory
sys.path.insert(0, parent_dir)

ext_modules = [
    Extension(
        "datamanager",
        ["bindings.cpp", "datamanager.cpp"],  # Your C++ files
        include_dirs=[pybind11.get_include(), current_dir],
        language="c++",
        # Build the extension in the build directory
        build_temp=build_dir,
        # Output the compiled module to build directory
        # Use a relative path that's added to sys.path
    )
]

setup(
    name="datamanager",
    version="1.0",
    ext_modules=ext_modules,
    # Configure build directory
    options={
        'build': {'build_base': build_dir},
        'build_ext': {'inplace': False}  # Don't build in-place
    },
)