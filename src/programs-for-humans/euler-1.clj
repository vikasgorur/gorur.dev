(ns euler-1)

;; Problem 1

(->> (range 1000)
     (filter #(or (zero? (mod % 3)) (zero? (mod % 5))))
     (reduce +))
;;=> 233168

;; Problem 2

(loop [f1 1,
       f2 2,
       even-sum 0]

  (if (>= f2 4000000)
    even-sum
    (if (zero? (mod f2 2))
      (recur f2 (+ f1 f2) (+ even-sum f2))
      (recur f2 (+ f1 f2) even-sum))))
;;=> 4613732

;; Problem 6

(- (int (Math/pow (->> (range 1 101)
                       (reduce +))
                  2))
   (->> (range 1 101)
        (map #(int (Math/pow % 2)))
        (reduce +)))
;;=> 25164150

;; Problem 65

(defn sum-terms
  "Sum the terms of a continued fraction"
  [xs]
  (if (empty? xs)
    0
    (/ 1 (+ (first xs) (sum-terms (rest xs))))))

;; sqrt(2)
(+ 1 (sum-terms (repeat 9 2)))
;;=> 3363/2378

;; e
(defn e-terms
  "The first n terms of the continued fraction for e"
  [n]
  )

(+ 2 (sum-terms [1 2 1 1 4 1 1 6 1 1]))
;;=> 2721/1001

;; Sum of 


