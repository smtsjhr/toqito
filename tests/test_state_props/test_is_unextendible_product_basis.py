"""Test is_unextendible_product_basis."""
import numpy as np

from toqito.state_props.is_unextendible_product_basis import is_unextendible_product_basis

def test_is_unextendible_product_basis_something():
    np.testing.assert_array_equal(True, True)

def test_is_unextendible_product_basis_input_empty_list():
    with np.testing.assert_raises(ValueError):
        empty_list = []
        is_unextendible_product_basis(empty_list)

def test_is_unextendible_product_basis_input_not_numpy_arrays():
    with np.testing.assert_raises(ValueError):
        list_of_listarrays = [[[1, 2], [3, 4]],[[5, 6], [7, 8]] ]
        is_unextendible_product_basis(list_of_listarrays)

def test_is_unextendible_product_basis_input_arrays_not_two_dimensional():
    with np.testing.assert_raises(ValueError):
        array_1D = np.array([1, 2, 3, 4])
        input = [array_1D, array_1D ]
        is_unextendible_product_basis(input)

def test_is_unextendible_product_basis_input_arrays_not_same_num_columns():
    with np.testing.assert_raises(ValueError):
        array_1 = np.array([[1, 2], [3, 4]])
        array_2 = np.array([[1], [3]])
        input = [array_1, array_2]
        is_unextendible_product_basis(input)



if __name__ == "__main__":
    np.testing.run_module_suite()