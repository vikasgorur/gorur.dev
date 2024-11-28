import marimo

__generated_with = "0.9.23"
app = marimo.App(width="medium")


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
    def random_onehot(n: int) -> torch.tensor:
        "Returns a random one-hot vector of length n"
        v = torch.zeros(n)
        v[torch.randint(n, ())] = 1
        return v

    random_onehot(8)
    return (random_onehot,)


@app.cell
def __(torch):
    torch.diag(torch.zeros((8, 8)))
    return


@app.cell
def __(torch):
    INPUTS = torch.tensor([1, 0, 0, 0, 0, 0, 0, 0,
                          0, 1, 0, 0, 0, 0, 0, 0,
                          0, 0, 1, 0, 0, 0, 0, 0,
                          0, 0, 0, 1, 0, 0, 0, 0,
                          0, 0, 0, 0, 1, 0, 0, 0,
                          0, 0, 0, 0, 0, 1, 0, 0,
                          0, 0, 0, 0, 0, 0, 1, 0,
                          0, 0, 0, 0, 0, 0, 0, 1], dtype=torch.float32).reshape(8, 8)
    INPUTS.dtype
    return (INPUTS,)


@app.cell
def __():
    return


@app.cell
def __(nn):
    from collections import OrderedDict

    class AutoEncoder(nn.Module):
        def __init__(self):
            super().__init__()
            self.stack = nn.Sequential(OrderedDict([
                ('input', nn.Linear(8, 3)),
                ('sigmoid', nn.Sigmoid()),
                ('hidden', nn.Linear(3, 8)),
                ('sigmoid', nn.Sigmoid())
            ]))

        def forward(self, x):
            return self.stack(x)
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
    def train(epochs: int):
        model = AutoEncoder()
        cross_entropy_loss = nn.CrossEntropyLoss()
        sgd = torch.optim.SGD(model.parameters(), lr=0.001)

        prev_loss = 1e9
        loss = 0
        iters = []
        losses = []
        for i in range(epochs):
            x = INPUTS
            yhat = model(x)
            prev_loss = loss
            loss = cross_entropy_loss(yhat, x)

            loss.backward()
            sgd.step()

            if abs(loss - prev_loss) < 1e-6:
                print(f"i = {i}, loss: {loss:>7f}")
                break

            if i % 100 == 0:
                print(f"i = {i}, loss: {loss:>7f}")

            iters.append(i)
            losses.append(loss.item())

        return model, iters, losses
    return (train,)


@app.cell
def __(INPUTS, nn):
    nn.CrossEntropyLoss()(INPUTS[0], INPUTS[0])
    return


@app.cell
def __(torch, train):
    torch.manual_seed(42)
    net, iters, losses = train(10000)
    return iters, losses, net


@app.cell
def __(iters, losses):
    import matplotlib.pyplot as plt

    plt.plot(iters, losses)
    return (plt,)


@app.cell
def __(INPUTS, net, np):
    for i in range(8):
        print(np.argmax(net(INPUTS[i]).detach().numpy()))
    return (i,)


if __name__ == "__main__":
    app.run()
