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
    INPUTS = torch.tensor([.9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                          0.1, .9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                          0.1, 0.1, .9, 0.1, 0.1, 0.1, 0.1, 0.1,
                          0.1, 0.1, 0.1, .9, 0.1, 0.1, 0.1, 0.1,
                          0.1, 0.1, 0.1, 0.1, .9, 0.1, 0.1, 0.1,
                          0.1, 0.1, 0.1, 0.1, 0.1, .9, 0.1, 0.1,
                          0.1, 0.1, 0.1, 0.1, 0.1, 0.1, .9, 0.1,
                          0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, .9], dtype=torch.float32).reshape(8, 8)
    INPUTS.dtype
    return (INPUTS,)


@app.cell
def __(nn):
    from collections import OrderedDict

    class AutoEncoder(nn.Module):
        def __init__(self):
            super().__init__()
            self.stack = nn.Sequential(OrderedDict([
                ('input', nn.Linear(8, 3, bias=True)),
                ('sigmoid1', nn.Sigmoid()),
                ('hidden', nn.Linear(3, 8, bias=True)),
            ]))

        def forward(self, x):
            return self.stack(x)

        def encode(self, x):
            return self.stack['input'](x)
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
        # nn.init.xavier_normal_(model.stack[0].weight)
        # nn.init.normal(model.stack[0].bias)
        # nn.init.xavier_normal_(model.stack[2].weight)
        # nn.init.normal(model.stack[2].bias)

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

            loss.backward()
            sgd.step()

            if abs(loss - prev_loss) < 1e-5:
                print(f"i = {i}, loss: {loss:>7f}, prev_loss: {prev_loss:>7f}")
                break

            if i % 100 == 0:
                print(f"i = {i}, loss: {loss:>7f}")

            iters.append(i)
            losses.append(loss.item())

        return model, iters, losses
    return (train,)


@app.cell
def __(torch, train):
    import matplotlib.pyplot as plt

    torch.manual_seed(9)
    net, iters, losses = train(10000, 0.0001, 0.5)
    plt.plot(iters, losses)
    return iters, losses, net, plt


@app.cell
def __(INPUTS, net, np):
    for i in range(8):
        print(np.argmax(net(INPUTS[i]).detach().numpy()))
    return (i,)


@app.cell
def __(net, torch):
    net.stack[1](net.stack[0](torch.tensor([0.0, 0, 0, 0, 0, 0, 0, 1.0])))
    return


@app.cell
def __(INPUTS, net):
    net(INPUTS)
    #INPUTS

    return


if __name__ == "__main__":
    app.run()
