# lensinfo.py
LensInfo.py is a python script that reads lens info out of EXIF data to create graphs of the camera, lenses and focal length used. 

Usage is:

    sazed:lensinfo joe$ ./lensinfo.py -h
    usage: lensinfo.py [-h] [--ignore IGNORE] [--text] [--version] path
        
    lensinfo.py: Command Line EXIF reader and grapher
    
    positional arguments:
    path             Specify a path to the file or directory to read,
                     directories will recurse.
    
    optional arguments:
      -h, --help       show this help message and exit
      --ignore IGNORE  Comma separated list of lenses to ignore, --ignore "Olympus
                       8mm","OLYMPUS M.17mm F1.8"
      --text           Print only text
      --version        show program's version number and exit


To read a single file run lensinfo.py fileName

    sazed:2015 joe$ lensinfo.py 12-31_moabride/PC310003.jpg 
    Image  : 12-31_moabride/PC310003.jpg
    Camera : E-M1
    Lens   : OLYMPUS M.8mm F1.8

To read all files in a directory specify the directory name. 

    sazed:2015 joe$ lensinfo.py 12-31_moabride
    +------------------------+-------+
    |          Lens          | Count |
    +------------------------+-------+
    |   OLYMPUS M.8mm F1.8   |   16  |
    | OLYMPUS M.12-40mm F2.8 |   7   |
    +------------------------+-------+
    +------+-------+
    | Body | Count |
    +------+-------+
    | E-M1 |   23  |
    +------+-------+

This the following creates graphs. 

![](https://lh3.googleusercontent.com/-vVvPaGukrCo/VU2TyUUjphI/AAAAAAAAV7Q/e4v1iJu3D_E/s800/lenses2015.png)
![](https://lh3.googleusercontent.com/-Qo7SXNjOWK4/VYZMHpBnbyI/AAAAAAAAWcM/qjTLr_Tu-QY/s800/picBubble.jpg)
![](https://lh3.googleusercontent.com/-JCg5mRFEniQ/VYZMHpkUTzI/AAAAAAAAWcI/xuhxEczOi1s/s800/picCamera.jpg)
![](https://lh3.googleusercontent.com/-GHSasomLWv4/VzspyiTMQmI/AAAAAAAAZp0/GZrySeA432s7OXSdgHAv54ca6AJTMCQEQCCo/s800/fstop.png)

To print text only output add --text

    sazed:2015 joe$ lensinfo.py 12-31_moabride --text

To ignore a specific lens, type the exact name of the lens enclosed in quotes and separated by commas. 

     sazed:2015 joe$./lensinfo.py --ignore "Panasonic 14mm F2.5","OLYMPUS M.12mm F2.0","OLYMPUS M.17mm F1.8","OLYMPUS M.75-300mm F4.8-6.7 II"
    ~/Desktop/pics/2015 

    --ignore specified, skipping the following lenses: 
    Panasonic 14mm F2.5
    OLYMPUS M.12mm F2.0
    OLYMPUS M.17mm F1.8
    OLYMPUS M.75-300mm F4.8-6.7 II
   
    +---------------------------+-------+
    |            Lens           | Count |
    +---------------------------+-------+
    |   OLYMPUS M.12-40mm F2.8  |  1801 |
    |   OLYMPUS M.7-14mm F2.8   |  765  |
    | OLYMPUS M.9-18mm F4.0-5.6 |  456  |
    |     OLYMPUS M.8mm F1.8    |  231  |
    |  OLYMPUS M.40-150mm F2.8  |  192  |
    |  M.40-150mm F2.8 + MC-14  |  189  |
    |    OLYMPUS M.25mm F1.8    |  163  |
    |    OLYMPUS M.75mm F1.8    |  158  |
    | OLYMPUS M.60mm F2.8 Macro |   99  |
    +---------------------------+-------+
    +------+-------+
    | Body | Count |
    +------+-------+
    | E-M1 |  3146 |
    | E-M5 |  908  |
    +------+-------+
    Skipped 330 photos from ignore list.
![](https://lh3.googleusercontent.com/-z68HCLa_Y1Y/VoXl98FAIpI/AAAAAAAAYes/qj5jvZ6p5Ps/s800-Ic42/PicByLens2015.png)
![](https://lh3.googleusercontent.com/-kmoHcnnmwf4/VoXl9piQb1I/AAAAAAAAYeo/xwbObjT21gM/s800-Ic42/PicByFocalLength2015.png)

Requires matplotlib, scipy, prettytable & exifread. I would just use pip to install them all... or download, whatever floats your boat. 

Scipy : http://www.scipy.org/install.html

Exifread: https://pypi.python.org/pypi/ExifRead

Matplotlib: http://matplotlib.org/

PrettyTable: https://github.com/dprince/python-prettytable




