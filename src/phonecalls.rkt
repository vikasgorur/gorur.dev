#lang racket

(require control)
(require racket/vector)

; Call the function f n times purely for side effects
(define (repeat f n)
  (dotimes (x n)
           (f)))

; Call f n times and sum the results
(define (repeat/sum f n)
  (let ([result 0])
    (begin (repeat (lambda ()
                     (set! result (+ result (f))))
                   n)
           result)))

(define (vector-incr! v i)
  (vector-set! v i [+ 1 (vector-ref v i)]))

(define (simulate-week w)
  (vector-fill! w 0)
  (repeat (lambda () (vector-incr! w (random 0 7)))
          12))

(define (atleast-one-per-day? w)
  (if [= (vector-count (lambda (x) (> x 0)) w) 7]
      1 0))
     

(define *N-TRIALS* 1000000.0)

(define *WEEK* (make-vector 7))

(define (trial)
  (begin (simulate-week *WEEK*)
         (atleast-one-per-day? *WEEK*)))

(time (/ (repeat/sum trial *N-TRIALS*)
         *N-TRIALS*))

