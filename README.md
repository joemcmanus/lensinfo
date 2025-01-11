# lensinfo.py
LensInfo.py is a python script that reads lens info out of EXIF data to create graphs of the camera, lenses and focal length used. 

Usage is:

    sazed:lensinfo joe$ ./lensinfo.py -h
    usage: lensinfo.py [-h] [--ignore IGNORE] [--file FILE] [--text] [--version] path
    
    lensinfo.py: Command Line EXIF reader and grapher

    positional arguments:
      path             Specify a path to the file or directory to read, directories recurse.

    optional arguments:
      -h, --help       show this help message and exit
      --ignore IGNORE  Comma seperated list of lenses to ignore, --ignore "Olympus 8mm","OLYMPUS M.17mm F1.8"
      --file FILE      filename pattern to look for, --file "L10"
      --text           Print only text
      --version        show program's version number and exit


To read a single file run lensinfo.py fileName

    sazed:2015 joe$ lensinfo.py 12-31_moabride/PC310003.jpg 
    Image  : 12-31_moabride/PC310003.jpg
    Camera : E-M1
    Lens   : OLYMPUS M.8mm F1.8

To read all files in a directory specify the directory name. Note this is recursive, so if you say `directoryA` it will look at sub directories in that folder, `dirA/dir1, dirA/dir2...`.

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
![](https://raw.githubusercontent.com/joemcmanus/lensinfo/refs/heads/master/LensInfo1.jpg)
![](https://raw.githubusercontent.com/joemcmanus/lensinfo/refs/heads/master/LensInfo2.jpg)
![](https://raw.githubusercontent.com/joemcmanus/lensinfo/refs/heads/master/LensInfo3.jpg)

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
![](https://raw.githubusercontent.com/joemcmanus/lensinfo/refs/heads/master/LensInfo1.jpg)





