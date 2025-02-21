(ns euler-1)

;; # Project Euler
;;
;; The first 100 problems.

;; ## Problem 1
;; Difficulty: 5%
;;
;; Find the sum of all multiples of 3 or 5 below 1000.

(->> (range 1000)
     (filter #(or (zero? (mod % 3)) (zero? (mod % 5))))
     (reduce +))
;;=> 233168

;; ## Problem 2
;; Difficulty: 5%
;;
;; By considering the terms in the Fibonacci sequence whose values
;; do not exceed four million, find the sum of the even-valued terms.

(loop [f1 1,
       f2 2,
       even-sum 0]

  (if (>= f2 4000000)
    even-sum
    (if (zero? (mod f2 2))
      (recur f2 (+ f1 f2) (+ even-sum f2))
      (recur f2 (+ f1 f2) even-sum))))
;;=> 4613732

;; ## Problem 6
;; Difficulty: 5%
;;
;; Find the difference between the sum of the squares of the first
;; one hundred natural numbers and the square of the sum.

(- (int (Math/pow (->> (range 1 101)
                       (reduce +))
                  2))
   (->> (range 1 101)
        (map #(int (Math/pow % 2)))
        (reduce +)))
;;=> 25164150

;; ## Problem 7
;;
;; Difficulty: 5%


;; ## Problem 65
;; Difficulty: 15%
;;
;; $e$ can be written as the continued fraction
;; $[2; 1, 2, 1, 1, 4, 1, 1, 6, 1, ... , 1, 2k, 1, ...]$
;;
;; The $n$th "convergent" of a continued fraction is the result of 
;; summing it upto $n$ terms. Find the sum of the digits in the
;; numerator of the 100th convergent of the fraction for $e$.
;;
;; First we write a generic function to sum the first $n$ terms
;; of a continued fraction.
(defn sum-terms
  [xs]
  (if (empty? xs)
    0
    (/ 1 (+ (first xs) (sum-terms (rest xs))))))

;; We can test that it works by computing $\sqrt{2}$ upto 10 terms.
(float (+ 1 (sum-terms (repeat 9 2))))
;;=> 1.4142137

;; The fraction for $e$ is slightly more complicated because the $k$th
;; term can be either $2k$ or $1$.
(defn e-terms
  "The first n terms of the continued fraction for e"
  [n]
  (take n (map (fn [k]
                 (case (mod k 3)
                   0 1
                   1 (* 2 (inc (quot k 3)))
                   2 1))
               (range n))))

;; Now sum the first 100 terms and compute the sum of the digits
;; of the numerator.
(reduce + (map #(Character/digit % 10)
               (str (numerator (+ 2 (sum-terms (e-terms 99)))))))
;;=> 272






