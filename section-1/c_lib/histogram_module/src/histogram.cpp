#include <Python.h>
#include <numpy/arrayobject.h>
#include <iostream>

#include "opencv_histogram.hpp"

static PyObject *calculateHistogram(PyObject *self, PyObject *args) {
	const char *photoFile;

	if (!PyArg_ParseTuple(args, "s", &photoFile)) {
		return NULL;
	}

	cv::Mat histogram;
	histogram = calculateOpenCVHistogram(photoFile);

	npy_intp dims[1];
	dims[0] = histogram.rows * histogram.cols;

	PyObject *pyArray = PyArray_SimpleNewFromData(1, dims, NPY_FLOAT, reinterpret_cast<void*>(histogram.ptr<float>(0)));
	PyArrayObject *npyArray = reinterpret_cast<PyArrayObject*>(pyArray);

	return PyArray_Return(npyArray);

    }

static PyMethodDef module_methods[] = {
    {"calculate_histogram", calculateHistogram, METH_VARARGS, "Calculate histogram using OpenCV C++"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef histogram_module = {
    PyModuleDef_HEAD_INIT,
    "histogram",
    NULL,
    -1,
    module_methods
};

PyMODINIT_FUNC PyInit_histogram(void) {
    PyObject *module = PyModule_Create(&histogram_module);
    import_array();
    return module;
}


