DMB Data Manager

A cross-platform data management system with C++ backend and PyQt6 GUI interface. The application provides an intuitive interface for managing structured data stored in .dmb format files.
Overview

This project implements a key-value data management system with section-based organization. The backend is written in C++ for performance, with Python bindings via pybind11, and features a modern PyQt6-based graphical user interface.
Key Features

    Section-based Data Organization: Group related key-value pairs into sections

    Cross-Platform Compatibility: Works on Windows, macOS, and Linux

    Type-Safe Data Access: Built-in type conversion for integers, floats, and booleans

    Multi-line Value Support: Store and edit multi-line text values

    Simple File Format: Human-readable .dmb file format with section headers

Project Structure
text

project/
├── src/
│   ├── datamanager.h          # C++ header file
│   ├── datamanager.cpp        # C++ implementation
│   ├── bindings.cpp           # Python bindings (pybind11)
│   ├── setup.py               # Build configuration
│   └── gui.py                 # PyQt6 GUI application
├── build/                     # Build artifacts (generated)
├── data/                      # Data files directory (generated)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── .gitignore                 # Version control exclusions

Installation
Prerequisites

    Python 3.8 or higher

    C++ compiler (GCC, Clang, or MSVC)

    pip package manager

Dependencies

Install Python dependencies:
bash

pip install -r requirements.txt

Building from Source

    Clone the repository:

bash

git clone <repository-url>
cd dmb-data-manager

    Build the C++ extension module:

bash

cd src
python setup.py build_ext --inplace

Alternatively, install in development mode:
bash

pip install -e ./src

Usage
Running the Application
bash

python src/gui.py

Basic Operations

    Loading Data: Click "Load .dmb" to open an existing .dmb file

    Creating New Sections: Click "Add Section" to create new data sections

    Editing Data: Double-click any cell to edit key or value

    Adding Rows: Within a section, click "Add Row" to create new key-value pairs

    Deleting Data: Use "Delete Selected Row" or "Delete Section" buttons

    Saving Data: Click "Save .dmb" to save changes to file

File Format

The .dmb format uses a simple INI-like structure:
text

[SectionName]
key1=value1
key2=value2
multi_line_key=<<<
Line 1
Line 2
Line 3
>>>

Development
Building the Extension Module

The project uses pybind11 to create Python bindings for the C++ DataManager class. To rebuild:
bash

cd src
python setup.py clean --all
python setup.py build_ext --inplace

Adding New Features

    Backend (C++): Add methods to datamanager.h and implement in datamanager.cpp

    Python Bindings: Update bindings.cpp to expose new methods to Python

    GUI: Modify gui.py to add new UI elements and connect to backend methods

Testing

Manual testing is recommended due to the GUI nature of the application:

    Create, edit, and save .dmb files

    Test all CRUD operations (Create, Read, Update, Delete)

    Verify file persistence across application sessions

Technical Details
Backend Architecture

The DataManager class implements:

    Memory-efficient storage using std::unordered_map

    File I/O with proper error handling

    Type-safe value retrieval with fallback defaults

    Multi-line string support with <<< and >>> delimiters

GUI Features

    Tab-based interface for section management

    Real-time synchronization between UI and backend

    Confirmation dialogs for destructive operations

    Input validation and error reporting

Build System

The project uses:

    setuptools for Python package management

    pybind11 for C++/Python interoperability

    Platform-independent build configuration

File Structure Details
Source Files

    datamanager.h/cpp: Core C++ implementation with data structures and algorithms

    bindings.cpp: Pybind11 wrapper exposing C++ class to Python

    gui.py: Complete PyQt6 application with full CRUD interface

    setup.py: Build configuration with cross-platform support

Generated Directories

    build/: Contains compiled extension modules (created during build)

    data/: Default directory for .dmb files (created on first run)

Contributing

    Ensure code follows existing style and conventions

    Test all changes thoroughly before submitting

    Update documentation as needed

    Maintain backward compatibility with existing .dmb files

Troubleshooting
Common Issues

Module Import Error: Ensure the extension module is built and in Python's path
text

cd src
python setup.py build_ext --inplace

Missing Dependencies: Install required packages:
text

pip install -r requirements.txt

File Permission Errors: Run with appropriate permissions for data directory
Platform-Specific Notes

    Windows: Requires Visual C++ Build Tools or MinGW

    macOS: Requires Xcode Command Line Tools

    Linux: Requires g++ and Python development headers

License

This project is available for academic and personal use. See LICENSE file for details.
Acknowledgments

    PyQt6 team for the GUI framework

    Pybind11 contributors for seamless C++/Python integration

    The C++ Standard Library for robust data structures