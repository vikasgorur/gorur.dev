#lang at-exp racket

(require infix)

(define (S n k)
  (cond
    [(or (= n 0) (= k 0)) 0]
    [else 0]))


(define (fib n)
  (cond [(<= n 1) 1]
        [else @${
                 fib[n - 1] + fib[n - 2]
        }]))
