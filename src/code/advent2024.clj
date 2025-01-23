(ns code.advent2024
  (:require
   [clojure.string :as string]
   [clojure.core.match :refer [match]]
   [clojure.test :refer [deftest testing is]]))

;; Day 1

(defn slurp-two-columns
  "Returns the two columns of integers from the input file"
  [input-path]
  (let [lines (string/split (slurp input-path) #"\n")
        pairs (map #(map Integer/parseInt
                         (string/split % #"\s+"))
                   lines)
        pairs-interleaved (flatten pairs)
        col1 (take-nth 2 pairs-interleaved)
        col2 (take-nth 2 (rest pairs-interleaved))]
    [col1 col2]))

(defn solve-day1-part1
  [input-path]
  (let [[col1 col2] (slurp-two-columns input-path)]
    (reduce + 0
            (map #(abs (- %1 %2))
                 (sort col1) (sort col2)))))

(defn solve-day1-part2
  [input-path]
  (let [[col1 col2] (slurp-two-columns input-path)
        counts (frequencies col2)
        scores (map #(* % (get counts % 0)) col1)]
    (reduce + 0 scores)))

(solve-day1-part1 "src/code/data/advent2024-1.txt")
;;=> 3508942

(solve-day1-part2 "src/code/data/advent2024-1.txt")
;;=> 26593248

;; Day 2

(defn slurp-rows
  "Returns the rows of integers from the input file"
  [input-path]
  (let [lines (string/split (slurp input-path) #"\n")]
    (map #(map Integer/parseInt (string/split % #"\s+")) lines)))

(defn deltas [xs] (map - (rest xs) (drop-last xs)))

(deltas [1 2 3 4 1])
;;=> (1 1 1 -3)

(defn sign [x] (if (zero? x) 0 (/ x (abs x))))
(defn same-sign? [r] (apply = (map sign (deltas r))))

(same-sign? [1 2 3 4 5])
;;=> true
(same-sign? [5 4 3 2 1])
;;=> true
(same-sign? [5 4 3 2 7])
;;=> false

(same-sign? [8 6 4 4 1])

(defn bounded-deltas? [r]
  (every? #(and (>= (abs %) 1) (<= (abs %) 3))
          (deltas r)))

(bounded-deltas? (deltas [7 6 4 2 1]))

(defn safe-report? [r]
  (and (same-sign? r) (bounded-deltas? r)))

(defn solve-day2-part1
  [input-path]
  (count (filter safe-report? (slurp-rows input-path))))

(solve-day2-part1 "src/code/data/advent2024-2.txt")
;;=> 269

(defn filter-one
  "Returns all sequences resulting from removing one element from the input"
  [r]
  (for [i (range (count r))]
    (concat (take i r) (drop (inc i) r))))

(defn solve-day2-part2
  [input-path]
  (->> (slurp-rows input-path)
       (filter #(some safe-report? (filter-one %)))
       count))

(solve-day2-part2 "src/code/data/advent2024-2.txt")
;;=> 337

;; Day 3

(defn solve-day3-part1
  [input-path]
  (reduce + 0
          (map #(let [[_ a b] %]
                 (* (Integer/parseInt a) (Integer/parseInt b)))
               (re-seq #"mul\((\d+),(\d+)\)" (slurp input-path)))))

(solve-day3-part1 "src/code/data/advent2024-3.txt")
;;=> 171183089

(defn process-instruction
  [result inst]
  (let [[enabled sum] result]
    (match inst
      :do [true sum]
      :dont [false sum]
      [:mul a b] (if enabled
                   [enabled (+ sum (* a b))]
                   [enabled sum])
      :else result)))

(deftest test-process-instruction
  (testing "process-instruction"
    (is (= [true 6] (process-instruction [true 0] [:mul 2 3])))
    (is (= [false 0] (process-instruction [true 0] :dont)))
    (is (= [true 0] (process-instruction [false 0] :do)))
    (is (= [false 0] (process-instruction [false 0] [:mul 2 3])))
    (is (= [true 0] (process-instruction [false 0] :do)))
    (is (= [false 6] (reduce process-instruction [true 0] [[:mul 2 3] :dont [:mul 1 1]])))))

(defn parse-instructions
  [input]
  (let [matches (re-seq #"mul\((\d+),(\d+)\)|do\(\)|don't\(\)"
                        input)]
    (map #(let [[text a b] %]
           (cond
             (.startsWith text "mul") [:mul
                                       (Integer/parseInt a)
                                       (Integer/parseInt b)]
             (= text "don't()") :dont
             (= text "do()") :do))
         matches)))

(parse-instructions "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))")
;;=> ([:mul 2 4] :dont [:mul 5 5] [:mul 11 8] :do [:mul 8 5])

(defn solve-day3-part2
  [input-path]
  (reduce process-instruction [true 0]
          (parse-instructions (slurp input-path))))

(solve-day3-part2 "src/code/data/advent2024-3.txt")
;;=> [false 63866497]