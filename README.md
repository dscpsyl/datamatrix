Python3 Data Matrix Reader 
==========

This repository is just a single file built on python data matrix readers and encoders.

Overview
--------

Running this script allows you to read any data matrix using your camera or encode any allowed data into a data matrix using the command line. You can also use this as a module and expand beyong this single script.

Dependencies
------------

- All code is written in Python 3.
- Dependencies are contained in the `dependencies.txt` file
- This script is built upon `OpenCV-2` & `pylibdmtx`
     

Installiation and Usage
--------------------
### Installiation
1. Start by cloning this repository. 
2. The main file is called `pydmatrix.py`
     - **YOU HAVE TO OPEN THIS IN AN ENVORIONMENT THAT HAS PREMISSION TO ACCESS YOUR CAMERA**
3. Navigate to the dependencies file directory.
4. Run `pip3 install -r dependencies.txt`
5. Navigate to the script directory.

### Usage
**Decoding**
1. Run `python3 pydmatrix.py`
2. It will ask you if you want to encode or decode. Select decode.
3. It will ask you if your image needs to be fliped. On some webcams, this will be needed. You can do multiple tests, to see if it is needed.
4. Your computer may ask for you to allow your command line to access to the camera. Select allow.
5. 3 different video feeds should pop up. Left will be the raw video; Center will be the threshold filtered; Right will be the contour detection results.
6. Another window with adjustable sliders will open as well. These control the threshold and countour min & max values. There is also one for area threshold.
7. Hold your data matrix into frame. Check the center feed to make sure all parts are being converted properly. You may need to adjust these values based on lighting. 
8. The data matrix must be detected within frame for 200 consecutive frames.
9. Once that threshold is reached, give it a few seconds to process and the resultign data should be displayed in your command line.

**Encoding**
1. Run `python3 pydmatrix.py`
2. It will ask you if you want to encode or decode. Select encode.
3. It will ask you for the data you wish to encode.
4. Enter your data and press enter.
    - *Data matrix can only encode up to 3116 ASCII characters. Read more [here](https://en.wikipedia.org/wiki/Data_Matrix).*
5. The program will encode and spit out the resulting data matrix image to the root directory of the script.


Module Usage
------------------------
1. `import pydmatrix`
2. To encode, call the function `writtingEncode()`. 
3. To decode, call the function `readingDecode()`.
  - **Currently, because of how the code is setup, it will call the entire process after you choose whether to encode or decode as if you ran this script. You can change it so that it is seperated into more spcialized tasks and whatnot. There are already some within the code that you can explore for yourself.**

Contribution
------------------------
This project is released under the MIT lisence. Anyone can change, add, delete, and alter the code in whatever way the may like. You may create a pull request at any time but spams will be blocked. Rejects and accepts will not be checked on a regular basis. 

Credits
------------------------
[simyoulater](https://twitter.com/SimYouLater28)


**Note:** *This project is unmaintained. You can submit issues and requests. However, they will be resolved at times only convient and available to me.*
