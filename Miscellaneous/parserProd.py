import torch
import torch.nn as nn
from lstm_linear import NN
from nntester import NeuralNetwork
import time
import itertools

# model = NeuralNetwork()
model = NN()
torch.save(model.state_dict(),"nntester4.pt")

# torch.save(model.state_dict(),"nntester2.pt")
batch_size = 1
seq_len = 2
hidden_dim = 2
input_dim = 5
n_layers = 1
inp = torch.ones(batch_size, seq_len, input_dim)
# inp = torch.ones(1,2)
# inp = torch.ones(1,2,3,3)
hidden_state = torch.ones(n_layers, batch_size, hidden_dim)
cell_state = torch.ones(n_layers, batch_size, hidden_dim)
hidden = (hidden_state, cell_state)
# X = torch.ones(1,2)
a = time.time()
# logits = model(X)
logits = model(inp, hidden) #hidden

# torch.onnx.export(model,               # model being run
#                   (inp, hidden),                         # model input (or a tuple for multiple inputs)
#                   "nn_lstm.onnx",   # where to save the model (can be a file or file-like object)
#                   export_params=True,        # store the trained parameter weights inside the model file
#                   opset_version=10,          # the ONNX version to export the model to
#                   do_constant_folding=True,  # whether to execute constant folding for optimization
#                   input_names = ['input'],   # the model's input names
#                   output_names = ['output'], # the model's output names
#                   )
print(f"Time taken: {time.time()-a}")
print(logits)
print("*"*30)
listToParse = []
for l in model.state_dict():
    print(model.state_dict()[l])
    reaList = model.state_dict()[l]
    shape = list(model.state_dict()[l].shape)
    combs = []
    #for F90, we must find transpose all combinations of dimensions
    for x in range(len(shape)):
        combs.append(x)
    for dim1,dim2 in itertools.combinations(combs,2):
        reaList = torch.transpose(reaList,dim1,dim2)
    listToParse.append((shape,reaList.flatten().tolist()))

def stringer(mat, dim):
    s = ""
    for elem in mat:
        s += str(elem) + " "
    return s.strip()


with open('weights_biases3.txt', 'w') as f:
    for shape, mat in listToParse:
        f.write(stringer(mat,len(shape)))
        f.write('\n')