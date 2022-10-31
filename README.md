# FyeNNa
A neural network model to Fortran and C translator (FyeNNa and CyeNNa?)

To run current tests located in [goldenFiles](https://github.com/comp-physics/FyeNNa/tree/develop/goldenFiles), change permissions for [run.sh](https://github.com/comp-physics/FyeNNa/blob/develop/run.sh). Each time the tests are run, new weights are initialized for the given test's model. To look at the model architectures of each test, go to the same **goldenFiles** folder, view each test's folder, and go to the .py file.

## Methodology
First, all the core files are compiled (activation_funcs.f90, derived_types.f90, layers.f90, readTester.f90). activation_funcs.f90 stores activation functions, derived_types.f90 stores derived types for certain layer types, layers.f90 stores the math behind certain layers (**currently we support GEMM, LSTM, Convolutional, and MaxPool layers**), and readTester.f90 loads in the weights that are stored in the system itself.

### Initialization and Preprocessing
Then, in each of the test case files in [goldenFiles](https://github.com/comp-physics/FyeNNa/tree/develop/goldenFiles), the **.py** file is run to create the model, randomly initialized with weights. It creates an intermediary file called inputs.fpp, which stores the exact inputs given to the model, which is later fed to the fortran built model. It also creates a "golden file" which represents the correct shape and output of the model. Lastly, the model that was run is stored in **.onnx** format.

[modelParserONNX.py](https://github.com/comp-physics/FyeNNa/blob/develop/modelParserONNX.py) is run to parse the onnx model and gathers information about the model and creates [onnxModel.txt](https://github.com/comp-physics/FyeNNa/blob/develop/onnxModel.txt) (layer names and weights dimensions) and [onnxWeights.txt](https://github.com/comp-physics/FyeNNa/blob/develop/onnxWeights.txt) (the corresponding weights for each layer). It also creates a [variables.fpp](https://github.com/comp-physics/FyeNNa/blob/develop/variables.fpp) file that stores some key information about the model that fypp will process during model creation.

### Running and Testing
Lastly, we have two **.fpp** files. [modelCreator.fpp](https://github.com/comp-physics/FyeNNa/blob/develop/modelCreator.fpp) is the module that builds the subroutine that stores the correct model architecture. It parses through [variables.fpp](https://github.com/comp-physics/FyeNNa/blob/develop/variables.fpp) and reconstructs the model with the subroutines in **layers.f90**. [userTesting.fpp](https://github.com/comp-physics/FyeNNa/blob/develop/userTesting.fpp) is used to create **userTesting.f90**, a sample file that calls "**initialize**" (which enables fortran to read in the weights and model structure from [onnxModel.txt](https://github.com/comp-physics/FyeNNa/blob/develop/onnxModel.txt) and [onnxWeights.txt](https://github.com/comp-physics/FyeNNa/blob/develop/onnxWeights.txt). Then it passes in the inputs from the intermediary file inputs.fpp, and runs the model. [userTesting.fpp](https://github.com/comp-physics/FyeNNa/blob/develop/userTesting.fpp) then stores the shape and output in a text file.


[testChecker.py](https://github.com/comp-physics/FyeNNa/blob/develop/goldenFiles/testChecker.py) compares the outputted text file to the test's "golden file". If the shapes match and the outputs are within reasonable range, the test case passes. Otherwise, the error is outputted.


## Fortran Library
The fLibrary folder holds all the core files that are needed to recreate the model in Fortran and be linked to a program. It contains a Makefile that compiles all core files and creates a library. 

Here are the steps one needs to follow. First preprocess the model down below. This customizes the modelCreator.f90 file to the model that is currently being used/preprocessed.

```make
    preprocess: modelParserONNX.py
        # arg1 = model structure file (.onnx format)
        # arg2 (optional) = weights file (.onnx format)
        python3 modelParserONNX.py $(arg1) $(arg2)

        #create the model based on modelParserONNX
        fypp modelCreator.fpp modelCreator.f90
```
Then, run "make library" to compile all the core files and create a library called "libcorelib.a". This file must be used to link any other "*.o" files in the program with the library. 

### User Example

``` fortran
    program name
        
        !must be imported
        USE rosenna
        implicit none
        
        !user has to provide inputs to the model
        REAL, DIMENSION(1,1,28,28) :: inputs
        REAL, DIMENSION(1,5) :: Plus214_Output_0
        
        !this must be called somewhere to read all the weights in
        CALL initialize()
        
        ! this must be called to run inference on the model
        CALL use_model(inputs, Plus214_Output_0)

        print *, Plus214_Output_0
    end program name
```
This represents a sample program that can be linked with the library created above and run succesfully (given the model's inputs match the inputs provided). Four things are required to use this library: **USE rosenna**, **initializing inputs**, **CALL initialize()**, and **CALL use_model(args)**.

## C Library
Need to Update


# Open Source Development

## Adding activation functions, layer functionality, and more

### Parsing in modelParserONNX.py

### Reading layer in reader.f90

### Adding Layer

### Adding activation function

### Fypp to call the layer/activation function
