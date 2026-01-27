#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "datamanager.h"

namespace py = pybind11;

PYBIND11_MODULE(datamanager, m) {
    py::class_<DataManager>(m, "DataManager")
        .def(py::init<>())
        .def("load", &DataManager::load)
        .def("save", &DataManager::save)
        .def("setValue", &DataManager::setValue)
        .def("getValue", &DataManager::getValue,
             py::arg("section"), py::arg("key"), py::arg("defaultValue")="")
        .def("removeKey", &DataManager::removeKey)
        .def("removeSection", &DataManager::removeSection)
        .def("keyExists", &DataManager::keyExists)
        .def("sectionExists", &DataManager::sectionExists)
        .def("getInt", &DataManager::getInt,
            py::arg("section"), py::arg("key"), py::arg("defaultValue") = 0)
        .def("getFloat", &DataManager::getFloat,
            py::arg("section"), py::arg("key"), py::arg("defaultValue") = 0.0f)
        .def("getBool", &DataManager::getBool,
            py::arg("section"), py::arg("key"), py::arg("defaultValue") = false)
        .def("listSections", &DataManager::listSections)
        .def("listKeys", &DataManager::listKeys)
        .def("clearSection", &DataManager::clearSection)
        .def("clearAll", &DataManager::clearAll);
}
