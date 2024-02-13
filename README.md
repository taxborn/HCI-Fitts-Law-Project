# [Fitts' Law](https://en.wikipedia.org/wiki/Fitts's_law) Experiment

This is the repository and data for a class project (CS 470: Topics in Human Computer Interaction).

# What is Fitts' Law?

> Fitts’ law states that the amount of time required for a person to move a pointer (e.g., mouse cursor) to a target area is a function of the distance to the target divided by the size of the target. Thus, the longer the distance and the smaller the target’s size, the longer it takes.

_Taken from [interaction-design.org](https://www.interaction-design.org/literature/topics/fitts-law)_

# Run the experiment

First, you need to install the dependencies:

```
pip install -r requirements.txt
```

Then, you just need to run the main script:

```
python main.py
```

Alternatively, there is an executable provided. You will need the consent form in the same location to access this.
## The Data
Snippet from the [example](./data/Example%20-%20Fitts%20Law%20Data.csv)
```csv
Distance ,Size ,Direction ,Time               ,Distance Traveled   ,Errors
     300 , 128 ,1         ,1.3636281490325928 , 68.4470598345904   ,     0
     500 , 128 ,1         ,1.9782507419586182 , 57.982756057296896 ,     1
     300 ,  64 ,1         ,0.9403584003448486 , 33.83784863137726  ,     0
     300 , 196 ,1         ,1.4766018390655518 ,123.5556554755791   ,     2
     400 , 256 ,-1        ,0.5160679817199707 ,117.18361660232202  ,     0
...
```
The distance and size (in pixels) columns are each selected from a list of 4 options defined at the top of [main.py](./main.py).
The next option, direction, denotes which side of the screen the button appeared on, **-1 means left, 1 means right**. The distance
traveled is measured by its *Euclidean distance* from the center. Finally, errors is the amount of misclicks before correctly clicking
the button.