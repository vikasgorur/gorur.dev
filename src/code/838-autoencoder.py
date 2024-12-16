import marimo

__generated_with = "0.9.23"
app = marimo.App(width="medium", css_file="marimo.css")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import torch
    from torch import nn
    from torchviz import make_dot
    return make_dot, mo, nn, np, torch


@app.cell
def __(torch):
    INPUTS = torch.diag(torch.ones(8))
    INPUTS
    return (INPUTS,)


@app.cell
def __(nn):
    from collections import OrderedDict

    class AutoEncoder(nn.Module):
        def __init__(self):
            super().__init__()
            self.stack = nn.Sequential(OrderedDict([
                ('hidden', nn.Linear(8, 3, bias=True)),
                ('output', nn.Linear(3, 8, bias=True)),
                ('sigmoid', nn.Sigmoid())
            ]))

        def forward(self, x):
            return self.stack(x)

        def encode(self, x):
            return self.stack[0](x)
    return AutoEncoder, OrderedDict


@app.cell
def __(AutoEncoder, mo, nn):
    from torchview import draw_graph

    def visualize(model: nn.Module):
        g = draw_graph(model, input_size=(8,)).visual_graph
        g.graph_attr["rankdir"] = 'LR'
        return mo.image(src=g.render())

    visualize(AutoEncoder())
    return draw_graph, visualize


@app.cell
def __(AutoEncoder, INPUTS, nn, torch):
    def train(epochs: int, lr: float, momentum: float):
        model = AutoEncoder()

        loss_fn = nn.MSELoss(reduction='mean')
        sgd = torch.optim.SGD(model.parameters(), lr=lr, momentum=momentum)
        
        prev_loss = 1e9
        loss = 0
        iters = []
        losses = []
        for i in range(epochs):
            x = INPUTS
            yhat = model(x)
            prev_loss = loss
            loss = loss_fn(yhat, x)

            sgd.zero_grad()
            loss.backward()
            sgd.step()

            if i % 5000 == 0:
                print(f"i = {i}, loss: {loss:>7f}")

            iters.append(i)
            losses.append(loss.item())

        return model, iters, losses
    return (train,)


@app.cell
def __(torch, train):
    import matplotlib.pyplot as plt

    torch.manual_seed(42)
    net, iters, losses = train(20000, 0.1, 0.9)
    plt.plot(iters, losses)
    return iters, losses, net, plt


@app.cell
def __(INPUTS, net, np):
    for i in range(8):
        print(np.argmax(net(INPUTS[i]).detach().numpy()))
    return (i,)


@app.cell
def __(INPUTS, net, torch):
    from torch.nn.functional import sigmoid
    torch.set_printoptions(linewidth=120, sci_mode=False)
    net(INPUTS)


    return (sigmoid,)


if __name__ == "__main__":
    app.run()
