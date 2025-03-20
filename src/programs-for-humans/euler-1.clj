(ns programs-for-humans.euler-1
  (:require [programs-for-humans.primes :as primes]
            [clojure.core :as core]
            [clojure.string :as str]
            [clojure.set :as set]))

;; # Project Euler
;;
;; The first 100 problems.

;; Progress report
(defn count-solved []
  (->> (slurp "src/programs-for-humans/project-euler.qmd")
       str/split-lines
       (filter #(.startsWith % "## Problem"))
       count))

(defn hundred-days-progress
  []
  (let [today (java.time.LocalDate/now)
        feb-23 (java.time.LocalDate/of 2025 2 23)
        days (.until feb-23 today java.time.temporal.ChronoUnit/DAYS)
        solved (count-solved)]
    [solved days]))

(hundred-days-progress)
;;=> [14 25]

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

;; ## Problem 4

(defn is-palindrome? [x]
  (let [xstr (Integer/toString x)]
    (= (map char xstr) (reverse xstr))))

(is-palindrome? 99)

(->> (for [a (range 100 1000)
           b (range 100 1000)
           :when (is-palindrome? (* a b))]
       (* a b))
     sort
     last)
;;=> 906609

;; ## Problem 5
;; What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

(* (* 2 2 2 2) (* 3 3) 5 7 11 13 17 19)
;;=> 232792560

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

;; ## Problem 8
;; Find the thirteen adjacent digits in the 1000-digit
;; number that have the greatest product. What is the value of this product?

(def INPUT-8 (filter #(not= % \newline)
                     (slurp "src/code/data/euler-8-input.txt")))

(->> (for [i (range 0 (- (count INPUT-8) 13))]
       (reduce * 1 (map #(Character/digit % 10)
                        (take 13 (drop i INPUT-8)))))
     sort
     last)
;;=> 23514624000

;; ## Problem 9
;; Find the one Pythagorean triplet for which a + b + c = 1000
(defn is-pythagorean? [v]
  (let [[a b c] (sort v)]
    (= (* c c)
       (+ (* a a) (* b b)))))

(->> (for [c (range 1 1000)
           :let [aplusb (- 1000 c)]]
       (for [a (range 1 aplusb)
             :let [b (- aplusb a)]
             :when (and (distinct? a b c)
                        (is-pythagorean? (vector a b c)))]
         (sort [a b c])))
     (mapcat identity)
     distinct
     first
     (reduce * 1))
;;=> 31875000
;;=> (200 375 425)

;; ## Problem 10
(reduce + 0 (primes/sieve-of-eratosthenes 2000000))
;;=> 142913828922

;; ## Problem 12
;; Highly divisible triangular numbers

(defn nth-triangle-number [n]
  (/ (* n (inc n)) 2))

(loop [i 1]
  (let [triangle (nth-triangle-number i)
        div-count (count (primes/divisors triangle))]
    (if (> div-count 500)
      triangle
      (recur (inc i)))))

;; ## Problem 17

(def DIGITS
  {
   1 "one"
   2 "two"
   3 "three" 
   4 "four"
   5 "five"
   6 "six"
   7 "seven"
   8 "eight"
   9 "nine"
   }
)

(def TEENS
  {
   11 "eleven"
   12 "twelve"
   13 "thirteen"
   14 "fourteen" 
   15 "fifteen"
   16 "sixteen"
   17 "seventeen"
   18 "eighteen"
   19 "nineteen"
  })

(def TENS
  {
   10 "ten"
   20 "twenty"
   30 "thirty"
   40 "forty"
   50 "fifty"
   60 "sixty"
   70 "seventy"
   80 "eighty"
   90 "ninety"
  })

(defn hundreds-count [h]
  (if (zero? h) 0
      (+ (count (DIGITS h)) (count "hundred"))))

(defn tens-count [t]
  (cond 
    (zero? t) 0                              ;; when t is 0
    (< t 10) (count (DIGITS t))              ;; single digit numbers
    (<= 11 t 19) (count (TEENS t))           ;; teen numbers
    :else (+ (count (TENS (* 10 (quot t 10))))  ;; numbers 20-99
             (if (zero? (mod t 10))
               0
               (count (DIGITS (mod t 10)))))))

(defn number-in-words-count [x]
  (let [h (quot x 100)
        t (mod x 100)
        and-count (if (and (> h 0) (not (zero? t))) (count "and") 0)]
    (+ (hundreds-count h) (tens-count t) and-count)))

(+ (->> (range 1 1000)
     (map number-in-words-count)
     (reduce + 0))
   (count "onethousand"))
;;=> 21124

;; ## Problem 19
;; How many Sundays fell on the first of the month during
;; the twentieth century (1 Jan 1901 to 31 Dec 2000)?

(defn is-leap-year? [y]
  (let [four (zero? (mod y 4))
        hundred (zero? (mod y 100))
        four-hundred (zero? (mod y 400))]
    (or (and four (not hundred))
        (and four hundred four-hundred))))

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

;; ## Problem 22
;; ## Names scores

(defn word-score [w]
  (reduce + 0 (map #(- (int (Character/toUpperCase %)) 64) w)))

(word-score "COLIN")

(let [sorted-names (->> (str/split
                         (slurp "src/code/data/euler_0022_names.txt")
                         #",")
                        (map #(str/replace % #"\"" ""))
                        sort)]
  (reduce + 0 (map-indexed
               #(* (inc %1) (word-score %2))
               sorted-names)))

;;=> 871198282

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

;; Problem 54
;; Who wins the poker hands?

;; A hand is a vector [rank suite]
(def RANKS [:2 :3 :4 :5 :6 :7 :8 :9 :T :J :Q :K :A])
(def SUITES #{:H :D :S :C})



