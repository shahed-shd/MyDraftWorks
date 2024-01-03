import ctypes

# Load the shared library
libsharedutils = ctypes.CDLL('./libsharedutils.so')

# Define the argument types and return type of the add function
libsharedutils.add.argtypes = [ctypes.c_int32, ctypes.c_int32]
libsharedutils.add.restype = ctypes.c_int32

libsharedutils.multiply.argtypes = [ctypes.c_int32, ctypes.c_int32]
libsharedutils.multiply.restype = ctypes.c_int32

# Call the add function
a, b = 2, 3
sum = libsharedutils.add(a, b)
product = libsharedutils.multiply(a, b)
print(f"sum: {sum}\nproduct: {product}")
