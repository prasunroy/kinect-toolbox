# Kinect Toolbox
**Kinect data acquisition and visualization toolbox for Windows.**
<img align='right' height='100' src='https://github.com/prasunroy/kinect-toolbox/blob/master/assets/logo.png' />

![badge](https://github.com/prasunroy/kinect-toolbox/blob/master/assets/badge_1.svg)
![badge](https://github.com/prasunroy/kinect-toolbox/blob/master/assets/badge_2.svg)

## Installation
#### Step 1: Setup hardware
<p align='center'>
  <img src='https://github.com/prasunroy/kinect-toolbox/raw/master/assets/image_1.png' />
</p>

>Note: Kinect Toolbox requires second-generation Kinect v2 sensor for data acquisition. For more information on Kinect sensor refer to the [official website](https://developer.microsoft.com/en-us/windows/kinect).

#### Step 2: Install Kinect for Windows SDK 2.0 from the [official website](https://developer.microsoft.com/en-us/windows/kinect)
#### Step 3: Install Python

>Note: Kinect Toolbox is compatible with both [Python 2.7](https://www.python.org/downloads/windows) and [Python 3.5+](https://www.python.org/downloads/windows). However Python 3.5+ is recommended over Python 2.7 for easier installation of dependencies in the following step.

#### Step 4: Install dependencies
```
pip install matplotlib numpy pandas pygame pyqt5
```
```
pip install git+https://github.com/Kinect/PyKinect2.git
```

>Note: For Python 2.7 PyQt5 needs to be configured and built manually from the source.

#### Step 5: Clone repository and launch application
```
git clone https://github.com/prasunroy/kinect-toolbox.git
cd kinect-toolbox
python app.py
```
<p align='center'>
  <img src='https://github.com/prasunroy/kinect-toolbox/raw/master/assets/image_2.png' />
</p>

## References

>[GUI animation](https://github.com/prasunroy/kinect-toolbox/raw/master/assets/anim.gif) is obtained from [Reddit](https://i.redd.it/ounq1mw5kdxy.gif).

>[Git Logo](https://github.com/prasunroy/kinect-toolbox/raw/master/assets/button_repo.png) is designed by [Jason Long](https://github.com/jasonlong) made available under [Creative Commons Attribution 3.0 Unported License](https://creativecommons.org/licenses/by/3.0/deed.en).

## License
MIT License

Copyright (c) 2018 Prasun Roy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

<br />
<br />





**Made with** :heart: **and GitHub**
