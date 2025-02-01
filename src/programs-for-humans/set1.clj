(ns set1
  (:require [clojure.data.codec.base64 :as b64]
            [clojure.string :as str]
            [clojure.java.io :as io]
            [nextjournal.clerk :as clerk]
            [criterium.core :as c]
            [clojure.test :refer [deftest is testing test-var]]))

(clerk/serve! {:browse? true})

(comment
  (clerk/build! {:paths ["src/programs-for-humans/set1.clj"]
                 :bundle true
                 :browse true
                 :ssr true}))

(defn hex->bytes
  "Convert a hex string to a byte array"
  [hex-string]
  (let [hex-pairs (re-seq #".{2}" hex-string)]
    (byte-array (map #(Integer/parseInt % 16) hex-pairs))))

(defn bytes->hex
  "Convert a byte array to a hex string"
  [input]
  (apply str (map #(format "%02x" %1) input)))

;; Challenge 1

(defn verify
  "Takes a boolean or sequence of booleans and returns emoji checkmarks or crosses"
  [input]
  (let [to-emoji #(if % "✅" "❌")]
    (if (sequential? input)
      (str/join " " (map to-emoji input))
      (to-emoji input))))

(defn hex->base64
  [input]
  (-> input
      hex->bytes
      b64/encode
      String.))

(defn solve-ch1
  []
  (let [CH1-INPUT "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        CH1-ANSWER "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"]

    (verify (= CH1-ANSWER
               (hex->base64 CH1-INPUT)))))

(solve-ch1)
;;=> "✅"

;; Challenge 2
(defn solve-ch2
  []
  (let [CH2-INPUT1 "1c0111001f010100061a024b53535009181c"
        CH2-INPUT2 "686974207468652062756c6c277320657965"
        CH2-ANSWER "746865206b696420646f6e277420706c6179"]

    (verify (= CH2-ANSWER
               (bytes->hex (map bit-xor
                                (hex->bytes CH2-INPUT1)
                                (hex->bytes CH2-INPUT2)))))))

(solve-ch2)
;;=> "✅"

;; Challenge 3

(defn non-readable [b]
  (not (or (and (>= b (byte \A)) (<= b (byte \Z)))
           (and (>= b (byte \a)) (<= b (byte \z)))
           (= b (byte \space)))))

(defn gibberish-score
  [^bytes text]
  (/ (double (count (filter non-readable text)))
     (count text)))

(defn gibberish-score-str
  [text]
  (gibberish-score (byte-array (map byte text))))

(def sample-bytes (byte-array (map byte "correct horse battery staple")))

(comment (c/quick-bench (gibberish-score sample-bytes))
         (c/quick-bench (gibberish-score "correct horse battery staple")))

(verify [(= 0.0 (gibberish-score-str "correct horse battery staple"))
         (= 0.2 (gibberish-score-str "ABCD?"))
         (= 0.5 (gibberish-score-str "(ok)"))
         (= 1.0 (gibberish-score-str "*@&#$*&@#"))])

;; Return the scores from using each of the `trial-keys` to try
;; to decrypt the ciphertext

(defn xor-trial-keys-scores
  [ciphertext trial-keys]
  
  (for [key trial-keys
        :let [plain (byte-array (map #(bit-xor key %) ciphertext))]]

    {:key (char key)
     :score (gibberish-score plain)
     :plain (String. plain)}))

(xor-trial-keys-scores
 (hex->bytes "1b3f89af9068")
 [(byte \B)])
;;=> ({:key \B, :score 0.8333333333333334, :plain "Y}���*"})

;; Challenge 3 answer is the key with the lowest gibberish score
(defn solve-ch3
  [trial-keys]

  (let [CH3-CIPHER (hex->bytes "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")]
    (apply min-key :score
         (xor-trial-keys-scores CH3-CIPHER trial-keys))))

(solve-ch3 (range 0 255))
;;=> {:key \X, :score 0.029411764705882353, :plain "Cooking MC's like a pound of bacon"}

;; Challenge 4

(defn read-hex-lines [file-path]
  (with-open [rdr (io/reader file-path)]
    (doall (map hex->bytes (line-seq rdr)))))

(defn solve-ch4
  []
  (let [ciphers (read-hex-lines "src/data/4.txt")
      trial-keys (range 0 255)
      best-scores (map #(apply min-key :score
                               (xor-trial-keys-scores % trial-keys))
                       ciphers)]
  (apply min-key :score best-scores)))

(solve-ch4)
;;=> {:key \5, :score 0.03333333333333333, :plain "Now that the party is jumping\n"}

;; Challenge 5

(defn repeating-key-xor [text key]
  (bytes->hex (map bit-xor
                   (map byte text)
                   (cycle (map byte key)))))

(let [CH5-CIPHER "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
      CH5-ANSWER "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"]

  (verify (= CH5-ANSWER
             (repeating-key-xor CH5-CIPHER "ICE"))))

;; Challenge 6

(def CH6-CIPHER
  (b64/decode (.getBytes (str/replace (slurp "src/data/6.txt") #"\n" ""))))

CH6-CIPHER

(defn hamming-distance [s1 s2]
  (reduce + (map #(Integer/bitCount (bit-xor %1 %2)) s1 s2)))

(deftest hamming-distance-test
  (testing "hamming-distance function"
    (is (= 37 (hamming-distance (.getBytes "this is a test")
                                (.getBytes "wokka wokka!!!")))
        "Known example from the challenge")))

(def TRIAL-KEYSIZES (range 2 40))

(def distances (into (sorted-map)
                     (map #(vector (/ (hamming-distance
                                       (take % CH6-CIPHER)
                                       (take % (drop % CH6-CIPHER)))
                                      (double %1))
                                   %1)
                          TRIAL-KEYSIZES)))

distances
;; => {1.2 5,
;;     2.0 3,
;;     2.5 2,
;;     2.5384615384615383 13,
;;     2.6363636363636362 11,
;;     2.7 20,
;;     2.7777777777777777 18,
;;     2.8684210526315788 38,
;;     2.933333333333333 15,
;;     2.9411764705882355 17,
;;     3.0 16,
;;     3.0476190476190474 21,
;;     3.096774193548387 31,
;;     3.108108108108108 37,
;;     3.1739130434782608 23,
;;     3.206896551724138 29,
;;     3.2142857142857144 14,
;;     3.24 25,
;;     3.25 12,
;;     3.257142857142857 35,
;;     3.272727272727273 33,
;;     3.3 10,
;;     3.3076923076923075 39,
;;     3.3157894736842106 19,
;;     3.323529411764706 34,
;;     3.375 24,
;;     3.4166666666666665 36,
;;     3.433333333333333 30,
;;     3.4375 32,
;;     3.4814814814814814 27,
;;     3.5 26,
;;     3.5357142857142856 28,
;;     3.5555555555555554 9,
;;     3.727272727272727 22,
;;     4.0 6}

(defn block-transpose
  "Return a sequence of blocks where each block is encrypted by successive chars of the key"
  [keysize input]
  (for [i (range keysize)]
    (take-nth keysize (drop i input))))

(flatten (block-transpose 9 (flatten (block-transpose 3 "abcdefghijklmnopqrstuvwxyz"))))
;; => (\a \b \c \d \e \f \g \h \i \j \k \l \m \n \o \p \q \r \s \t \u \v \w \x \y \z)


(def LIKELY-KEYSIZES [5 3 2 13 11 20 18 38 15 17 16 21 31 37 23 29])

(map #(let [block-1 (first (block-transpose %1 CH6-CIPHER))]
        (solve-ch3 block-1 (range 0 255)))
     LIKELY-KEYSIZES)

(def KEYSIZE 29)

;; Break each of the 29 blocks

(def CH6-KEY
  (map #(:key (solve-ch3 (nth (block-transpose KEYSIZE CH6-CIPHER) %1) (range 0 255)))
       (range 0 KEYSIZE)))

(apply str CH6-KEY)
;; => "Terminator X: Bring the noise"

(count CH6-CIPHER)
;; => 2876

(Math/round (Math/ceil (double (/ (count CH6-CIPHER) KEYSIZE))))
;; => 100

(time (String. (byte-array (map bit-xor
                                CH6-CIPHER
                                (cycle (map byte CH6-KEY))))))


(set! *warn-on-reflection* true)






