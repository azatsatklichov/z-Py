'''
Created on Jan 7, 2018

@author: satklichov


Any code that you write using any compiled language like C, C++, or Java can be integrated or 
imported into another Python script. This code is considered as an "extension."

A Python extension module is nothing more than a normal C library. 
On Unix machines, these libraries usually end in .so (for shared object). 
On Windows machines, you typically see .dll (for dynamically linked library).


On Unix machines, this usually requires installing a developer-specific package such as python2.5-dev.



#include <Python.h>

static PyObject* helloworld(PyObject* self) {
   return Py_BuildValue("s", "Hello, Python extensions!!");
}

static char helloworld_docs[] =
   "helloworld( ): Any message you want to put here!!\n";

static PyMethodDef helloworld_funcs[] = {
   {"helloworld", (PyCFunction)helloworld, 
      METH_NOARGS, helloworld_docs},
      {NULL}
};

void inithelloworld(void) {
   Py_InitModule3("helloworld", helloworld_funcs,
                  "Extension module example!");
}
'''