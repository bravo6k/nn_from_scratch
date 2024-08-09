import random
from engine import Value
from show_graph import draw_dot

class Module:

    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0

    def parameters(self):
        return []


class Neuron(Module):
    def __init__(self, d_in, nonlin=True) -> None:
        self.w = [Value(random.uniform(-1, 1)) for i in range(d_in)]
        self.b = Value(random.uniform(-1, 1))
        self.nonlin = nonlin

    def __call__(self, x):
        act = sum((wi*xi for xi, wi in zip(x,self.w)),self.b)
        return act.tanh() if self.nonlin else act

    
    def parameters(self):
        return self.w + [self.b]
    

class Layer(Module):
    def __init__(self, d_in, d_out) -> None:
        self.neurons = [Neuron(d_in) for i in range(d_out)]

    def __call__(self, x):
        return [i(x) for i in self.neurons] if len(self.neurons) !=1 else self.neurons[0](x)
    
    def parameters(self):
        return [p for n in self.neurons for p in n.parameters()]

class MLP(Module):
    def __init__(self, d_in, list_d_out) -> None:
        size = [d_in] + list_d_out
        self.layers = [Layer(size[i], size[i+1]) for i in range(len(list_d_out))]

    def __call__(self, x):
        for i in self.layers:
            x = i(x)
        return x
    
    def parameters(self,return_type='list'):
        if return_type == 'list':
            return [p for layer in self.layers for p in layer.parameters()]
        else:
            params = {f"Layer {i}": [k for k in j.parameters()]
                       for i,j in enumerate(self.layers)}
            return params
