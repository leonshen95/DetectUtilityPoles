# DetectUtilityPoles
## 10.28 Updated(finishing labeling, and in the process of training annotated images...)

The goal is to download the images based on GPS location followed by:
1. Detecting the poles
2. Detecting all components in the pole (wires, light, boxes, connectors).
3. Measure the height of the pol and the distance between each component.
4. Build a 3D model of the pole.

## Preface

We used MacOS as my developing environment. Things may be subject to change in Windows or other operating systems. 

### Installing and Instruction

- We use **_LabelImg_.py** to annotate our training data. Anotation will be saved in coordinates as txt. You can also see the details [here](https://github.com/tzutalin/labelImg#macos).

Here is an idea about how it works eventually.

![Alt text](https://raw.githubusercontent.com/tzutalin/labelImg/master/demo/demo3.jpg)

Type the following command to make sure you meet the requirements.

```
brew install python3
pip install pipenv
pipenv --three
pipenv shell
pip install py2app
pip install PyQt5 lxml
make qt5py3
rm -rf build dist
python setup.py py2app -A
mv "dist/labelImg.app" /Applications
```
- And finally you can run the **_LabelImg_.py** by open the directory and type:
```
python LabelImg.py
```

- Then follow the steps below:


### Steps (YOLO)
- In data/predefined_classes.txt define the list of classes that will be used for your training. In my case, I just defined **utility poles**.
- Build and launch using the instructions above.
- Right below "Save" button in toolbar, click "PascalVOC" button to switch to YOLO format.
- You may use Open/OpenDIR to process single or multiple images. When finished with single image, click save.
- A txt file of yolo format will be saved in the same folder as your image with same name. A file named "classes.txt" is saved to that folder too. "classes.txt" defines the list of class names that your yolo label refers to.

Note:

- Your label list shall not change in the middle of processing a list of images. When you save a image, classes.txt will also get updated, while previous annotations will not be updated.
- You shouldn't use "default class" function when saving to YOLO format, it will not be referred.
- When saving as YOLO format, "difficult" flag is discarded.

![Alt text](https://github.com/leonshen95/DetectUtilityPoles/blob/master/YOLO.jpg?raw=true)

### Training

- As we mentioned before, we are going to use YOLO(You only look once) to detect our poles.

- But first, you need to install Darknet. You can also refer [here](https://github.com/tzutalin/labelImg#macos):
```
git clone https://github.com/pjreddie/darknet.git
cd darknet
make
```
- If this works you should see a whole bunch of compiling information such as:
```mkdir -p obj
gcc -I/usr/local/cuda/include/  -Wall -Wfatal-errors  -Ofast....
gcc -I/usr/local/cuda/include/  -Wall -Wfatal-errors  -Ofast....
gcc -I/usr/local/cuda/include/  -Wall -Wfatal-errors  -Ofast....
.....
gcc -I/usr/local/cuda/include/  -Wall -Wfatal-errors  -Ofast -lm....
```
- If you have any errors, try to fix them? If everything seems to have compiled correctly, try running it!
```
./darknet
```
If you get the following output, then you set up successfully.
```
usage: ./darknet <function>
```
