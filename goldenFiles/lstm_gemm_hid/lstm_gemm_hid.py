import torch
import torch.nn as nn
import sys
sys.path.append("..")
from nnLSTM import LSTM
import os
class NN(nn.Module):
    def __init__(self):
        super(NN, self).__init__()
        self.lstm = LSTM(5,2,1)
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(2, 2),
            nn.ReLU(),
            nn.Linear(2, 3),
            nn.Sigmoid(),
            nn.Linear(3, 3),
            nn.ReLU(),
            nn.Linear(3,1),
            nn.Sigmoid(),
        )

    def forward(self, inp, hidden):
        logits, (hid1, hid2) = self.lstm(inp,hidden) #logits will have shape of hidden_dimension
        sq = hid1.view(-1,hid1.size(2)) #.view reshapes it to a valid (1,hid_dim) for lin layer
        print("*"*50)
        print(sq.shape)
        sq1 = self.linear_relu_stack(sq)
        return sq1

model = NN()
batch_size = 1
seq_len = 2
hidden_dim = 2
input_dim = 5
n_layers = 1
inp = torch.ones(batch_size, seq_len, input_dim)
hidden_state = torch.ones(n_layers, batch_size, hidden_dim)
cell_state = torch.ones(n_layers, batch_size, hidden_dim)
hidden = (hidden_state, cell_state)

def stringer(mat):
    s = ""
    for elem in mat:
        s += str(elem) + " "
    return s.strip()
logits = model(inp, hidden)
with open("lstm_gemm_hid.txt", "w") as f:
    f.write(stringer(list(logits.shape)))
    f.write("\n")
    f.write(stringer(logits.flatten().tolist()))
print(logits.flatten().tolist())

torch.onnx.export(model,               # model being run
                  (inp, hidden),                         # model input (or a tuple for multiple inputs)
                  "lstm_gemm_hid.onnx",   # where to save the model (can be a file or file-like object)
                  export_params=True,        # store the trained parameter weights inside the model file
                  opset_version=10,          # the ONNX version to export the model to
                  do_constant_folding=True,  # whether to execute constant folding for optimization
                  input_names = ['input', 'hidden_state','cell_state'],   # the model's input names
                  output_names = ['output'], # the model's output names
                  )

torch.onnx.export(model,               # model being run
                  (inp, hidden),                         # model input (or a tuple for multiple inputs)
                  "lstm_gemm_hid_weights.onnx",   # where to save the model (can be a file or file-like object)
                  export_params=True,        # store the trained parameter weights inside the model file
                  opset_version=10,          # the ONNX version to export the model to
                  do_constant_folding=False,  # whether to execute constant folding for optimization
                  input_names = ['input', 'hidden_state','cell_state'],   # the model's input names
                  output_names = ['output'], # the model's output names
                  )