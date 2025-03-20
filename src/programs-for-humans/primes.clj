(ns programs-for-humans.primes
  (:import java.util.BitSet))

(defn divisors [n]
  (concat (->> (range 1 (inc (Math/ceil (/ n 2))))
               (filter #(= (mod n %) 0)))
          [n]))

(defn is-divisible-by-any?
  "Returns true if x is divisible by any of the ds"
  [x ds]
  (some #(= (mod x %) 0) ds))

(is-divisible-by-any? 600851475143 [2 3 5 7 11 13 17 19 23 29])

;; 600851475143

(Math/sqrt 600851475143)
;;=> 775146.0992245268

(def b (BitSet. 4))
(.set b 0 4)
(.clear b)
b


(defn sieve-of-eratosthenes
  "Implements the Sieve of Eratosthenes algorithm to find prime numbers up to n"
  [n]
  (let [sieve (BitSet. (inc n))]
    ;; Set all bits to true initially
    (.set sieve 0 (inc n))

    ;; 0 and 1 are not prime
    (.clear sieve 0)
    (.clear sieve 1)

    (doseq [x (range 2 (inc (int (Math/sqrt n))))]
      (doseq [i (range 2 (inc (quot n x)))]
        (.clear sieve (* x i))))
    
    (filter #(.get sieve %) (range 2 n))))

(sieve-of-eratosthenes 100)
(sieve-of-eratosthenes (int (Math/sqrt 600851475143)))

