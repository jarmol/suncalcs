REM  *****  BASIC  *****
Sub Main

End Sub

Function daynr(anno as Integer, mon as Integer, dag as Integer) as Integer
      Dim N1 as Integer, N2 as Integer, N3 as Integer
      Dim q as Integer, qq as Integer, Nr as Integer
      N1 = Int(275*mon/9)
      N2 = Int((mon + 9.0)/12.0)
      q  = Int(anno/4)
      qq = 2 - 4*q + anno
      N3 = 1 + Int(qq/3) 
      Nr = N1 - N2*N3 + dag - 30
      daynr = Nr
	
End Function

Function suntime(longit as Double, dnr as Integer, w as Integer) as Double
't1 = N + (6 - lngHour) / 24
't2 = N + (18 - lngHour) / 24
	Dim t1 as Double, t as Double
	t1 = longit/15.0
	t1 = 6.0 - t1
	t1 = dnr + t1/24.0

	If (w=1) then
	   t = t1
	Elseif (w=2) then
	   t  = t1 + 0.5
	End if
	
	suntime = t
	
End Function

Function manom(ty as Double) as Double
' Mean anomaly of Sun
	Dim t2 as Double
	t2 = 0.9856*ty - 3.289
	manom = t2
	
End Function

function truelong(Mx as Double) as Double
' Calculate true longitude of Sun
' L = M+(1.916*sin(M))+(0.020*sin(2*M))+282.634
	Dim Lx as Double
	Dim LY as Double
	Dim Lz as Double

	Dim d2rad as Double
	d2rad = PI/180.0

	Lx = 1.916*sin(d2rad*Mx)
	Ly = 0.02*sin(2*d2rad*Mx)
	Ly = Lx + Ly + Mx + 282.634
	Lz = Ly - Int(Ly/360)*360
	truelong = Lz

End Function

Function sunra(L as Double) As Double
'RA = atan(0.91764 * tan(L))
	d2rad = PI/180.0
	Dim RA as Double
	x = atn(0.91764*tan(d2rad*L))
	RA = x/d2rad
	sunra = RA
End Function

Function RALquad(RA as Double, L as Double) As Double
	Lquadrant  = Int(L/90)*90
	Raquadrant = Int(RA/90)*90
	RA = RA + (Lquadrant - RAquadrant)
	RALquad = RA
End Function

