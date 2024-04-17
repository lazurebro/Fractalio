from multiprocessing import Pool
import sys
import os
import math
from cmath import *
import numpy as np
from PIL import Image, ImageDraw
import matplotlib
import matplotlib.cm
import matplotlib.pyplot

TOL = 1.e-8

def newton(z0, f, fprime, MAX_IT=1000):
    z = z0
    for i in range(MAX_IT):
        dz = f(z)/fprime(z)
        if abs(dz) < TOL:
            return z
        z -= dz

    return False

class NewtonRaphson():
    def __init__(self, canvasW, canvasH, exponent, f, fp, x=0, y=0, m=1.5, iterations=None, w=None, h=None, zoomFactor=.1, buildCustomFormulas=False, jX=-1, jY=0.0):
        self.buildCustomFormulas = buildCustomFormulas
        self.exponentFunc = eval("lambda: " + exponent)

        self.canvasW = canvasW
        self.canvasH = canvasH
        self.w, self.h = (round(canvasW*0.9), round(canvasH*0.9)) if None in {w, h} else w, h
        self.iterations = 256 if iterations is None else iterations
        self.xCenter, self.yCenter = x, y
        if canvasW > canvasH:
            self.xDelta = m/(canvasH/canvasW)
            self.yDelta = m
        else:
            self.yDelta = m/(canvasW/canvasH)
            self.xDelta = m
        self.delta = m
        self.xmin = x - self.xDelta
        self.xmax = x + self.xDelta
        self.ymin = y - self.yDelta
        self.ymax = y + self.yDelta
        self.zoomFactor = zoomFactor
        self.yScaleFactor = self.h/canvasH
        self.xScaleFactor = self.w/canvasW
        self.c, self.z = 0, 0

        self.f = eval("lambda Z: " + f)
        self.fp = eval("lambda Z: " + fp)

        self.defualt_f = lambda z: z**(self.exponentFunc()) - 1
        self.defualt_fp = lambda z: self.exponentFunc()*z**(self.exponentFunc()-1)

    def shiftView(self, event):
        self.xCenter = translate(event.x*self.xScaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y*self.yScaleFactor, self.h, 0, self.ymin, self.ymax)
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta

    def zoomOut(self, event):
        self.xCenter = translate(event.x*self.xScaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y*self.yScaleFactor, self.h, 0, self.ymin, self.ymax)
        self.xDelta /= self.zoomFactor
        self.yDelta /= self.zoomFactor
        self.delta /= self.zoomFactor
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta

    def zoomOutXY(self, x, y):
        self.xCenter = x
        self.yCenter = y
        self.xDelta /= self.zoomFactor
        self.yDelta /= self.zoomFactor
        self.delta /= self.zoomFactor
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta

    def zoomIn(self, event):
        self.xCenter = translate(event.x*self.xScaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y*self.yScaleFactor, self.h, 0, self.ymin, self.ymax)
        self.xDelta *= self.zoomFactor
        self.yDelta *= self.zoomFactor
        self.delta *= self.zoomFactor
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta

    def zoomInXY(self, x, y):
        self.xCenter = x
        self.yCenter = y
        self.xDelta *= self.zoomFactor
        self.yDelta *= self.zoomFactor
        self.delta *= self.zoomFactor
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta

    def getPixels(self):
        roots = []
        pixels = []

        def get_root_index(roots, r):
            try:
                return np.where(np.isclose(roots, r, atol=TOL))[0][0]
            except IndexError:
                roots.append(r)
                return len(roots) - 1

        for ix, x in enumerate(np.linspace(self.xmin, self.xmax, self.w)):
            for iy, y in enumerate(np.linspace(self.ymin, self.ymax, self.h)):
                try:
                    z0 = x + y*1j
                    r = None
                    if self.buildCustomFormulas == 0:
                        r=newton(z0, self.defualt_f, self.defualt_fp, MAX_IT=self.iterations)
                    else:
                        r=newton(z0, self.f, self.fp, MAX_IT=self.iterations)
                        
                    if r is not False:
                        ir = get_root_index(roots, r)
                        pixels.append((iy,ix,ir))
                except:
                    pixels.append((iy,ix,0))

        self.pixels = pixels
        self.MaxRoots = len(roots)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)
