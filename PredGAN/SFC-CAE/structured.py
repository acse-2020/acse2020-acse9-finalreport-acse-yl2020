from simple_hilbert import *
from advection_block_analytical import *
import space_filling_decomp_new as sfc
import numpy as np  # Numpy
import scipy.sparse.linalg as spl
import scipy.linalg as sl
import scipy.sparse as sp
from utils import *



def load_tensor(data_dir, simulation_indexes):
    '''
    Load simulation tensors by the simulation generated in sfc_cae.advection_block_analytical.py
    ---
    data_dir: [string] the abosolute address of the root dir of the simulation folders
    simulation_indexes: [1d-array] the indices of the simulation number to be loaded.
    ---
    Returns:

    tensor: [torch.floatTensor] the whole tensors of the loaded simulations, of shape[len(simulation_indexes), tuple(shape of each simulation tensor)]
    '''

    total = len(simulation_indexes)
    cnt_progress = 0
    bar=progressbar.ProgressBar(maxval=total)
    tensor = loadsimulation(data_dir, simulaion_steps, simulation_indexes[0])
    cnt_progress+=1
    bar.update(cnt_progress)    
    for i in range(1, total):
        tensor = torch.cat((tensor, loadsimulation(data_dir, simulaion_steps, simulation_indexes[i])))
        cnt_progress+=1
        bar.update(cnt_progress)          
    bar.finish()
    return tensor

def index_split(train_ratio, valid_ratio, test_ratio, total_num = 500):
    '''
    Get random spilting indexes, for train, valid and test set.
    ---
    train_ratio: [float] The ratio of the number of train set.
    valid_ratio: [float] The ratio of the number of valid set.
    test_ratio: [float] The ratio of the number of test set.
    total_num: [int] The total number of the dataset (snapshots)
    ---
    Returns:

    train_index: [1d-array] The indices of the train set, shape of [total_num * train_ratio]
    valid_index: [1d-array] The indices of the valid set, shape of [total_num * valid_ratio]
    test_index: [1d-array] The indices of the test set, shape of [total_num * test_ratio]
    '''

    if train_ratio + valid_ratio + test_ratio != 1:
        raise ValueError("The sum of three input ratios should be 1!")
    total_index = np.arange(1, total_num + 1)
    rng = np.random.default_rng()
    total_index = rng.permutation(total_index)
    knot_1 = int(total_num * train_ratio)
    knot_2 = int(total_num * valid_ratio) + knot_1
    train_index, valid_index, test_index = np.split(total_index, [knot_1, knot_2])
    return train_index, valid_index, test_index



def get_hilbert_curves(size, num):
    '''
    Get the hilbert_curves on a structured square grid of size [size]^ 2.
    ---
    size: [int] the size of the square grid.
    num: [int] the number of space-filling curves want to generate.
    ---
    Returns:

    curve_lists: [list of 1d-arrays] the list of space-filling curve orderings, of shape (number of curves, number of Nodes).
    inv_lists: [list of 1d-arrays] the list of inverse space-filling curve orderings, of shape (number of curves, number of Nodes).
    '''

    Hilbert_index = hilbert_space_filling_curve(size)
    invert_Hilbert_index = np.argsort(Hilbert_index)
    if num == 1: return [Hilbert_index], [invert_Hilbert_index]
    elif num == 2:
        Hilbert_index_2 = Hilbert_index.reshape(size, size).T.flatten()
        invert_Hilbert_index_2 = np.argsort(Hilbert_index_2)
        return [Hilbert_index, Hilbert_index_2], [invert_Hilbert_index, invert_Hilbert_index_2]

def get_MFT_RNN_curves_structured(size, num):
    '''
    Get the MFT_RNN_curves on a structured square grid of size [size]^ 2.
    ---
    size: [int] the size of the square grid.
    num: [int] the number of space-filling curves want to generate.
    ---
    Returns:

    curve_lists: [list of 1d-arrays] the list of space-filling curve orderings, of shape (number of curves, number of Nodes).
    inv_lists: [list of 1d-arrays] the list of inverse space-filling curve orderings, of shape (number of curves, number of Nodes).
    '''

    findm, colm, ncolm  = sparse_square_grid(size)
    curve_lists = []
    inv_lists = []
    ncurve = num
    graph_trim = -10  # has always been set at -10
    starting_node = 0 # =0 do not specifiy a starting node, otherwise, specify the starting node
    whichd, space_filling_curve_numbering = sfc.ncurve_python_subdomain_space_filling_curve(colm, findm, starting_node, graph_trim, ncurve, size**2, ncolm)
    for i in range(space_filling_curve_numbering.shape[-1]):
        curve_lists.append(np.argsort(space_filling_curve_numbering[:,i]))
        inv_lists.append(np.argsort(np.argsort(space_filling_curve_numbering[:,i])))

    return curve_lists, inv_lists

