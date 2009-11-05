function arrow(args)
var=subwrd(args,1)
xrit=subwrd(args,2)
ybot=subwrd(args,3)
len=subwrd(args,4)
scale=subwrd(args,5)
unit=subwrd(args,6)
'set arrowhead 0.09'
'set arrscl 'len' 'scale
'set arrlab off'
'd 'var
x = xrit-0.25
y = ybot+0.2
'set line 1 1 4'
'draw line 'x-len/2.' 'y' 'x+len/2.' 'y
'draw line 'x+len/2.-0.05' 'y+0.025' 'x+len/2.' 'y
'draw line 'x+len/2.-0.05' 'y-0.025' 'x+len/2.' 'y
'set string 1 c'
'set strsiz 0.1'
'draw string 'x' 'y+0.4' VECTOR'
'draw string 'x' 'y+0.2' 'scale' 'unit
