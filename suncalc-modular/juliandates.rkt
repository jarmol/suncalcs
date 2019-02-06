#lang racket/base
(provide selectMode currsecs JD t2JD centEpoc runMins hour day month year day2 month2 fixedTime)
(require racket/date)
(require racket/struct)

; Calculation date and time 
(define year 2019)
(define month 2)
(define day 1)
(define hour 12)
(define minute 37)
(define A (current-date))
(define L (struct->list A))
(define isItFixed 0)
(define (selectMode isItFixed) (if (eq? isItFixed 1) #t #f))

(define fixedTime #t)
;(define fixedTime #f)

; Lisättävä tämänhetkinen päivä ja kuukausi
(define (getDay   currDateStruct) (car  (cdddr currDateStruct))) ; Current day
(define (getMonth currDateStruct) (cadr (cdddr currDateStruct))) ; Current Month
(define day2   (getDay L))
(define month2 (getMonth L))

(define (getTime isitFixed?)
(if isitFixed? (find-seconds 00 minute hour day month year #t) ; Add one hour if summertime!!!
 (current-seconds))) ; selected current time

; If fixed time set #true then use it
; else use current time
(define currsecs  (getTime fixedTime))

(define JD (date->julian/scalinger (seconds->date currsecs #t)))
(define t2JD (+ (/ (modulo currsecs (* 3600 24)) 24. 3600.) JD -0.5))

(define centEpoc (/ (- t2JD 2451545.) 36525))
; For JD check ref.: http://www.csgnetwork.com/juliandatetodaycalc.html

; Minutes since midnight 727 at noontime 12:07
; Minutes since midnight 522 at sunrise 08:42

(define (getMins isitFixed?)
  (if isitFixed?
(+ minute (* 60 hour))  ; fixed time
(+ (/ (car L) 60.0) (cadr L) (* 60 (caddr L))))) ; current time: seconds, minute and hour

; get minutes since midnight

(define runMins (getMins fixedTime))
