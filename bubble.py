"""CS 108 Final Project

This module implements the model of the SquareBubble.

@author: Anwesha Pradhananga (ap45)
@date: Fall, 2021
"""
import random

class SquareBubble:
    """SquareBubble models a single square bubble and its possible actions."""

    def __init__(self, max = 2, x = 250, y = 50, vel_y = 12):
        """Instantiate a SquareBubble object with max, x and y coordinates, and a velocity y."""
       
        self.x = x
        self.y = y
        self.vel_y = vel_y
        
        possible_scores = [2]
        i = 4
        while i < max:
            possible_scores.append(i)
            i *= 2
        
        #assigns a random score to the SquareBubble instance and a color based on on that score.
        self.score = random.choice(possible_scores)
        self.color = self.get_score_color(self.score)
        
        self.square_size = 100
   
   
    def draw(self, drawing):
        """This method draws a rounded square using 4 circles and 2 rectangles with the given specifications."""
        
        self.circle1 = drawing.oval(self.x - int(self.square_size / 2), self.y - int(self.square_size / 2), self.x, self.y, color = self.color)
        self.circle2 = drawing.oval(self.x, self.y - int(self.square_size / 2), self.x + int(self.square_size / 2), self.y, color = self.color)
        self.circle3 = drawing.oval(self.x - int(self.square_size / 2), self.y, self.x, self.y + int(self.square_size / 2), color = self.color)
        self.circle4 = drawing.oval(self.x, self.y, self.x + int(self.square_size / 2), self.y + int(self.square_size / 2), color = self.color)
        
        self.rectangle1 = drawing.rectangle(self.x - int(self.square_size / 2), self.y - int(self.square_size / 4), self.x + int(self.square_size / 2) + 1, self.y + int(self.square_size / 4), color = self.color)
        self.rectangle2 = drawing.rectangle(self.x - int(self.square_size / 4), self.y - int(self.square_size / 2), self.x + int(self.square_size / 4), self.y + int(self.square_size / 2) + 1, color = self.color)
        
        #Changes the position and font of the text based on its number of digits.
        if self.score < 10:
            xoffset = 16
            fontsize = 36
        elif self.score < 100:
            xoffset = 32
            fontsize = 36
        elif self.score < 1000:
            xoffset = 38
            fontsize = 30
        elif self.score < 10000:
            xoffset = 45
            fontsize = 25
        else:
            xoffset = 55
            fontsize = 20
        
        #Adds a guitext in the square bubble
        self.guitext = drawing.text(self.x-xoffset,self.y-32,str(self.score),color="white", size = fontsize)
        
    
    def get_score_color(self, score):
        """This method assigns score_color according to the scores in the bubble."""
        
        if score == 2:
            score_color = "#FF00AC"
        elif score == 4:
            score_color = "#8C00FF"
        elif score == 8:
            score_color = "#FAFF2B"        
        elif score == 16:
            score_color = "#0066FF"        
        elif score == 32:
            score_color = "#26FF00"        
        elif score == 64:
            score_color = "#FF0000"        
        elif score == 128:
            score_color = "#FF87AB"        
        elif score == 256:
            score_color = "#B8B8FF"        
        elif score == 512:
            score_color = "#90F1EF"        
        elif score == 1024:
            score_color = "#FFFF9F"        
        elif score == 2048:
            score_color = "#B2FF9E"        
        elif score == 4096:
            score_color = "#D100D1"        
        elif score == 8192:
            score_color = "#00F5D4"
        elif score == 16384:
            score_color = "#EA3966"
        else:
            score_color = "#FFFFFF"

        return score_color


    def distance(self, x1, y1, x2, y2):
        """ Compute the distance between two points."""
        
        return abs(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)
    
    
    def move_down(self, drawing):
        """This method moves the square bubble by increasing the y velocity until it reaches the bottom row of the drawing canvas."""
        
        if self.y < drawing.height - int(self.square_size / 2):
            self.y += self.vel_y            
    
    
    def move_sideways(self,drawing, magnitude):
        """This method moves the square bubble sideways depending on the magnitude until it touches any of the walls."""
        
        if magnitude == "+":
            if self.x < drawing.width - int(self.square_size / 2):
                self.x += 100
                
        elif magnitude == "-":
            if self.x > int(self.square_size / 2):
                self.x -= 100
                
                
    def check_end(self,drawing):
        """This method checks if the y coordinates of the square bubble is on the bottom row of the drawing canvas."""
        
        return self.y >= drawing.height - int(self.square_size / 2)
    
    
    def stacked_up(self,other):
        """This method checks if 'self' square bubble is on top of the 'other' square bubble."""
        
        if self == other:
            return False
        if self.x == other.x and self.y < other.y:
            return self.y >= other.y - self.square_size
        else:
            return False
    
    
    def hits(self, other):
        """This method checks if 'self' square bubble hits 'other' square bubble from any of the four directions."""
        
        if self == other:
            return False
        
        return self.distance(self.x, self.y, other.x, other.y) <= 100
    
    
    def full_column(self, drawing):
        """This method checks if the canvas is fully stacked up."""
        
        return self.y <= 150
    
    
    
