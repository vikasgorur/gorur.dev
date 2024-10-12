(ns roman-arithmetic
  (:require [clojure.test :refer [deftest testing is]]))

;; We will do arithmetic like a Roman. This means entirely operating on vectors of symbols
;; like '[V I] = 6. At no point can we convert a number to an integer because we don't
;; understand the Indian decimal system.

;; This Reddit comment has the idea that arithmetic can be done entirely as term-rewriting?
;; https://www.reddit.com/r/math/comments/rd6bpl/comment/ho0q97i/

(def SYMBOL-ORDER [\I \V \X \L \C \D \M])

;; Let's define the normal form of a roman number as a string that matches
;; the regex M*D*C*L*X*V*I*

;; In other words, the symbols appear in decreasing order and there is no
;; restriction on the number of times each symbol may appear.

(defn symbol-less-than
  [a b]
  (< (.indexOf SYMBOL-ORDER a) (.indexOf SYMBOL-ORDER b)))

(deftest symbol-less-than-test
  (testing "symbol-less-than function"
    (is (true? (symbol-less-than \I \V)))
    (is (false? (symbol-less-than \D \C)))))

(def simplify
  "Simplify by replacing any streak of four identical symbols with its simpler form (IIII -> IV)"
  [rn]

  )

(comment
  (re-seq #"(.)\1{3}" "IIII")
  (re-seq #"(.)\1{3}" "LVIIII")
  (vec (seq "ICX")))

(defn log2
  "Calculates the logarithm base 2 of x"
  [x]
  (/ (Math/log x) (Math/log 2)))


(+ (* (double 1/4) (log2 4))
   (* (double 3/4) (log2 4/3)))