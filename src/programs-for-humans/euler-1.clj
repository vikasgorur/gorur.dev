(ns euler-1
  (:require [primes]))

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

;; ## Problem 3
;; Largest prime factor of 600851475143

(let [N 600851475143]
  (->> (primes/sieve-of-eratosthenes (int (Math/sqrt N)))
       reverse
       (filter #(zero? (mod N %)))
       first))
;;=> 6857

(quot 13195 5)

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
(let [N 10001
      approx-nth-prime (* N (Math/log N))]
  (nth (primes/sieve-of-eratosthenes
        (int (* 1.2 approx-nth-prime)))
       (dec N)))

;;=> 104743

;; ## Problem 19
;; How many Sundays fell on the first of the month during
;; the twentieth century (1 Jan 1901 to 31 Dec 2000)?

(defn days-in-month [m y]
  (case m
    1 31
    2 (if (is-leap-year? y) 29 28)
    3 31
    4 30
    5 31
    6 30
    7 31
    8 31
    9 30
    10 31
    11 30
    12 31))

(defn is-leap-year? [y]
  (let [four (zero? (mod y 4))
        hundred (zero? (mod y 100))
        four-hundred (zero? (mod y 400))]
    (or (and four (not hundred))
        (and four hundred four-hundred))))

(map is-leap-year? [1900 1996 2000])
;;=> (false true true)

(let [day (atom 2)      ;; Jan 1 1901 was a Tuesday
      result (atom 0)]  

  (doseq [year (range 1901 2001)
          month (range 1 13)]
    (reset! day (mod (+ @day (days-in-month month year)) 7))
    (when (zero? @day)
      (println year month)
      (swap! result inc)))
  @result)
;;=> 171

;; ## Problem 21 - Amicable numbers

(defn sum-proper-divisors
  "Returns the sum of all divisors of n, excluding n itself"
  [n]
  (->> (range 1 (inc (Math/ceil (/ n 2))))
       (filter #(= (mod n %) 0))
       (reduce + 0)))

(defn amicable? [a]
  (let [b (sum-proper-divisors a)]
    (and (not= a b)
         (= (sum-proper-divisors b) a))))

(->> (range 2 10001)
     (filter amicable?)
     (reduce + 0))
;;=> 31626

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






