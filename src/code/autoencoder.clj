
;; A vector is a Java float array
;; A matrix is a 2d Java float array

(defn make-one-hot 
  "Return a one-hot array of size n, with i hot"
  [i n]
  (let [result (make-array Float/TYPE n)]
    (aset-float result i 1.0)
    result))

(def INPUTS
  (map #(make-one-hot % 8) (range 8)))

INPUTS

(defn argmax
  "Return the index with the max value in a vector"
  [v]
  (first (apply max-key second (map-indexed vector v))))

(comment
  (argmax (vec [0 1 8 7])))
  ;;=> 2

(defn sigmoid
  "Sigmoid of a vector"
  [xs]
  (map #(/ 1 (+ 1 (Math/exp (- %)))) xs))

(sigmoid (make-one-hot 2 8))

(defn count-rows [M]
  (count M))

(defn count-columns [M]
  (count (aget M 0)))

(defn dot
  "Dot product of two vectors"
  [a b]
  (reduce + 0.0 (map * a b)))

(dot [1 2 3] [4 5 6])
;;=> 32.0

(defn matrix-vector
  "Multiply a matrix by a vector"
  [M v]
  (assert (= (count-columns M) (count v)))

  (let [result (make-array Float/TYPE (count-rows M))]
    (doseq [i (range (count-rows M))]
      (aset-float result i
                  (dot (aget M i) v)))
    result))

(comment
  (matrix-vector (random-matrix 2 2) (random-vector 2))
  (matrix-vector (random-matrix 3 8) (random-vector 8)))

(defn random-vector
  "Random vector of size n"
  [n]
  (let [result (make-array Float/TYPE n)]
    (doseq [i (range n)]
      (aset-float result i (rand)))
    result))

(random-vector 8)

(defn random-matrix
  "Random matrix of shape (r, c)"
  [r c]
  (let [result (make-array Float/TYPE r c)]
    (doseq [i (range r)
            j (range c)]
      (aset-float result i j (rand)))
    result))

(aget (random-matrix 3 3) 1)

(defn feed-forward
  "The forward pass of the autoencoder"
  [input W0 W1]
  (matrix-vector W1
                 (sigmoid (matrix-vector W0 input))))

(feed-forward (make-one-hot 2 8)
              (random-matrix 8 3)
              (random-matrix 3 8))

(count (aget (random-matrix 8 3) 0))

(range 8)

(defn mean-squared-loss
  [y yhat]
  (reduce + 0 (map #((Math/pow (- %1 %2) 2))
                   y yhat)))

(mean-squared-loss
 [1 2 3.0]
 [1 1 1.0])
