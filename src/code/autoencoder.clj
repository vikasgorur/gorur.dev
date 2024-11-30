(defn make-one-hot 
  "Return a one-hot array of size n, with i hot"
  [i n]
  (let [result (vec (repeat n 0))]
    (assoc result i 1)))

(def INPUTS
  (map #(make-one-hot % 8) (range 8)))

INPUTS


