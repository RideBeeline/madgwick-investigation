import pathlib

# Export filenames to data files. Useful because they have to be in the matlab directory.
_mat_filters_dir = pathlib.Path(__file__).parent.absolute()

example_data_filename = _mat_filters_dir / "ExampleData.hdf5"
input_data_filename = _mat_filters_dir / "input_data.hdf5"
output_data_filename = _mat_filters_dir / "output_data.hdf5"