#lang racket
(provide sunDeclination declination HAsunRise dayLength eqOfTime
         HAcivilTwilight HAnautical noonTime TrueSolarTime AMnauticalTwilightTime AMcivilTwilightTime
         sunriseTime sunsetTime PMcivilTwilightTime PMnauticalTwilightTime hourAngle atRefract
         noonZenith solarElevation
         correctedElevation Azimuth sunriseAzimuth noonAzimuth sunsetAzimuth)

(require "trigonometrics.rkt")
(require "juliandates.rkt")
(require "indata.rkt")

(define-syntax-rule (def id body) (define id body))


; Mean Longitude of Sun (not exported)
(def (arg1 cent) (+ 280.46646  (* cent (+ 36000.76983  (* cent 0.0003032)))))
(def meanLongSun (decNorm360 (arg1 centEpoc)))

; Mean anomality of Sun (not exported)
(def (arg2 cent) (+ 357.52911 (* cent (- 35999.05029 (* 1.537e-04 cent)))))
(def meanAnomalSun (arg2 centEpoc)) ; degrees

; Eccentricy of Earth Orbit (not exported)
(def eccentEarthOrbit (- 0.016708634 (* centEpoc (+ 4.2037e-05 (* 1.267e-07 centEpoc)))))

; Sun Equation of Center = The difference between the true anomaly and the mean anomaly
; not exported
(def SunEqCntr
 (+ (* (sind meanAnomalSun)
 (- 1.914602 (* centEpoc (+ 0.004817 (* 0.000014 centEpoc)))))
 (* (sind (* 2 meanAnomalSun)) (- 0.019993 (* 0.000101 centEpoc)))
 (* (sind (* 3 meanAnomalSun)) 0.000289)))

; Sun true anomality not needed!
;(def sunTrueAnom (+ meanAnomalSun SunEqCntr))

; Sun true longitude = meanLongSun + SunEqCntr
(def trueLongSun (+
                  meanLongSun
                  SunEqCntr))

; Sun apparent longitude
(def appLongSun (- trueLongSun 0.00569 (* 0.00478 (sind (- 125.04 (* 1934.136 centEpoc))))))

(def obliqCorr (lambda (cent)
(+ 23 
    (/ (+ 26    
       (/ (- 21.448 (* cent   
          (+ 46.815 (* cent (- 0.00059 (* cent 0.001813)))))) 60)) 60)
 
(* 0.00256 (cosd (- 125.04 (* 1934.136 cent)))))
))

; Sun Right Ascension not needed!
;(def (sunRightAscension cent) 
;(toDegrees (atan (* (cosd (obliqCorr cent))
;                    (sind appLongSun))
;                    (cosd  appLongSun)))  ; Function atan works also like atan2 
;)

; (def sunRtAscen (sunRightAscension centEpoc)) ; Not needed!

; Sun declination
(def (sunDeclination cent)
  (toDegrees (asin (* (sind (obliqCorr cent))
                      (sind appLongSun))))
  )

(def declination (sunDeclination centEpoc))

; parameter y
(def y (sqr (tand (/ (obliqCorr centEpoc) 2.)))) 

; Equation of time
(def (eqOfTime cent) (* 4 (toDegrees (- (+ (- (* y (sind (* 2 meanLongSun)))
    (* 2 eccentEarthOrbit (sind meanAnomalSun)))
    (* 4 eccentEarthOrbit y (sind meanAnomalSun) (cosd (* 2 meanLongSun))))                 
    (* 0.5 y y (sind (* 4 meanLongSun)))
    (* 1.25 eccentEarthOrbit eccentEarthOrbit (sind (* 2 meanAnomalSun)))
))))

(def zenithSunriseSunset 90.833)
(def zenithCivilTwilight 96.0)
(def zenithNautical 102.)

;(def geoLatitude 65.85) ; Tornio latitude

; HA Twilight
(def (HAw zenith) (toDegrees (acos  (- (/ (cosd zenith) (* (cosd geoLatitude) (cosd declination))) (* (tand geoLatitude) (tand declination))))))  
(def HAsunRise (HAw zenithSunriseSunset))
(def HAcivilTwilight (HAw zenithCivilTwilight))
(def HAnautical (HAw zenithNautical))

(def (solZenith latit declinat hourAngl) 
     (toDegrees (acos (+ (* (sind latit) (sind declinat))
                         (* (cosd latit) (cosd declinat) (cosd hourAngl))))))

; Daylength
(define dayLength (/ HAsunRise 180.))

; Noon time
(def noonTime (/ (+ (- 720. (* 4 geoLongitude)  (eqOfTime centEpoc)) (* 60 timeZone)) 1440.))

; True Solar Time
(def TrueSolarTime (+ runMins (eqOfTime centEpoc) (- (* 4 geoLongitude) (* 60 timeZone)))) ; OK 

(def hourAngle (- (/ TrueSolarTime 4.0) 180))
(def noonZenith (solZenith geoLatitude declination hourAngle))
(def solarElevation (- 90.0 noonZenith))

; Atmospheric refraction as function of solar elevation
(def atRefract (lambda (solElevat)
                    (cond
                      ((> solElevat 85.0) 0.0)
                      
                      ((> solElevat 5.0) (/ (+ (- (/ 58.1 (tand solElevat)) (/ 0.07 (expt (tand solElevat) 3)))
                        (/ 0.000086 (expt (tand solElevat) 5))) 3600))  ; -> 0.11412 OK
                      
                      ((> solElevat -0.575) (/ (+ 1735 (* solElevat (- (* solElevat (+ 103.4 (* solElevat (- (* solElevat 0.711) 12.79)))) 518.2))) 3600)) ; -> 0.16524 OK
                      (else (/ -20.772 (tand solElevat) 3600))  ; -> 0.4286 OK
                      )))


; calculate refraction corrected elevation
(def correctedElevation (+ solarElevation (atRefract solarElevation)))


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
(define sunsetAzimuth (Azimuth HAsunRise geoLatitude zenithSunriseSunset declination))
(define sunriseAzimuth (Azimuth (- HAsunRise 180.) geoLatitude zenithSunriseSunset declination))


(def AMnauticalTwilightTime (- noonTime (/ HAnautical 360.)))    ; Before Sunrise Nautical Twilight time
(def AMcivilTwilightTime (- noonTime (/ HAcivilTwilight 360.)))  ; Before Sunrise Civil Twilight time
(def sunriseTime (- noonTime (/ HAsunRise 360.)))                ; Sunrise time
(def sunsetTime  (+ noonTime (/ HAsunRise 360.)))                ; Sunset time
(def PMcivilTwilightTime (+ noonTime (/ HAcivilTwilight 360.)))  ; After Sunset Civil Twilight time
(def PMnauticalTwilightTime (+ noonTime (/ HAnautical 360.)))    ; After Sunset Nautical Twilight time 

