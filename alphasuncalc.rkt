#lang racket
; Sunrise, Sunset, noon, daylength, max altitude
; for given date and location
; solar-calc
; Zenith added 2018-11-29
; Hour angle   2018-11-30
; Solar elevation 2018-12-02
; Correction of solar elevation with athmospheric refraction 2018-12-03
; Azimuth at noon 2018-12-08 & at sunrise/sunset 2018-12-11

(require racket/date)
(require rackunit) ; testausta varten

(define frac (lambda (x) (- x (floor x)))); takes decimal part of number
(define radians (/ pi 180.0)) ; coefficient of conversion degrees to radians
(define degrees (/ 180 pi))   ; coefficient of conversion radians to degrees
(define toRadians (lambda (degree) (* radians degree))); conversion degrees to radians
(define toDegrees (lambda (radian) (* degrees radian))); conversion radian to degrees
(define cosd (lambda (x) (cos (toRadians x))))
(define sind (lambda (x) (sin (toRadians x))))
(define tand (lambda (x) (tan (toRadians x))))

(define currsecs (find-seconds 00 06 12 08 11 2018 #t)) ; Tunti lisää kesäaikana (keskipäivälläkin)!!!

(define currdays (/ currsecs 3600. 24.))
  
(define JD (date->julian/scalinger (seconds->date currsecs #t)))
;(define tJD (+ JD (frac currdays) -0.5))
; molemmat kaavat toimii, tJD ja t2JD
; JD tarkistusapu: http://www.csgnetwork.com/juliandatetodaycalc.html
(define t2JD (+ (/ (modulo currsecs (* 3600 24)) 24. 3600.) JD -0.5)) ; toimii myös
(define centEpoc (/ (- t2JD 2451545.) 36525))

; Mean Longitude of Sun
(define (arg1 cent) (+ 280.46646  (* cent (+ 36000.76983  (* cent 0.0003032)))))
(define decNorm360 (lambda (arg) (+ (remainder (floor arg) 360) (frac arg))))
(define meanLongSun (decNorm360 (arg1 centEpoc)))

; Mean anomality of Sun
(define (arg2 cent) (+ 357.52911 (* cent (- 35999.05029 (* 1.537e-04 cent)))))
(define meanAnomalSun (arg2 centEpoc)) ; degrees

; Eccentricy of Earth Orbit
(define eccentEarthOrbit (- 0.016708634 (* centEpoc (+ 4.2037e-05 (* 1.267e-07 centEpoc)))))

; Sun Equation of Center = The difference between the true anomaly and the mean anomaly
(define SunEqCntr
 (+ (* (sind meanAnomalSun)
 (- 1.914602 (* centEpoc (+ 0.004817 (* 0.000014 centEpoc)))))
 (* (sind (* 2 meanAnomalSun)) (- 0.019993 (* 0.000101 centEpoc)))
 (* (sind (* 3 meanAnomalSun)) 0.000289)))

; Sun true anomality
(define sunTrueAnom (+ meanAnomalSun SunEqCntr))
              
; Sun true longitude = meanLongSun + SunEqCntr
(define trueLongSun (+ meanLongSun SunEqCntr))

; Sun apparent longitude
(define appLongSun (- trueLongSun 0.00569 (* 0.00478 (sind (- 125.04 (* 1934.136 centEpoc))))))

(define obliqCorr (lambda (cent)
(+ 23 
    (/ (+ 26    
       (/ (- 21.448 (* cent   
          (+ 46.815 (* cent (- 0.00059 (* cent 0.001813)))))) 60)) 60)
 
(* 0.00256 (cosd (- 125.04 (* 1934.136 cent)))))
))

; Sun Right Ascension
(define (sunRightAscension cent) 
(toDegrees (atan (* (cosd (obliqCorr cent))
                    (sind appLongSun))
                 (cosd  appLongSun)))  ; Funktio atan toimii myös kuten atan2 
)

(define sunRtAscen (sunRightAscension centEpoc))

; Sun declination
(define (sunDeclination cent)
  (toDegrees (asin (* (sind (obliqCorr cent))
                      (sind appLongSun))))
  )

(define declination (sunDeclination centEpoc))

; parameter y
(define y (sqr (tand (/ (obliqCorr centEpoc) 2.)))) 

; Equation of time
(define (eqOfTime cent) (* 4 (toDegrees (- (+ (- (* y (sind (* 2 meanLongSun)))
    (* 2 eccentEarthOrbit (sind meanAnomalSun)))
    (* 4 eccentEarthOrbit y (sind meanAnomalSun) (cosd (* 2 meanLongSun))))                 
    (* 0.5 y y (sind (* 4 meanLongSun)))
    (* 1.25 eccentEarthOrbit eccentEarthOrbit (sind (* 2 meanAnomalSun)))
))))

; HA Sunrise hourangle
(define zenithSunriseSunset 90.833)
(define zenithCivilTwilight 96.0)
(define zenithNautical 102.)

(define geoLatitude 65.85) ; Tornio latitude
(define (HAw zenith) (toDegrees (acos  (- (/ (cosd zenith) (* (cosd geoLatitude) (cosd declination))) (* (tand geoLatitude) (tand declination))))))  
(define HAsunRise (HAw zenithSunriseSunset))

; HA Twilight
(define HAcivilTwilight (HAw zenithCivilTwilight))
(define HAnautical (HAw zenithNautical))

;(define geoLongitude 27.01) ; Utsjoki longitude
(define geoLongitude 24.18)  ; Tornio longitude
(define timeZone 2.0)
(define runMins 726)  ; Minutes since midnight 726

; Noon time
(define noonTime (/ (+ (- 720. (* 4 geoLongitude)  (eqOfTime centEpoc)) (* 60 timeZone)) 1440.))

(define AMnauticalTwilightTime (- noonTime (/ HAnautical 360.)))    ; Before Sunrise Nautical Twilight time
(define AMcivilTwilightTime (- noonTime (/ HAcivilTwilight 360.)))  ; Before Sunrise Civil Twilight time
(define sunriseTime (- noonTime (/ HAsunRise 360.)))                ; Sunrise time
(define sunsetTime  (+ noonTime (/ HAsunRise 360.)))                ; Sunset time
(define PMcivilTwilightTime (+ noonTime (/ HAcivilTwilight 360.)))  ; After Sunset Civil Twilight time
(define PMnauticalTwilightTime (+ noonTime (/ HAnautical 360.)))    ; After Sunset Nautical Twilight time 

; True Solar Time
(define TrueSolarTime (+ runMins (eqOfTime centEpoc) (- (* 4 geoLongitude) (* 60 timeZone)))) ; OK 
(define hourAngle (- (/ TrueSolarTime 4.0) 180))  ; -> -0.024373

(define (solZenith latit declinat hourAngl) 
     (toDegrees (acos (+ (* (sind latit) (sind declinat))
                         (* (cosd latit) (cosd declinat) (cosd hourAngl))))))    ; -> 82.45906533290812

(define noonZenith (solZenith geoLatitude declination hourAngle))
(define solarElevation (- 90.0 noonZenith))

; Atmospheric refraction as function of solar elevation
(define atRefract (lambda (solElevat)
                    (cond
                      ((> solElevat 85.0) 0.0)
                      
                      ((> solElevat 5.0) (/ (+ (- (/ 58.1 (tand solElevat)) (/ 0.07 (expt (tand solElevat) 3)))
                        (/ 0.000086 (expt (tand solElevat) 5))) 3600))  ; -> 0.11412 OK
                      
                      ((> solElevat -0.575) (/ (+ 1735 (* solElevat (- (* solElevat (+ 103.4 (* solElevat (- (* solElevat 0.711) 12.79)))) 518.2))) 3600)) ; -> 0.16524 OK
                      (else (/ -20.772 (tand solElevat) 3600))  ; -> 0.4286 OK
                      )))

; calculate refraction corrected elevation
(define correctedElevation (+ solarElevation (atRefract solarElevation)))

(define (decmodulo x y) (if (> x 0) (+ (modulo (inexact->exact (floor x))  y) (frac x))
                                 (- (+ (modulo (inexact->exact (floor x))  y) (frac x)) y)))  

; Azimuth
(define (palikka latit zen decl) (toDegrees (acos (/ (- (* (sind latit) (cosd zen)) (sind decl))
                   (* (cosd latit) (sind zen))))))

(define (Azimuth HA latit zen decl)

(if (>= HA 0.0) 
 (decmodulo (+      (palikka latit zen decl) 180.0) 360.)

 (decmodulo (- 540. (palikka latit zen decl)) 360))
)

; Azimuths for different times
(define noonAzimuth   (Azimuth hourAngle geoLatitude (solZenith geoLatitude declination hourAngle) declination))
(define sunsetAzimuth (Azimuth HAsunRise geoLatitude 90.833 declination))
(define sunriseAzimuth (Azimuth (- HAsunRise 180.) geoLatitude 90.833 declination))

; Daylength
(define dayLength (/ HAsunRise 180.))

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
(fprintf op2 " Azimuth at noon      ~a°~n" (~r noonAzimuth    #:precision 3))
(fprintf op2 " Azimuth at sunset    ~a°~n" (~r sunsetAzimuth  #:precision 3))
(fprintf op2 " Equation of Time      ~a minutes~n" (~r (eqOfTime centEpoc) #:precision 2))
(fprintf op2 " Julian day       ~a\n" JD) ; See https://ssd.jpl.nasa.gov/tc.cgi#top
(fprintf op2 " Local time JD    ~a\n" (fixed4 t2JD)) ; alternative tJD

(fprintf op2 "\n Calculation time:   ~a\n" (date->string (seconds->date currsecs #t) #t))
(fprintf op2 " Tornio: Latitude    ~a° N, longitude ~a° E~n" geoLatitude geoLongitude)
(fprintf op2 "\n ==========================================\n\n")
(printf "~a" (get-output-string op2))
(printf "~a" (get-output-string _out))
