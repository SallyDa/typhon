# -*- encoding: utf-8 -*-
import numpy as np
import pytest
import os
import typhon
import scipy as sp

try:
    from typhon.arts.workspace import Workspace, arts_agenda
except:
    skip_arts_tests = True
else:
    skip_arts_tests = False

from typhon.arts.catalogues import Sparse



def agenda(ws):
    ws.Print(ws.y, 0)


@pytest.mark.skipif(skip_arts_tests, reason='ARTS library not available')
class TestWorkspace:
    def setup_method(self):
        """This ensures a new Workspace for every test."""
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.ws  = Workspace()
        self.setup_workspace()

    def setup_workspace(self):
        ws = self.ws
        ws.atmosphere_dim = 1
        ws.p_grid = np.linspace(1e5, 1e3, 21)
        ws.Touch(ws.lat_grid)
        ws.Touch(ws.lon_grid)

        ws.f_grid = 183.0e9 * np.ones(1)
        ws.stokes_dim = 1

        ws.sensor_los = 180.0 * np.ones((1, 1))
        ws.sensor_pos = 830e3 * np.ones((1, 1))
        ws.sensorOff()

    def test_index_transfer(self):
        self.ws.IndexCreate("index_variable")
        i = np.random.randint(0, 100)
        self.ws.index_variable = i
        assert self.ws.index_variable.value == i

    def test_array_of_index_transfer(self):
        self.ws.ArrayOfIndexCreate("array_of_index_variable")
        i = [np.random.randint(0, 100) for j in range(10)]
        self.ws.array_of_index_variable = i
        assert self.ws.array_of_index_variable.value == i

    def test_array_of_vector_transfer(self):
        self.ws.ArrayOfVectorCreate("array_of_vector_variable")
        aov = typhon.arts.xml.load(os.path.join(self.dir,
                                                "xml/reference/arrayofvector.xml"))
        self.ws.array_of_vector_variable = aov
        assert self.ws.array_of_vector_variable.value == aov

    def test_string_transfer(self):
        self.ws.StringCreate("string_variable")
        s = "some random string."
        self.ws.string_variable = s
        assert self.ws.string_variable.value == s

    def test_vector_transfer(self):
        self.ws.VectorCreate("vector_variable")
        v = np.random.rand(10)
        self.ws.vector_variable = v
        assert all(self.ws.vector_variable.value == v)

    def test_matrix_transfer(self):
        self.ws.MatrixCreate("matrix_variable")
        m = np.random.rand(10, 10)
        self.ws.matrix_variable = m
        assert all(self.ws.matrix_variable.value.ravel() == m.ravel())

    def test_sparse_transfer(self):
        sparse_formats = ["csc", "csr", "bsr", "lil", "dok", "coo", "dia"]
        for f in sparse_formats:
            i = sp.sparse.identity(11)
            self.ws.sensor_response = i
            print(self.ws.sensor_response.value)
            assert  np.all(i.todense() == self.ws.sensor_response.value.todense())

    def test_supergeneric_overload_resolution(self):
        self.ws.ArrayOfIndexCreate("array_of_index")
        self.ws.ArrayOfArrayOfIndexCreate("array_of_array_of_index")
        self.ws.array_of_index = [1, 2, 3]
        self.ws.Append(self.ws.array_of_array_of_index, self.ws.array_of_index)
        self.ws.Append(self.ws.array_of_array_of_index, self.ws.array_of_index)

    def test_creation(self):
        self.ws.ArrayOfIndexCreate("array_of_index")
        self.ws.ArrayOfIndexCreate("array_of_index")
        with pytest.raises(Exception):
            self.ws.VectorCreate("array_of_index")

    def test_wsm_error(self):
        with pytest.raises(Exception):
            self.ws.yCalc()

    def test_doc(self):
        repr(self.ws.yCalc)

    def test_agenda(self):
        self.ws.atmosphere_dim = 1
        arts_agenda(agenda)
        assert self.ws.atmosphere_dim.value == 1

    def test_execute_controlfile(self):

        dir = os.path.dirname(os.path.realpath(__file__))
        test_dir = os.path.join(dir, "test_files")
        self.ws.WriteXML("ascii", np.array([1.0]),
                         os.path.join(test_dir, "vector.xml"))
        os.chdir(test_dir)
        self.ws.execute_controlfile("controlfile.arts")

        os.remove(os.path.join(test_dir, "vector.xml"))

    def test_supergeneric_overload_failure(self):
        with pytest.raises(Exception):
            self.ws.NumericCreate("numeric_wsv")
            self.ws.StringCreate("string_wsv")
            self.ws.Copy(self.ws.string_wsv, self.ws.numeric_wsv)

    def test_tensor_3(self):
        t_0 = np.random.rand(*([3] * 3))
        self.ws.Tensor3Create("tensor_3")
        self.ws.tensor_3 = t_0
        assert np.all(t_0 == self.ws.tensor_3.value)

    def test_tensor_4(self):
        t_0 = np.random.rand(*([3] * 4))
        t_1 = self.ws.Tensor4Create("tensor_4")
        self.ws.tensor_4 = t_0
        assert np.all(t_0 == self.ws.tensor_4.value)

    def test_tensor_5(self):
        t_0 = np.random.rand(*([3] * 5))
        t_1 = self.ws.Tensor5Create("tensor_5")
        self.ws.tensor_5 = t_0
        assert np.all(t_0 == self.ws.tensor_5.value)

    def test_tensor_6(self):
        t_0 = np.random.rand(*([3] * 6))
        t_1 = self.ws.Tensor6Create("tensor_6")
        self.ws.tensor_6 = t_0
        assert np.all(t_0 == self.ws.tensor_6.value)

    def test_tensor_7(self):
        t_0 = np.random.rand(*([3] * 7))
        self.ws.Tensor7Create("tensor_7")
        self.ws.tensor_7 = t_0
        assert np.all(t_0 == self.ws.tensor_7.value)

    def test_execute_controlfile(self):

        dir = os.path.dirname(os.path.realpath(__file__))
        test_dir = os.path.join(dir, "test_files")
        self.ws.WriteXML("ascii", np.array([1.0]),
                         os.path.join(test_dir, "vector.xml"))
        os.chdir(test_dir)

        agenda = self.ws.execute_controlfile("controlfile.arts")
        self.ws.foo = "not bar"

        @arts_agenda
        def execute(ws):
            ws.FlagOff(ws.jacobian_do)
            ws.StringSet(ws.foo, "still not bar")
            INCLUDE("controlfile.arts")
            INCLUDE(agenda)

        self.ws.execute_agenda(execute)

        assert self.ws.foo.value == "bar"
        os.remove(os.path.join(test_dir, "vector.xml"))

    def test_covariance_matrix(self):
        ws = self.ws

        ws.jacobianInit()
        ws.jacobianAddAbsSpecies(species = "O3",
                                 g1 = ws.p_grid,
                                 g2 = ws.lat_grid,
                                 g3 = ws.lon_grid)
        ws.jacobianAddAbsSpecies(species = "H2O",
                                 g1 = ws.p_grid,
                                 g2 = ws.lat_grid,
                                 g3 = ws.lon_grid)
        ws.jacobianClose()

        ws.covmatDiagonal(out = ws.covmat_block,
                          out_inverse = ws.covmat_block,
                          vars = np.ones(ws.p_grid.value.size))
        ws.covmat_sxAddBlock(block = ws.covmat_block)
        ws.covmatDiagonal(out = ws.covmat_block,
                          out_inverse = ws.covmat_block,
                          vars = np.ones(ws.p_grid.value.size))
        ws.covmat_sxAddBlock(block = ws.covmat_block)



from IPython import get_ipython
ipython = get_ipython()
ipython.magic("load_ext autoreload")
ipython.magic("autoreload 2")

__file__ = "/home/simonpf/src/typhon/test/arts/test_workspace.py"
t = TestWorkspace()
t.setup_method()
t.test_covariance_matrix()
c = t.ws.covmat_sx.value
