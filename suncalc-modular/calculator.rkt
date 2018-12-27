#lang racket
; Sunrise, Sunset, noon, daylength, max altitude
; for given date and location
; solar-calc
; Zenith added 2018-11-29
; Hour angle   2018-11-30
; Solar elevation 2018-12-02
; Correction of solar elevation with athmospheric refraction 2018-12-03
; Azimuth at the calculation time
; Less imported parametres from the module solar.rkt 2018-12-27
; Location and timezone from the file indata.rkt
; calculation date and time from juliandates.rkt

(require racket/date)
(require "indata.rkt")
(require "trigonometrics.rkt")
(require "juliandates.rkt")
(require "solar.rkt")
(require rackunit) ; testing values

(define-syntax-rule (def id body) (define id body))

; Sun declination
(check-within declination -16.5678 1.0e-04)  ; Test OK

; Solar times to date common time strings
(define (getHours xTime) (exact-floor (* 24. xTime)))
(define (getMinutes xTime) (modulo (exact-floor (/ (* 24 3600 xTime) 60)) 60))
(define (getSeconds xTime) (modulo (exact-floor (* 24 3600 xTime)) 60))

(define (suntimes xTime) (date->string (seconds->date (find-seconds (getSeconds xTime)
                                                       (getMinutes xTime) 
                                                       (getHours xTime) 8 11 2018) #t) #t))

(define (fixed4 x) (/ (round (* 1.0e4 x)) 1.0e4))
(define (fixed6 x) (/ (round (* 1.0e6 x)) 1.0e6))

(define _out (open-output-string))

(fprintf _out "Current seconds ~a\n" currsecs)

(fprintf _out "Hour angle               ~a°~n" (fixed4 hourAngle))
(fprintf _out "Solar elevation           ~a°~n" (fixed4 solarElevation))

(define op2 (open-output-string))

(define posDeclin (if (> 0.0 declination) " Arctic winter - No Sunset!" " Arctic summer - no sunrise"))

(date-display-format 'rfc2822)
(if (real? HAnautical)      (fprintf op2 " Nautical twilight   ~a\n" (suntimes AMnauticalTwilightTime)) " Arctic summer - no nautical twilight")
(if (real? HAcivilTwilight) (fprintf op2 " Civil twilight time ~a\n" (suntimes AMcivilTwilightTime))    " Arctic summer - no civil twilight")
(if (real? HAsunRise) (fprintf op2 " Sunrise time        ~a\n" (suntimes sunriseTime)) posDeclin)
(fprintf op2 " Noon time           ~a\n" (suntimes noonTime))
(if (real? HAsunRise) (fprintf op2 " Sunset time         ~a\n" (suntimes sunsetTime))  posDeclin)
(if (real? HAcivilTwilight) (fprintf op2 " Civil twilight time ~a\n" (suntimes PMcivilTwilightTime))    " Arctic summer - no civil twilight")
(if (real? HAnautical)      (fprintf op2 " Nautical twilight   ~a\n" (suntimes PMnauticalTwilightTime)) " Arctic summer - no nautical twilight")

(if (real? dayLength) (fprintf op2 " Daylength            ~a\n" (substring (suntimes dayLength) 16 24)) " Daylength not determined")

(fprintf op2 " Sun declination      ~a°~n" (fixed4 declination))
(fprintf op2 " Zenith at noon        ~a°~n" (fixed4 noonZenith))
(fprintf op2 " Sun elevation corr.    ~a°~n" (fixed4 correctedElevation))
(fprintf op2 " Atmospher. refraction  ~a°~n" (fixed4 (atRefract solarElevation)))
(fprintf op2 " Azimuth at sunrise   ~a°~n" (~r sunriseAzimuth #:precision 3))
(fprintf op2 " Azimuth at calc. t.  ~a°~n" (~r noonAzimuth    #:precision 3))
(fprintf op2 " Azimuth at sunset    ~a°~n" (~r sunsetAzimuth  #:precision 3))
(fprintf op2 " Equation of Time      ~a minutes~n" (~r (eqOfTime centEpoc) #:precision 2))
(fprintf op2 " Julian day       ~a\n" JD) ; See https://ssd.jpl.nasa.gov/tc.cgi#top
(fprintf op2 " Local time JD    ~a\n" (fixed4 t2JD)) ; alternative tJD

(fprintf op2 "\n Calculation time:   ~a\n" (date->string (seconds->date currsecs #t) #t))
(fprintf op2 " Tornio: Latitude    ~a° N, longitude ~a° E~n" geoLatitude geoLongitude)
(fprintf op2 "\n ==========================================\n\n")
(printf "~a" (get-output-string op2))
(printf "~a" (get-output-string _out))
