from multiprocessing import Pool
import sys
import os
import math
from cmath import *

#from fractalio_math import *

class Mandelbrot():
    def __init__(self, canvasW, canvasH, formula, x=-0.75, y=0, m=1.5, iterations=None, w=None, h=None, zoomFactor=.1, buildAsJulia=False, jX=-1, jY=0.0):
        self.buildAsJulia = buildAsJulia
        self.jX = jX
        self.jY = jY

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

        self.formula = formula
        self.CalculateFunc = eval("lambda Z, C: " + formula)

    def setNewCanvasSize(self, canvasW, canvasH, resolution):
        self.canvasW = canvasW
        self.canvasH = canvasH
        self.w = resolution
        self.h = resolution

        if canvasW > canvasH:
            self.xDelta = self.delta/(canvasH/canvasW)
            self.yDelta = self.delta
        else:
            self.yDelta = self.delta/(canvasW/canvasH)
            self.xDelta = self.delta
        self.yScaleFactor = self.h/canvasH
        self.xScaleFactor = self.w/canvasW

        self.xmin = self.xCenter - self.xDelta
        self.xmax = self.xCenter + self.xDelta
        self.ymin = self.yCenter - self.yDelta
        self.ymax = self.yCenter + self.yDelta

    def setNewArguments(self, formula, x, y, m):
        self.xCenter, self.yCenter = x, y
        self.delta = m
        self.c, self.z = 0, 0

        if self.canvasW > self.canvasH:
            self.xDelta = self.delta/(self.canvasH/self.canvasW)
            self.yDelta = self.delta
        else:
            self.yDelta = self.delta/(self.canvasW/self.canvasH)
            self.xDelta = self.delta
        self.yScaleFactor = self.h/self.canvasH
        self.xScaleFactor = self.w/self.canvasW

        self.xmin = self.xCenter - self.xDelta
        self.xmax = self.xCenter + self.xDelta
        self.ymin = self.yCenter - self.yDelta
        self.ymax = self.yCenter + self.yDelta

        self.formula = formula
        self.CalculateFunc = eval("lambda Z, C, x, y: " + formula)

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
        self.xCenter = x#translate(event.x*self.xScaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = y#translate(event.y*self.yScaleFactor, self.h, 0, self.ymin, self.ymax)
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

        coordinates = []
        for x in range(self.w):
            for y in range(self.h):
                coordinates.append((x, y))
        pixels = []
        for coord in coordinates:
            pixels.append(self.getEscapeTime(coord[0], coord[1]))
        self.pixels = pixels

    def getEscapeTime(self, x, y):
        re = translate(x, 0, self.w, self.xmin, self.xmax)
        im = translate(y, 0, self.h, self.ymax, self.ymin)

        z = complex(re, im)
        c = complex(re, im)

        if self.buildAsJulia:
            z = complex(re, im)
            c = complex(self.jX, self.jY)

        for i in range(1, self.iterations):
            
            if abs(z) > 2:
                return (x, y, i)

            try:
                z = self.CalculateFunc(z, c)
            except Exception as e:
                return (x, y, 0)

        return (x, y, 0)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)
