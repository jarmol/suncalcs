#lang racket

(provide (all-defined-out))

(define frac (lambda (x) (- x (floor x)))); takes decimal part of number
(define radians (/ pi 180.0)) ; coefficient of conversion degrees to radians
(define degrees (/ 180 pi))   ; coefficient of conversion radians to degrees
(define toRadians (lambda (degree) (* radians degree))); conversion degrees to radians
(define toDegrees (lambda (radian) (* degrees radian))); conversion radian to degrees
(define cosd (lambda (x) (cos (toRadians x))))
(define sind (lambda (x) (sin (toRadians x))))
(define tand (lambda (x) (tan (toRadians x))))
(define (fixed4 x) (/ (round (* 1.0e4 x)) 1.0e4))
(define (fixed6 x) (/ (round (* 1.0e6 x)) 1.0e6))

(define decNorm360 (lambda (arg) (+ (remainder (floor arg) 360) (frac arg))))

(define (decmodulo x y) (if (> x 0) (+ (modulo (inexact->exact (floor x))  y) (frac x))
                            (- (+ (modulo (inexact->exact (floor x))  y) (frac x)) y)))  

