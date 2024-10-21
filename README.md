
**gH - Tiny Bytecode Analyzing Framework**
=============================================

**Overview**
------------

gH is a lightweight, open-source bytecode processing framework designed to provide a simple and efficient way to analyze binary files. Developed by JRDP Team, gH is written in Python and utilizes various libraries to provide a comprehensive set of features for bytecode processing.

**Features**
------------

* **Multi-threaded file loading**: gH uses multiple threads to load binary files, significantly improving performance and reducing loading times.
* **Checksum calculation**: gH calculates various checksums (SHA256, MD5, CRC32, and Whirlpool) for the loaded binary data.
* **File type detection**: gH uses the `magic` library to detect the file type of the loaded binary data.
* **Binary data formatting**: gH formats the binary data into a human-readable format, with options for colorization and ASCII representation.
* **Output file generation**: gH can write the formatted binary data to an output file.
* **Advanced analysis**: gH provides advanced analysis features, including mean, median, standard deviation, entropy, and skewness calculations.

**Usage**
-----

### Command-Line Interface

gH can be used from the command line by running the `gh` script. The following options are available:

* `-c`, `--colorize`: Colorize the output for easier reading.
* `-b`, `--bytes-per-line`: Number of bytes to display per line (default: 16).
* `-t`, `--threads`: Number of threads to use for file loading (default: 5).
* `-o`, `--output-file`: Output file path to write byte data in formatted form.
* `--ASCII`: Show ASCII representation of the bytes.
* `--color-info`: Show color scale information.

### Example Usage

```bash
$ python3 gh.py -c -b 16 -t 5 example.bin
```

This command loads the `example.bin` file using 5 threads, colorizes the output, and displays 16 bytes per line.

### API Documentation

gH provides a Python API for developers who want to integrate its features into their own applications. The API documentation is available in the `docs` directory.

**Requirements**
------------

* Python 3.6+
* `argparse` library
* `colorama` library
* `tqdm` library
* `magic` library
* `numpy` library (for advanced analysis features)
* `scipy` library (for advanced analysis features)

**Installation**
------------

No installation required,just install dependencies,by running this command:

```bash
    $ sudo bash install_dependencies.sh
```

**Contributing**
------------

gH is an open-source project, and contributions are welcome. If you'd like to contribute to gH, please fork the repository and submit a pull request.


**Contact**
-------

If you have any suggestions/questions or need help with gH, please don't hesitate to contact us:

* Contact: [https://jrdpteam.netlify.app](https://jrdpteam.netlify.app)


## gH was developed by JRDP Team.
