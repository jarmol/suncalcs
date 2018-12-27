#lang racket
(provide currsecs JD t2JD centEpoc runMins)
(require racket/date)

; Calculation date and time
(define year 2018)
(define month 11)
(define day 8)
(define hour 8)
(define minute 42)

(define currsecs (find-seconds 00 minute hour day month year #t)) ; Add one hour if summertime!!!
(define JD (date->julian/scalinger (seconds->date currsecs #t)))
(define t2JD (+ (/ (modulo currsecs (* 3600 24)) 24. 3600.) JD -0.5))

(define centEpoc (/ (- t2JD 2451545.) 36525))
; For JD check ref.: http://www.csgnetwork.com/juliandatetodaycalc.html

; Minutes since midnight 726 at noontime 12:07
; Minutes since midnight 522 at sunrise 08:42
(define runMins (+ 42 (* 60 hour))) 
