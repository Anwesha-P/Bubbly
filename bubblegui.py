"""CS 108 Final Project

This module implements the GUI of the SquareBubble to make an interactive game called Bubbly-2048.

After the Project 3 - Walkthrough, I have added a method - check_new_win(), pop-up windows,
a separate window for the leaderboard and different methods related to the leaderboard.

@author: Anwesha Pradhananga (ap45)
@date: Fall, 2021
"""

from guizero import App, Drawing, PushButton, Box, Text, Window
from bubble import SquareBubble


class BubblesGUI:
    """BubblesGUI runs a simulation of the SquareBubbles and makes it interative as a game."""

    def __init__(self, app):
        """Instantiate the simulation GUI app."""
        
        app.title = 'Bubble-2048'
        UNIT = 500
        CONTROL_UNIT = 50
        TITLE_UNIT = 125
        SHOOTER_UNIT = 15
        SQUARE_UNIT = 100

        app.width = UNIT
        app.height = UNIT + CONTROL_UNIT + TITLE_UNIT + SHOOTER_UNIT + SQUARE_UNIT
        
        # Add the widgets.
         
        box_header = Box(app, layout = 'grid', width = UNIT, height = TITLE_UNIT )
        
        name = Text(box_header, text = "BUBBLY-2048", size =  31, font = "Bubble Bobble", grid = [0,0,1,3])     
       
        menu = Box(box_header, layout = 'grid', grid = [1,0,5,1], align = "right")
        
        high = PushButton(menu, text = "Scores", grid = [1,0], align = "top", pady = 1, command = self.show)
        PushButton(menu, image = 'reset.png', grid = [2,0], width = 30, height = 30, command = self.reset)
        Text(menu, text = "Reset", size = 8, grid = [2,1])
        PushButton(menu, image = 'save.png', grid = [3,0], width = 30, height = 30, command = self.save_game)
        Text(menu, text = "Save", size = 8, grid = [3,1])
        PushButton(menu, image = 'open.png', width = 30, height = 30, grid = [4,0], command = self.open_game)
        Text(menu, text = "Open", size = 8, grid = [4,1])
        PushButton(menu, image = 'quit.png', width = 30, height = 30, grid = [5,0], command = self.quit_game)
        Text(menu, text = "Quit", size = 8, grid = [5,1])
        
        Text(box_header, text="Score  ", font = "TypoGraphica", size = 14, grid = [2,1])
        Text(box_header, text = "Best", font = "TypoGraphica", size = 14, grid = [3,1], align = "right")
        
        self.total_score = Text(box_header, text = '0', size = 13,  grid = [2,2])
        self.best_score = Text(box_header, text = '0', size = 13, grid = [3,2])
        
        box_shooter = Box(app, layout = 'grid', width = UNIT, height = SHOOTER_UNIT)
        self.shooter = Drawing(box_shooter, width = UNIT, height = SHOOTER_UNIT, grid = [0,0])
        self.shooter.line(0,0,UNIT,1, color = "black", width = 6)
        self.shooter.polygon((UNIT/2 - (3*SQUARE_UNIT)/4), 0, (UNIT/2) - (SQUARE_UNIT/2), SHOOTER_UNIT, (UNIT/2) + (SQUARE_UNIT/2), SHOOTER_UNIT, (UNIT/2) + ((3*SQUARE_UNIT)/4), 0, color="black")
        
        self.drawing = Drawing(app, width = UNIT, height = UNIT + SQUARE_UNIT)
        self.drawing.bg = "black"
        
        box_control = Box(app, layout = 'grid', width = UNIT, height = CONTROL_UNIT)      
        PushButton(box_control, text = "          <——          ", grid = [0,0], command = self.shift_left) 
        self.drop_pushbtn = PushButton(box_control, text = "                 Drop                 ", grid = [1,0], command = self.drop_init) 
        PushButton(box_control, text = "          ——>          ", grid = [2,0], align = "left", command = self.shift_right) 
        
        self.open_bestscore()

        app.when_key_pressed = self.key_pressed
        
        self.name = app.question("Name", "Please type your name:")
        
        #Leaderboard Window
        
        window.title = "Leaderboard"
        
        Text(window, text = "Leaderboard Scores", size =  20, font = "Bubble Bobble")
        Text(window, text = "——————————————————", size = 20)

        ranks = Box(window, layout = "grid")
        Text(ranks, text = "    Rank    ", font = "TypoGraphica", size = 16, grid = [0,0])
        Text(ranks, text = "    Name    ", font = "TypoGraphica", size = 16, grid = [1,0])
        Text(ranks, text = "    Score    ", font = "TypoGraphica", size = 16, grid = [2,0])
        Text(ranks, text = "    #1     ", size = 14, grid = [0,1])
        Text(ranks, text = "    #2     ", size = 14, grid = [0,2])
        Text(ranks, text = "    #3     ", size = 14, grid = [0,3])
        
        score = self.open_leaderboard()
        self.rank_name1 = Text(ranks, text = str(score[0][1]), grid = [1,1])
        self.rank_score1 = Text(ranks, text = str(score[0][0]) , grid = [2,1])
        self.rank_name2 = Text(ranks, text = str(score[1][1]), grid = [1,2])
        self.rank_score2 = Text(ranks, text = str(score[1][0]) , grid = [2,2])
        self.rank_name3 = Text(ranks, text = str(score[2][1]), grid = [1,3])
        self.rank_score3 = Text(ranks, text = str(score[2][0]) , grid = [2,3])
        
        self.close = PushButton(window, text = "close", align = "top", command = window.hide)

        #Initializing variables
        self.bubble_drop = False
        self.highest_score = 2
        self.sq_bubbles_list = []
        
        self.add_particle()
        
        self.draw_frame()
        
        
    def show(self):
        """Displays the window widget."""
        
        window.show()
        
        
    def draw_frame(self):
        """Draws every bubble in the list and also checks for merges and if the game is over."""
    
        self.drawing.clear()
        self.merge()  

        for bubbles in self.sq_bubbles_list:
            bubbles.draw(self.drawing)
        self.game_over()
                       
 
    def merge(self):
        """This method calls different methods after certain conditions are met."""
        
        if self.b.y > 50:
            self.fly()

            for i in range(len(self.sq_bubbles_list) - 1):
                
                if self.b.check_end(self.drawing) or self.b.stacked_up(self.sq_bubbles_list[i]):
                    self.check_hit_self()
                    self.check_hit_others()
                    self.fly()
                
    
    def fly(self):
        """This method checks if a bubble is flying (not in the bottom row or not stacked up)."""
        
        for i in range(len(self.sq_bubbles_list) - 1):
            count = 0

            for j in range(i):
                if self.sq_bubbles_list[i] != (self.sq_bubbles_list[j]):
                    if self.sq_bubbles_list[i].stacked_up(self.sq_bubbles_list[j]):
                        count +=1
                        break
                    
            if count == 0:
                if self.sq_bubbles_list[i].check_end(self.drawing) == False:
                    self.sq_bubbles_list[i].y += 100
        
                    
    def check_hit_self(self):
        """This method checks if the bubble being dropped is hitting any other bubble in the list.
        It then doubles the score and changes the color of the bubble, and removes the bubble that was hit."""
        
        for bubble in self.sq_bubbles_list:           
        
            if self.b.hits(bubble):
                if self.b.score == bubble.score:
                    
                    self.total_score.value = str(int(self.total_score.value) + (self.b.score * 2))
                    if int(self.total_score.value) > int(self.best_score.value):
                        self.best_score.value = self.total_score.value
                    self.b.score *= 2
                    self.b.color = self.b.get_score_color(self.b.score)
                    self.sq_bubbles_list.remove(bubble)
                    
                    if self.b.score > self.highest_score:
                        self.highest_score = self.b.score
                        self.check_new_win()
                                                
                elif self.b.x == bubble.x:
                    self.b.y = bubble.y - 100
             
   
    def check_hit_others(self):
        """This method checks if one bubble in the list is hitting any other bubble in the list.
        It then doubles the score and changes the color of the bubble, and removes the bubble that was hit."""
        
        for i in range(len(self.sq_bubbles_list) - 1):
            for j in range(i):
                if self.sq_bubbles_list[i].hits(self.sq_bubbles_list[j]):
                    
                    if self.sq_bubbles_list[i].score == self.sq_bubbles_list[j].score:
                        self.total_score.value = str(int(self.total_score.value) + (self.b.score * 2))
                        if int(self.total_score.value) >= int(self.best_score.value):
                            self.best_score.value = self.total_score.value
                        self.sq_bubbles_list[i].score *= 2
                                    
                        self.sq_bubbles_list[i].color = self.b.get_score_color(self.sq_bubbles_list[i].score)
                        self.sq_bubbles_list.remove(self.sq_bubbles_list[j])
                        self.fly()
                                                
                        if self.sq_bubbles_list[i].score > self.highest_score:
                            self.highest_score = self.sq_bubbles_list[i].score
                            self.check_new_win()
                            
                            
    def game_over(self):
        """This method checks if the game is over by looking if the bubbles are stacked up
            in any of the columns. It also allows the user to restart the game, saves the bestscore
            and displays the leaderboard."""
        
        stacked = 0
        for b in range(len(self.sq_bubbles_list) - 1):
            if self.sq_bubbles_list[b].full_column(self.drawing):
                stacked += 1
        if stacked!= 0:
            app.warn("Game", "Game Over!!!")
            if not self.reset():
                self.save_bestscore()
                self.leaderboard()
                self.show()
                window.after(3000, window.hide)
                app.after(4000, app.destroy)
            
    
    def check_new_win(self):
        """This method displays a congratulatory message if the user achieves a score higher than 1024
            and a special message if 2048 is formed"""
        
        if self.highest_score == 2048:
            app.info("Congratulations!", "A 2048 bubble formed!")
            
        elif self.highest_score >= 1024:
            app.info("New Achievement!", "Woah! You formed a high scoring bubble - {}".format(self.highest_score))
        
     
    def key_pressed(self, event):
        """This method calls different methods according to the different event data (here, keys)."""

        key = event.tk_event.keysym

        if key == "space":
            self.drop_init()
        elif key == "Left":
            self.shift_left()
        elif key == "Right":
            self.shift_right()

               
    def shift_left(self):
        """This method calls the instance method move_sideways() to move the bubble to the left before it's dropped.""" 

        if self.bubble_drop == False:
            self.b.move_sideways(self.drawing, "-")
            self.draw_frame()     
    
    
    def shift_right(self):
        """This method calls the instance method move_sideways() to move the bubble to the right before it's dropped."""
        
        if self.bubble_drop == False:
            self.b.move_sideways(self.drawing, "+")
            self.draw_frame()


    def drop_init(self):
        """This method starts a repeated call to drop() method"""
        
        app.repeat(20, self.drop)
    
    
    def drop(self):
        """This method moves the square bubble downwards and adds a new bubble to the list
        if the present bubble stacks up on other bubble or reaches the bottom row.
        """
        
        self.b.move_down(self.drawing)
        self.draw_frame()
        self.bubble_drop = True
        
        #Checks if the bubble reached the end of the canvas and stops the repeat call command to the drop() method.
        if self.b.check_end(self.drawing): 
            self.drop_pushbtn.cancel(self.drop)
            self.merge()
            self.add_particle()
            self.draw_frame()
            
        #Checks if any bubble is stacked up on any other bubble and stops the repeat call command to the drop() method.               
        for i in range(len(self.sq_bubbles_list) - 1): # FIXME tyo utpatyang
            if self.b.x == self.sq_bubbles_list[i].x and self.b.stacked_up(self.sq_bubbles_list[i]):
                self.drop_pushbtn.cancel(self.drop)
                self.merge()
                self.add_particle()
                self.draw_frame()
              
              
    def reset(self):
        """This method resets the game to the starting position."""
        
        confirm = app.yesno("New Game", "Do you want to start a new game?")
        if confirm == True:
            self.leaderboard()
            self.show()
            window.after(3000, window.hide)
            self.save_bestscore()
            
            self.highest_score = 2
            self.sq_bubbles_list = []
            self.total_score.value = '0'
            self.drawing.clear()
            self.add_particle()
            self.draw_frame()
            self.open_bestscore()
        
        return confirm


    def save_game(self):
        """This method writes the positions and scores of all Square Bubbles into savescore.txt file."""
        
        game_score = open("savescore.txt", "w")
        game_score.write(self.total_score.value)
        game_score.close()
        
        clear_file = open("savegame.txt", "w")
        clear_file.close()
        
        game_data = open("savegame.txt", "a")   
        for i in range(len(self.sq_bubbles_list) - 1):
            game_data.write(str(self.sq_bubbles_list[i].x) + "," + str(self.sq_bubbles_list[i].y) + "," + str(self.sq_bubbles_list[i].score) + "\n")
        
        game_data.close()
        
        app.info("Save", "Current game saved!")
       
       
    def open_game(self):
        """This method reads the positions and scores of all Square Bubbles from savescore.txt file."""
        
        confirm = app.yesno("Confirm", "You will lose your current progress. Do you want to continue opening the previously saved game?")
        if confirm:
            
            game_score = open("savescore.txt", "r")
            score = game_score.read()
            self.total_score.value = score
            
            game_score.close()
            
            game_data = open("savegame.txt", "r")
            game_state = game_data.readlines()
            
            self.sq_bubbles_list = []
            scores = []
            
            for state in game_state:
                state = state.split(",")          
                t = SquareBubble(x = int(state[0]), y = int(state[1]))
                t.score = int(state[2])
                t.color = t.get_score_color(t.score)
                self.sq_bubbles_list.append(t)
            
            self.add_particle()
            self.draw_frame()  
    
    
    def quit_game(self):
        """This method allows the user to quit the game and saves the highest score
            and displays the leaderboard."""
        
        confirm = app.yesno("Quit", "Do you really want to quit the game?")
        
        if confirm == True:
            self.save_bestscore()
            self.leaderboard()
            self.show()
            window.after(5000, window.hide)
            app.after(7000, app.destroy)
        
    
    def save_bestscore(self):
        """This method saves the bestscore of the game in bestscore.txt file."""

        best_score = open("bestscore.txt", "w")
        best_score.write(self.best_score.value)
        best_score.close()
    
    
    def open_bestscore(self):
        """This method opens bestscore.txt file to retrieve the bestscore of the game.
            It also creates a new file if there is no file to read from.
            """
        
        try:
            best_score = open("bestscore.txt")
            self.best_score.value = best_score.read()
            best_score.close()
        except:
            #Creates a file if it doesn't exist
            best_score = open("bestscore.txt","w")
            best_score.close()
            
            best_score = open("bestscore.txt")
            self.best_score.value = best_score.read()
            best_score.close()
            
    
    def leaderboard(self):
        """Updates ranks in the leaderboard."""
        
        self.rank_list = [[int(self.rank_score1.value), self.rank_name1.value], [int(self.rank_score2.value), self.rank_name2.value],[int(self.rank_score3.value), self.rank_name3.value]]
        self.rank_list.append([int(self.total_score.value), self.name])
        
        self.rank_list.sort(reverse = True)
        self.rank_list.pop()
        
        while "\n" in self.rank_list:
            self.rank_list.remove("\n")
        
        self.rank_score1.value = str(self.rank_list[0][0])
        self.rank_name1.value = self.rank_list[0][1]
        self.rank_score2.value = str(self.rank_list[1][0])
        self.rank_name2.value = self.rank_list[1][1]
        self.rank_score3.value = str(self.rank_list[2][0])
        self.rank_name3.value = self.rank_list[2][1]
        
        self.save_leaderboard()
        self.open_leaderboard()
    
    
    def save_leaderboard(self):
        """Writes ranks to the leaderboard.txt file."""
        
        leaderboard = open("leaderboard.txt","w")
        
        leaderboard.write(self.rank_score1.value + "," + self.rank_name1.value + "\n")
        leaderboard.write(self.rank_score2.value + "," + self.rank_name2.value  + "\n")
        leaderboard.write(self.rank_score3.value + "," + self.rank_name3.value )
        leaderboard.close()


    def open_leaderboard(self):
        """Reads ranks from leaderboard.txt file."""
        
        try:
            leaderboard = open("leaderboard.txt")
        except:
            #Creates a file if it doesn't exist
            leaderboard = open("leaderboard.txt", "w")
            
            leaderboard.write("0" + "," + "" + "\n")
            leaderboard.write("0" + "," + "" + "\n")
            leaderboard.write("0" + "," + "")
            leaderboard.close()
            
            leaderboard = open("leaderboard.txt")
            
        scores = leaderboard.readlines()
        leaderboard.close()
        ranks_list = []
        for s in scores:    
            s = s.strip().split(",")
            ranks_list.append(s)
        return ranks_list
            
            
    def add_particle(self):
        """This method adds a new square bubble to the list and assigns False to self.bubble_drop."""
        
        self.b = SquareBubble(max = self.highest_score)
        self.sq_bubbles_list.append(self.b)
        self.bubble_drop = False
                
      
app = App()
window = Window(app, width = 300, height = 300)
window.hide()
BubblesGUI(app)
app.display()




