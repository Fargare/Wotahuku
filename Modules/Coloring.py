import Image,ImageTk
#from Tkinter import *
import colorsys

#Base Color RGB
red = [204,0,0] #0
orange = [255,183,76] #1
yellow= [255,255,0]#2
green = [40,175,12]#3
pink = [239,143,15]#4
#brown = [124,96,53]#5
blue = [40,47,203]#6
purple = [135,0,204]#7
white = [220,220,220]#8
black = [0,0,0]#9
#gray = [80,80,80]#10

colors = []
colors.append(["red",red])
colors.append(["orange",orange])
colors.append(["yellow",yellow])
colors.append(["green",green])
colors.append(["pink",pink])
#colors.append(["brown",brown])
colors.append(["blue",blue])
colors.append(["purple",purple])
colors.append(["white",white])
colors.append(["black",black])
#colors.append(["gray",gray])

def Call_Colors():
    return colors

def HtoRGB(H):
    rgb = [0]*3
    if H>=0 and H<=60:
        rgb[0] = 255
        rgb[1] =  int((float(H)/60)*255)
        rgb[2] = 0
    elif H>60 and H<=120:
        rgb[0] = int(((120-float(H))/60)*255)
        rgb[1] = 255
        rgb[2] = 0
    elif H>120 and H<=180:
        rgb[0] = 0
        rgb[1] = 255
        rgb[2] = int(((float(H)-120)/60)*255)
    elif H>180 and H<=240:
        rgb[0] = 0
        rgb[1] = ((240-float(H))/60)*255
        rgb[2] = 255
    elif H>240 and H<=300:
        rgb[0] = int(((float(H)-240)/60)*255)
        rgb[1] = 0
        rgb[2] = 255
    elif H>300 and H<=360:
        rgb[0] = 255
        rgb[1] = 0
        rgb[2] = int(((360-float(H))/60)*255)
    return rgb

def color_pick(image,part):
    px = image.load()
    top = px[1,1]
    #self.rgb = px[1,1]
    
    if top[0]>top[1] and top[0]>top[2]:
        self.H=int(60*(float(top[1]-top[2])/float(max(top)-min(top))))
    elif top[1]>top[2] and top[1]>top[0]:
        self.H=int(60*(float(top[2]-top[0])/float(max(top)-min(top))))+120
    elif top[2]>top[0] and top[2]>top[1]:
        self.H=int(60*(float(top[0]-top[1])/float(max(top)-min(top))))+240
    if self.H<0:
        self.H+=360
    #print self.H,top

def judge_colors(rgb):
    colornum = 0
    mindist = 100
    
    RGB = [float(rgb[0])/255,float(rgb[1])/255,float(rgb[2])/255]
    #print "judge",RGB
    #print "original color",rgb,RGBtoXYZ(RGB),XYZtoLab(RGBtoXYZ(RGB))
    for i in range(len(colors)):
        distance = 0
        
        Color = [float(colors[i][1][0])/255,float(colors[i][1][1])/255,float(colors[i][1][2])/255]
        #print "color",i,Color,RGBtoXYZ(Color),XYZtoLab(RGBtoXYZ(Color))
        for j in range(3):
            distance+=(Color[j]-RGB[j])**2

        #print colors[i][0],distance
        #print i,distance
        if distance < mindist:
            mindist = distance
            colornum = i
    #print colornum
    return colors[colornum][0]

def collect_color(rgb):
    #from RGB to HSV
    #print "collect_before",rgb
    hsv = [0]*3
    if rgb[0]>rgb[1] and rgb[0]>rgb[2]:
        hsv[0]=int(60*(float(rgb[1]-rgb[2])/float(max(rgb)-min(rgb))))
    elif rgb[1]>rgb[2] and rgb[1]>rgb[0]:
        hsv[0]=int(60*(float(rgb[2]-rgb[0])/float(max(rgb)-min(rgb))))+120
    elif rgb[2]>rgb[0] and rgb[2]>rgb[1]:
        hsv[0]=int(60*(float(rgb[0]-rgb[1])/float(max(rgb)-min(rgb))))+240
    if hsv[0]<0:
        hsv[0]+=360
    
    hsv[1] = int(float(max(rgb)-min(rgb)/max(rgb)))
    hsv[2] = max(rgb)
    #print "HSV",hsv
    #collect V (+30)
    hsv[2]+=70
    if hsv[2]>255:
        hsv[2]=255

    #from HSV to RGB
    MAX = hsv[2]
    MIN = MAX-int((float(hsv[1])/255)*MAX)
    RGB = [0]*3
    if hsv[0]>=0 and hsv[0]<=60:
        RGB[0] = MAX
        RGB[1] =  int((float(hsv[0])/60)*(MAX-MIN))+MIN
        RGB[2] = MIN
    elif hsv[0]>60 and hsv[0]<=120:
        RGB[0] = int(((120-float(hsv[0]))/60)*(MAX-MIN))+MIN
        RGB[1] = MAX
        RGB[2] = MIN
    elif hsv[0]>120 and hsv[0]<=180:
        RGB[0] = MIN
        RGB[1] = MAX
        RGB[2] = int(((float(hsv[0])-120)/60)*(MAX-MIN))+MIN
    elif hsv[0]>180 and hsv[0]<=240:
        RGB[0] = MIN
        RGB[1] = ((240-float(hsv[0]))/60)*(MAX-MIN)+MIN
        RGB[2] = MAX
    elif hsv[0]>240 and hsv[0]<=300:
        RGB[0] = int(((float(hsv[0])-240)/60)*(MAX-MIN))+MIN
        RGB[1] = MIN
        RGB[2] = MAX
    elif hsv[0]>300 and hsv[0]<=360:
        RGB[0] = MAX
        RGB[1] = MIN
        RGB[2] = int(((360-float(hsv[0]))/60)*(MAX-MIN))+MIN
    #print "collect_after",RGB
    return RGB

def collect_color2(rgb):
    RGB_b = [float(rgb[0])/255,float(rgb[1])/255,float(rgb[2])/255]
    #print "collect!!!!!!!!!!!!!!"
    #print rgb
    #print RGB_b
    hsv = list(colorsys.rgb_to_hsv(RGB_b[0],RGB_b[1],RGB_b[2]))
    #print hsv
    hsv[2]+=0.1
    #print hsv
    RGB_a = list(colorsys.hsv_to_rgb(hsv[0],hsv[1],hsv[2]))
    RGB = [int(RGB_a[0]*255),int(RGB_a[1]*255),int(RGB_a[2]*255)]
    return RGB

def RGBtoXYZ(rgb):
    xyz = [0]*3
    xyz[0]=0.436041*float(rgb[0])+0.385113*float(rgb[1])+0.143046*float(rgb[2])
    xyz[1]=0.222485*float(rgb[0])+0.716905*float(rgb[1])+0.060610*float(rgb[2])
    xyz[2]=0.019465*float(rgb[0])+0.097067*float(rgb[1])+0.713913*float(rgb[2])
    return xyz

def XYZtoLab(xyz):
    lab = [0]*3
    lab[0]=116*Lab_ft(xyz[1]/1.0)-16
    lab[1]=500*(Lab_ft(xyz[0]/0.9642)-Lab_ft(xyz[1]/1.0000))
    lab[2]=200*(Lab_ft(xyz[1]/1.0000)-Lab_ft(xyz[2]/0.8249))
    return lab

def Lab_ft(t):
    if t>0.008856:
        return t**(1.0/3.0)
    else:
        return (1.0/3.0)*((29.0/6.0)**2)*t+(4.0/29.0)
