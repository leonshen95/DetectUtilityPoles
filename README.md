# DetectUtilityPoles
## 11.28 Updated(finishing labeling, training and testing. Now in the process of combining front end and back end...)

The goal is to download the images based on GPS location followed by:
1. Detecting the poles
2. Detecting all components in the pole (wires, light, boxes, connectors).
3. Measure the height of the pol and the distance between each component.
4. Build a 3D model of the pole.

### Preface

We used MacOS as our developing environment. Things may be subject to change in Windows or other operating systems. 

### Installing and Instruction

- We use **_LabelImg_.py** to annotate our training data. Anotation will be saved in coordinates as txt. You can also see the details [here](https://github.com/tzutalin/labelImg#macos).

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

![Alt text](https://github.com/leonshen95/DetectUtilityPoles/blob/master/YOLO.jpg)

- Our aim is to create .txt-file for each .jpg-image-file - in the same directory and with the same name, but with .txt-extension, and put to file: object number and object coordinates on this image. You can refer [here](https://medium.com/@manivannan_data/how-to-train-yolov2-to-detect-custom-objects-9010df784f36). Your text file should like this:

![Alt text](https://cdn-images-1.medium.com/max/1600/0*DlB8bHOE0E8WzLik.PNG)
-[category number] [object center in X] [object center in Y] [object width in X] [object width in Y]

- Great! We now have a .txt file per image in the training set, telling YOLOv2 where the object we want to detect is at: our data set is completely annotated. Make sure both file types are in the same folder. The below image illustrates how the folder should look like by now:

![Alt text](https://github.com/leonshen95/DetectUtilityPoles/blob/master/annotated_images.jpg?raw=true)

- At this point, we need **_process.py_** to create training set and test set from the images found in the directory where it is run. The percentage of images to be used for test can be defined by changing the variable _percentage_test_. The _path_data_ variable indicates where images are located, which are in the same directory with _darknet.exe_ executable.

- You need to change the dataset path in **line 5**

```
current_dir = '<Your Dataset Path>'
```
- After running the the Python script, you will see something below. For testing purpose, I only used a few images. But for formal training later, you are supposed to have more lines in the images below:
![Alt text](https://github.com/leonshen95/DetectUtilityPoles/blob/master/train_test.jpg?raw=true)

### Prepare YOLO configuration files
- You need to create three files: cfg/obj.data, cfg/obj.names and cfg/yolo-tiny.cfg

- First, start creating the obj.data

```
classes= 1  
train  = train.txt  
valid  = test.txt  
names = obj.names  
backup = backup/
```
- Next create obj.names and every new category should be on a new line, its line number should match the category number in the .txt label files we created earlier.
```
utility poles
```
- A final file we have to prepare (I know, powerful GPU eagerly waiting to start crunching!), is the .cfg file. I just duplicated the yolo-tiny.cfg file, and made the following edits:
```
Line 2: set batch=24, this means we will be using 64 images for every training step
Line 3: set subdivisions=8, the batch will be divided by 8 to decrease GPU VRAM requirements. If you have a powerful GPU with loads of VRAM, this number can be decreased, or batch could be increased. The training step will throw a CUDA out of memory error so you can adjust accordingly.
Line 120: set classes=1, the number of categories we want to detect.
Line 114: set filters=(classes + 5)*5 in our case filters=30.
```
- To start training, YOLOv2 requires a set of convolutional weights. To make things a little easier, Joseph offers a set that was pre-trained on Imagenet. This conv.23 file can be [downloaded](https://pjreddie.com/media/files/darknet19_448.conv.23)(76Mb) from the official YOLOv2 website and provides an excellent starting point. We’ll need this file for the next step.

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
- If you get the following output, then you set up successfully.
```
usage: ./darknet <function>
```
- Now you have the config file for YOLO in the cfg/ subdirectory.Time for the fun part! Enter the following command into your terminal and watch your GPU do what it does best (copy your train.txt and test.txt to yolo_darknet folder):
```
~./darknet detector train cfg/obj.data cfg/yolo-obj.cfg darknet19_448.conv.23
```
-Usually sufficient 2000 iterations for each class(object), but not less than 4000 iterations in total. But for a more precise definition when you should stop training, use the following manual:

1. During training, you will see varying indicators of error, and you should stop when no longer decreases 0.XXXXXXX avg:
```
Region Avg IOU: 0.798363, Class: 0.893232, Obj: 0.700808, No Obj: 0.004567, Avg Recall: 1.000000, count: 8 Region Avg IOU: 0.800677, Class: 0.892181, Obj: 0.701590, No Obj: 0.004574, Avg Recall: 1.000000, count: 8

9002: 0.211667, 0.060730 avg, 0.001000 rate, 3.868000 seconds, 576128 images Loaded: 0.000000 seconds
```
- **9002** - iteration number (number of batch)
- **0.060730 avg** - average loss (error) - the lower, the better
2. Once training is stopped, you should take some of last .weights-files from darknet\build\darknet\x64\backup and choose the best of them.

### Testing 
- Path to the folder where your Darknet.exe locates and type the following command:
```
./darknet detector test data/obj.data yolov3-tiny-obj.cfg backup/yolov3-tiny-obj_10000.weights data/obj/666.jpg -ext_output < data/train.txt > result.txt
```
- The testing data in above case is **data/obj/666.jpg** and you can changing the testing target accordingly. The results will be saved in result.txt. You should see the similar content as follow:
```
data/obj/666.jpg: Predicted in 0.774528 seconds.
utility poles: 69%
```
![Alt text](https://github.com/leonshen95/DetectUtilityPoles/blob/master/predictions%201.jpg?raw=true)
![Alt text](https://github.com/leonshen95/DetectUtilityPoles/blob/master/predictions%202.jpg?raw=true)

### Current status
- We are during the proccess of combining GoogleMap interface and the detection network.

- In GoogleMapApp folder, the files will provide an interface for user to login and select the target coordinates.

- **_examplecode.py_** combines two modules: Getting images from Google Street View API and use the model we trained to see if there is any utility poles. So basically it will take in two types of inputs: 1. the coordinates location used for Google Map; 2. The four corner coordinates of the rectangles that model has detected there is a utility pole.

