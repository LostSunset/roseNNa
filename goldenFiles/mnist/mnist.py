import torch
import torch.nn as nn
import torch.onnx
import onnx
from onnx import numpy_helper
import onnxruntime as ort
import numpy as np
import time

inp = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.121568635, 0.5176471, 0.9960785, 0.9921569, 0.9960785, 0.8352942, 0.32156864, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.08235294, 0.5568628, 0.91372555, 0.98823535, 0.9921569, 0.98823535, 0.9921569, 0.98823535, 0.8745099, 0.078431375, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.48235297, 0.9960785, 0.9921569, 0.9960785, 0.9921569, 0.87843144, 0.7960785, 0.7960785, 0.8745099, 1.0, 0.8352942, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7960785, 0.9921569, 0.98823535, 0.9921569, 0.8313726, 0.078431375, 0.0, 0.0, 0.2392157, 0.9921569, 0.98823535, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16078432, 0.95294124, 0.87843144, 0.7960785, 0.7176471, 0.16078432, 0.59607846, 0.11764707, 0.0, 0.0, 1.0, 0.9921569, 0.40000004, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.15686275, 0.078431375, 0.0, 0.0, 0.40000004, 0.9921569, 0.19607845, 0.0, 0.32156864, 0.9921569, 0.98823535, 0.078431375, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.32156864, 0.83921576, 0.121568635, 0.4431373, 0.91372555, 0.9960785, 0.91372555, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.24313727, 0.40000004, 0.32156864, 0.16078432, 0.9921569, 0.909804, 0.9921569, 0.98823535, 0.91372555, 0.19607845, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.59607846, 0.9921569, 0.9960785, 0.9921569, 0.9960785, 0.9921569, 0.9960785, 0.91372555, 0.48235297, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.59607846, 0.98823535, 0.9921569, 0.98823535, 0.9921569, 0.98823535, 0.75294125, 0.19607845, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.24313727, 0.7176471, 0.7960785, 0.95294124, 0.9960785, 0.9921569, 0.24313727, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.15686275, 0.6745098, 0.98823535, 0.7960785, 0.078431375, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.08235294, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7176471, 0.9960785, 0.43921572, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.24313727, 0.7960785, 0.6392157, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2392157, 0.9921569, 0.5921569, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.08235294, 0.83921576, 0.75294125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.043137256, 0.8352942, 0.9960785, 0.5921569, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.40000004, 0.9921569, 0.5921569, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16078432, 0.8352942, 0.98823535, 0.9921569, 0.43529415, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.16078432, 1.0, 0.8352942, 0.36078432, 0.20000002, 0.0, 0.0, 0.121568635, 0.36078432, 0.6784314, 0.9921569, 0.9960785, 0.9921569, 0.5568628, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6745098, 0.98823535, 0.9921569, 0.98823535, 0.7960785, 0.7960785, 0.91372555, 0.98823535, 0.9921569, 0.98823535, 0.9921569, 0.50980395, 0.078431375, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.08235294, 0.7960785, 1.0, 0.9921569, 0.9960785, 0.9921569, 0.9960785, 0.9921569, 0.9568628, 0.7960785, 0.32156864, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.078431375, 0.5921569, 0.5921569, 0.9921569, 0.67058825, 0.5921569, 0.5921569, 0.15686275, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]).astype(np.float32)
inp = np.reshape(inp, (1,1,28,28))

ort_sess = ort.InferenceSession('goldenFiles/mnist/mnist.onnx')


print("starting...")
start = time.time()
logits = ort_sess.run(None, {'Input3': inp})[0]
print(time.time() - start)
with open("inputs.fpp",'w') as f1:
    inputs = inp.flatten().tolist()
    inpShapeDict = {'inputs': list(inp.shape)}
    inpDict = {'inputs':inputs}
    f1.write(f"""#:set inpShape = {inpShapeDict}""")
    f1.write("\n")
    f1.write(f"""#:set arrs = {inpDict}""")
    f1.write("\n")
    f1.write("a")

def stringer(mat):
    s = ""
    for elem in mat:
        s += str(elem) + " "
    return s.strip()


filePath = "goldenFiles/mnist/"
with open(filePath+"mnist.txt", "w") as f2:
    f2.write(stringer(list(logits.shape)))
    f2.write("\n")
    f2.write(stringer(logits.flatten().tolist()))
print(logits.flatten().tolist())

onnx.shape_inference.infer_shapes_path('goldenFiles/mnist/mnist.onnx', 'goldenFiles/mnist/mnist_inferred.onnx')
print("done")