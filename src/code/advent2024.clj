(ns code.advent2024 
  (:require
    [clojure.string :as string]))

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

(defn deltas [xs]
  (map -
       (rest xs)
       (drop-last xs)))

(deltas [1 2 3 4 1])
;;=> (1 1 1 -3)

(defn same-sign?
  "Returns true if all elements of xs have the same sign"
  [xs]
  (or (every? #(>= % 0) xs)
      (every? #(< % 0) xs)))

(defn monotonic? [r] (same-sign? (deltas r)))

(monotonic? [7 6 4 2 1])

(defn bounded-deltas? [r]
  (every? #(and (>= (abs %) 1) (<= (abs %) 3)) (deltas r)))

(bounded-deltas? (deltas [7 6 4 2 1]))

(defn safe-report? [r]
  ((and (monotonic? r) (bounded-deltas? r))))

(defn solve-day2-part1
  [input-path]
  (count (filter true? (map safe-report? (slurp-rows input-path)))))

(solve-day2-part1 "src/code/data/advent2024-2.txt")
;;=> 269

(defn filter-one 
  "Returns all sequences resulting from removing one element from the input"
  [r]
  (for [i (range (count r))]
    (concat (take i r) (drop (inc i) r))))

(defn solve-day2-part2
  [input-path]
  (count (filter true?
                 (map (fn [r]
                        (some true? (map safe-report? (filter-one r))))
                      (slurp-rows input-path)))))

(solve-day2-part2 "src/code/data/advent2024-2.txt")
;;=> 337

;; Day 3

(defn solve-day3-part1
  [input-path]
  (reduce + 0
          (map (fn [match]
                 (let [[_ a b] match]
                   (* (Integer/parseInt a) (Integer/parseInt b))))
               (re-seq #"mul\((\d+),(\d+)\)" (slurp input-path)))))

(solve-day3-part1 "src/code/data/advent2024-3.txt")
;;=> 171183089
