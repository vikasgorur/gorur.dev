type vector = number[];
type matrix = number[][];

function assert(condition: boolean, message?: string): asserts condition {
    if (!condition) {
        throw new Error(message || "Assertion failed");
    }
}

// Vector primitives
function dot(a: vector, b: vector): number {
    assert(a.length === b.length, "dot: vectors must have the same length");
    return a.map((value, index) => value * b[index]).reduce(
        (total, x) => total + x,
        0
    );
}

function sigmoid(x: vector): vector {
    let sigma = (x: number) => 1 / (1 + Math.exp(-x))
    return x.map((xi, i) => sigma(xi))
}

function randomVector(n: number): vector {
    let result = new Array<number>(n);
    for (let i = 0; i < result.length; i++) {
        result[i] = Math.random();
    }
    return result;
}

function vectorAdd(a: vector, b: vector) {
    assert(a.length === b.length, "add: vectors must have the same length");

    let result = new Array<number>(a.length);
    for (let i = 0; i < result.length; i++) {
        result[i] = a[i] + b[i]; 
    }
    return result;
}

// Matrix primitives
function matrixVector(W: matrix, x: vector): vector {
    let result = new Array<number>(W.length);

    for (let row = 0; row < W.length; row++) {
        result[row] = dot(W[row], x);
    }
    return result;
}

function randomMatrix(r: number, c: number): matrix {
    let result: matrix = new Array<Array<number>>(r);
    for (let i = 0; i < r; i++) {
        result[i] = new Array<number>(c); 
        for (let j = 0; j < c; j++) {
            result[i][j] = Math.random();
        }
    }
    return result;
}

// Network
interface Layer {
    W: {
        value: matrix;
        grad: matrix;
    }; 
    b: {
        value: vector;
        grad: vector;
    };
}

interface Network {
    layers: Array<Layer>;
}

const AUTOENCODER: Network = {
    layers: [
        // input layer
        {
            W: { value: randomMatrix(3, 8), grad: randomMatrix(3, 8) },
            b: { value: randomVector(3), grad: randomVector(3) }
        },
        // output layer
        {
            W: { value: randomMatrix(8, 3), grad: randomMatrix(8, 3) },
            b: { value: randomVector(8), grad: randomVector(8) }
        }
    ]
};

function feedForward(x: vector): vector {
    let h = vectorAdd(
        matrixVector(AUTOENCODER.layers[0].W.value, x),
        AUTOENCODER.layers[0].b.value
    );
    let p = vectorAdd(
        matrixVector(AUTOENCODER.layers[1].W.value, h),
        AUTOENCODER.layers[1].b.value
    );
    let output = sigmoid(p);
    return output;
}

// Loss
function mseLoss(yhat: vector, y: vector): number {
    let loss = 0;
    for (let i = 0; i < yhat.length; i++) {
        loss += Math.pow(yhat[i] - y[i], 2);
    }
    return loss;
}

// Exports
export {
    vector, matrix,
    // vector
    dot,
    sigmoid,
    vectorAdd,
    randomVector,
    // matrix
    matrixVector,
    randomMatrix,
    // network
    feedForward,
};