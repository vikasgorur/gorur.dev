(ns autoencoder
  (:require [clojure.test :refer [deftest testing is]]))

(defn dot
  "Returns the dot product of a and b"
  ^double
  [^"[D" a  ^"[D" b]
  (loop [i      0
         result 0.0]
    (if (= i (alength a))
      result
      (recur (inc i)
             (+ result (* (aget a i) (aget b i)))))))

(defn sigmoid
  "Computes the sigmoid of each element of x and stores the result"

  [^"[D" result
   ^"[D" x]
  (let [sigma (fn [x] (/ 1 (+ 1 (Math/exp (- x)))))]
    (dotimes [i (alength x)]
      (aset result i (sigma (aget x i))))
    result))

(defn random-array
  ([n] (let [^"[D" result (make-array Double/TYPE n)]
         (dotimes [i n]
           (aset result i (Math/random)))
         result))
  ([m n] (let [^"[[D" result (make-array Double/TYPE m n)]
           (doseq [i (range m)
                   j (range n)]
             (aset result i j (Math/random)))
           result)))

(defn vector-add
  "Adds two vectors and stores the result"

  [^"[D" result ^"[D" a ^"[D" b]
  (dotimes [i (alength a)]
    (aset result i (+ (aget a i) (aget b i))))
  result)

(defn matrix-vector
  "Multiplies W and x and stores the result"
  [^"[D" result ^"[[D" W ^"[D" x]
  
  (dotimes [i (alength W)]
    (aset result i
          (dot (aget W i) x)))
  result)

;; forward pass

;; h = W0 * x + b0
;; output = sigmoid(W1 * h + b1)

(def NETWORK
  {:W0      (random-array 3 8)
   :W0-grad (make-array Double/TYPE 3 8)

   :b0      (random-array 3)
   :b0-grad (make-array Double/TYPE 3)

   :W1      (random-array 8 3)
   :W1-grad (make-array Double/TYPE 8 3)

   :b1      (random-array 8)
   :b1-grad (make-array Double/TYPE 8)})

(alength (:W0 NETWORK))

;; TODO: make sure I count the number of bytes needed to run the computation
;; and the number of FLOPs

(defn feed-forward
  [x]
  (let [h      (make-array Double/TYPE 3)
        W0x    (make-array Double/TYPE 3)
        W1h    (make-array Double/TYPE 8)
        p      (make-array Double/TYPE 8) ;; pre-activation
        output (make-array Double/TYPE 8)]
    
    (vector-add h
                (matrix-vector W0x (:W0 NETWORK) x)
                (:b0 NETWORK))
    (vector-add p
                (matrix-vector W1h (:W1 NETWORK) h)
                (:b1 NETWORK))
    (sigmoid output p)
    output))

(def INPUTS (let [A (make-array Double/TYPE 8 8)]
              (dotimes [i 8]
                (aset A i i 1))
              A))

(mse-loss (feed-forward (aget INPUTS 3))
          (aget INPUTS 3))

(defn mse-loss
  [^"[D" y' ^"[D" y]
    (loop [i      0
          result 0.0]
     (if (= i (alength y))
       result
       (recur (inc i)
              (+ result (Math/pow (- (aget y i) (aget y' i)) 2))))))

;; Tests
(deftest test-dot
  (testing "dot product"
    (is (= 3.0
           (dot (into-array Double/TYPE [1.0 1.0 1.0])
                (into-array Double/TYPE [1.0 1.0 1.0]))))
    (is (= 0.0
           (dot (into-array Double/TYPE [1.0 -1.0])
                (into-array Double/TYPE [1.0 1.0]))))
    (is (= 14.0
           (dot (into-array Double/TYPE [1.0 2.0 3.0])
                (into-array Double/TYPE [1.0 2.0 3.0]))))
    (is (= -4.0
           (dot (into-array Double/TYPE [-1.0 2.0 -3.0])
                (into-array Double/TYPE [3.0 1.0 1.0]))))))

(deftest test-sigmoid
  (testing "sigmoid"
    (let [result (make-array Double/TYPE 3)]
      (is (= [0.2689414213699951 0.5 0.7310585786300049]
             (seq (sigmoid result (into-array Double/TYPE [-1.0 0 1.0]))))))))

(set! *warn-on-reflection* true)

