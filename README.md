# GatorSpec_benchtop
Code and files for benchtop UV-Visible spectroscopy setup.
This system consists of a mini Ocean Optics UV-Visible spectrophotometer (STS-UV) and a miniature Hamamatsu xenon flash lamp housed in a 3D-printed enclosure and controlled using a Python script run on a Raspberry Pi.

# Setup
The system was originally developed to be run using a Raspberry Pi model 3B+ with the Raspbian Stretch OS. Later, the system was upgraded to a RPi model 4 with 1 GB of RAM running Raspberry Pi OS.
The system uses a Python library called 'seabreeze' which can be installed on the RPi using pip in the RPi terminal window by typing in the following command:

pip install seabreeze

A C library called 'libusb' is also needed for the RPi to communicate with the spectrophotometer. This can be installed by typing the following command into the RPi terminal:

sudo apt-get install git-all build-essential libusb-dev

After installing seabreeze and libusb, the following command should be typed into the RPi terminal to finish setting up seabreeze:

seabreeze_os_setup

The GatorSpec_benchtop also has a GUI that is created using tkinter, and spectra are displayed using matplotlib with the 'TkAgg' backend. However, the RPi may not have a required library ('ImageTk') pre-installed. To install this library type the following command into the RPi terminal:

sudo apt-get install python3-pil.imagetk

The program also uses several other Python libraries such as NumPy and Pandas which may also need to be installed using pip before the program can run.
