def rgb2lab(inputColor):

    num = 0
    RGB = [0, 0, 0]

    for value in inputColor:
        value = float(value) / 255

        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value = value / 12.92

        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0, ]

    X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
    Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
    Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
    XYZ[0] = round(X, 4)
    XYZ[1] = round(Y, 4)
    XYZ[2] = round(Z, 4)

    # Observer= 2°, Illuminant= D65
    XYZ[0] = float(XYZ[0]) / 95.047         # ref_X =  95.047
    XYZ[1] = float(XYZ[1]) / 100.0          # ref_Y = 100.000
    XYZ[2] = float(XYZ[2]) / 108.883        # ref_Z = 108.883

    num = 0
    for value in XYZ:

        if value > 0.008856:
            value = value ** (0.3333333333333333)
        else:
            value = (7.787 * value) + (16 / 116)

        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]

    L = (116 * XYZ[1]) - 16
    a = 500 * (XYZ[0] - XYZ[1])
    b = 200 * (XYZ[1] - XYZ[2])

    Lab[0] = round(L, 4)
    Lab[1] = round(a, 4)
    Lab[2] = round(b, 4)
    
    print(Lab)
    return Lab

def lab_to_xyz(lab):
    l   = lab[0]
    a   = lab[1]
    b   = lab[2]

    ill = [95.0489, 100, 108.8840]
    sl  = (l + 16) / 116
    x   = ill[0] * finv(sl + (a/500))
    y   = ill[1] * finv(sl)
    z   = ill[2] * finv(sl-(b/200))
    return x, y, z

def finv(t):
    ratio = (6.0/29.0)
    if t>ratio:
        t= t*t*t
    else:
        t=(3.0*ratio*ratio*(t - (4.0/29.0)))
    return t

def xyz_to_rgb(xyz):

  x  = xyz[0]
  y  = xyz[1]
  z  = xyz[2]

  rl = (3.2406*x) - (1.5372*y) - (0.4986*z)
  gl = (-0.9689*x) + (1.8758*y) + (0.0415*z)
  bl = (0.0557*x ) - (0.2040*y) + (1.0570*z)

  clip = (rl<0.0 or rl>1.0 or gl<0.0 or gl>1.0 or bl<0.0 or bl>1.0)

  if clip:
    if (rl<0.0):
        rl =0.0
    elif (rl>1.0):
        rl=1.0
    if (gl<0.0):
        gl =0.0
    elif (gl>1.0):
        gl=1.0
    if (bl<0.0):
        bl =0.0
    elif (bl>1.0):
        bl=1.0

  r = 255.0 * correct(rl)
  g = 255.0 * correct(gl)
  b = 255.0 * correct(bl)

  return r, g, b



def correct(c):
    a = 0.055
    if (c<=0.0031308):
        return (12.92*c)
    else:
        return ((1 + a) * (c**(1/2.4)) - a)


l,a,b = rgb2lab([50,75,120])
x,y,z = lab_to_xyz([l,a,b])
print("x: {} y: {} z: {}".format(x,y,z))
r,g,b = xyz_to_rgb([x,y,z])
print("r: {} g: {} b: {}".format(r,g,b))