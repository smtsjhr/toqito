"""Test is_unextendible_product_basis."""
import numpy as np
import pytest

from toqito.state_props.is_unextendible_product_basis import is_unextendible_product_basis
from toqito.matrix_ops import tensor
from toqito.matrix_ops import inner_product


tiles_A = np.zeros([3,5])
tiles_A[:, 0] = [1, 0, 0]
tiles_A[:, 1] = [1/np.sqrt(2), -1/np.sqrt(2), 0]
tiles_A[:, 2] = [0, 0, 1]
tiles_A[:, 3] = [0, 1/np.sqrt(2), -1/np.sqrt(2)]
tiles_A[:, 4] = [1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)]

tiles_B = np.zeros([3,5])
tiles_B[:, 0] = [1/np.sqrt(2), -1/np.sqrt(2), 0]
tiles_B[:, 1] = [0, 0, 1]
tiles_B[:, 2] = [0, 1/np.sqrt(2), -1/np.sqrt(2)]
tiles_B[:, 3] = [1, 0, 0]
tiles_B[:, 4] = [1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)]

def GenShifts(parties):
    k = int((parties + 1)/2)
    num_states = 2*k
    upb = [np.zeros([2, num_states]) for _ in range(parties)]
    local_states = [[np.cos(angle), np.sin(angle)] for angle in [(i/k)*np.pi/2 for i in range(2*k - 1, k, -1)] ]
    orth_local_states = [[np.cos(angle), np.sin(angle)] for angle in [(i/k)*np.pi/2 for i in range(1,k)] ]

    state_list = []
    state_list.append([0,1])
    state_list.extend(local_states)
    state_list.extend(orth_local_states)

    for party in upb:
        party[:,0] = [1, 0]

    for state in range(1, num_states):
        for i, party in enumerate(upb):
            party[:,state] = state_list[i]
        state_list = state_list[-1:] + state_list[:-1]

    return upb


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

def test_is_unextendable_product_basis_tiles():
    res = is_unextendible_product_basis([tiles_A, tiles_B])
    expected_res = [True, None]
    np.testing.assert_array_equal(res, expected_res)

@pytest.mark.parametrize("num_states", [1, 2, 3, 4])
def test_is_unextendable_product_basis_tiles_remove_states_false(num_states):
    res = is_unextendible_product_basis([tiles_A[:, 0:num_states], tiles_B[:, 0:num_states]])
    expected_res = False
    np.testing.assert_equal(res[0], expected_res)

@pytest.mark.parametrize("num_states", [1, 2, 3, 4])
def test_is_unextendable_product_basis_tiles_remove_states_orthogonal_witness(num_states):
    witness = is_unextendible_product_basis([tiles_A[:, 0:num_states], tiles_B[:, 0:num_states]])[1]
    witness_product = tensor(witness[0], witness[1])
    ip_list = []
    for i in range(num_states):
        UPB_product = tensor(np.array([tiles_A[:, i]]).T, np.array([tiles_B[:, i]]).T)
        ip = inner_product(witness_product[:,0], UPB_product[:, 0])
        ip_list.append(ip)
    expected_res = [0]*num_states
    np.testing.assert_array_almost_equal(ip, expected_res)

@pytest.mark.parametrize("num_parties", [3, 5, 7])
def test_is_unextendable_product_basis_tiles_GenShifts(num_parties):
    res = is_unextendible_product_basis(GenShifts(num_parties))
    expected_res = [True, None]
    np.testing.assert_array_equal(res, expected_res)


if __name__ == "__main__":
    np.testing.run_module_suite()