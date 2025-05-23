from tkinter import *
import random
class Window:
    def __init__(self, master):
        self.master = master
        self.score = 0

        self.topFrame = Frame(self.master)
        self.bottomFrame = Frame(self.master)

        self.topFrame.pack()
        self.bottomFrame.pack()

        self.label = Label(self.topFrame, text=f"SCORE : {self.score}", font = ("Arial", 20, "bold"))
        self.label.pack()

        self.canvasWidth = 800
        self.canvasHeight = 700
        self.canvas = Canvas(self.topFrame, width=self.canvasWidth, height=self.canvasHeight)
        self.canvas.pack()

        self.restartButton = None

        self.bird = self.canvas.create_oval(150, 200, 200, 250, fill="yellow")

        self.canvas.focus_set()
        self.canvas.bind("<space>", self.jump)

        self.startGame()
        
        
    def jump(self, event):
        self.canvas.move(self.bird, 0, -80)

    def applyGravity(self):
        self.canvas.move(self.bird, 0, 5)
        self.gravityId = self.master.after(20, self.applyGravity)

    def movePipes(self):
        newPipes = []
        birdX1Coordinates = self.canvas.coords(self.bird)[0]

        for top, bottom, passed, scored in self.pipes:
            self.canvas.move(top, -4, 0)
            self.canvas.move(bottom, -4, 0)

            topPipeCoordinates = self.canvas.coords(top)
            
            if (topPipeCoordinates[2] < birdX1Coordinates and not(passed) and not(scored)):
                scored = True
                self.updateScore()
            
            if (topPipeCoordinates[2] > 0):
                newPipes.append((top, bottom, False, scored)) # false one is to ensure pipe moves till end but due to scored checking it wont add score continuously
            else:
                self.canvas.delete(top)
                self.canvas.delete(bottom)

        self.pipes = newPipes
        
        self.movePipeId = self.master.after(20, self.movePipes) 
        self.checkCollision()

    def createPipes(self):
        gapStart = random.randint(200,400)
        gapHeight = 200

        top = self.canvas.create_rectangle(self.canvasWidth, 0, self.canvasWidth + 80, gapStart, fill="green")
        bottom = self.canvas.create_rectangle(self.canvasWidth, gapStart + gapHeight, self.canvasWidth + 80, self.canvasHeight, fill="green")

        self.pipes.append((top, bottom, False, False))

        # Create new pipe every 2 seconds
        self.createPipeId = self.master.after(1800, self.createPipes)
        

    def checkCollision(self):
        birdCoordinates = self.canvas.coords(self.bird) # x1, y1, x2, y2
        if birdCoordinates[3] >= self.canvasHeight:
            print("Bird hit the ground")
            self.stopGame()

        for top, bottom, passed, scored in self.pipes:
            topPipeCoordinates = self.canvas.coords(top)
            bottomPipeCoordinates = self.canvas.coords(bottom)
        
            # COLLISION WITH TOP PIPE
            if (birdCoordinates[2] > topPipeCoordinates[0] and birdCoordinates[0] < topPipeCoordinates[2] and birdCoordinates[3] > topPipeCoordinates[1] and birdCoordinates[1] < topPipeCoordinates[3]):
                print("Collision with top pipe")
                self.stopGame()
                
            # COLLISION WITH BOTTOM PIPE
            elif (birdCoordinates[2] > bottomPipeCoordinates[0] and birdCoordinates[0] < bottomPipeCoordinates[2] and birdCoordinates[3] > bottomPipeCoordinates[1] and birdCoordinates[1] < bottomPipeCoordinates[3]):
                print("Collision with bottom pipe")
                self.stopGame()


            

    def stopGame(self):

        self.master.after_cancel(self.gravityId)
        self.master.after_cancel(self.movePipeId)
        self.master.after_cancel(self.createPipeId)
        self.canvas.unbind("<space>")

        self.restartButton = Button(self.bottomFrame, text = "Restart", font = ("Arial", 20, "bold"), command= self.restartGame)
        self.restartButton.pack()


    def startGame(self):

        self.pipes = []
        self.applyGravity()
        self.createPipes()
        self.movePipes()


    def updateScore(self):
        self.score += 1
        self.label.config(text = f"SCORE : {self.score}")


    def restartGame(self):
        self.restartButton.destroy()
        self.canvas.delete("all")

        # Reset bird
        self.bird = self.canvas.create_oval(150, 200, 200, 250, fill="yellow")

        # Reset score
        self.score = 0
        self.label.config(text=f"SCORE : {self.score}")

        # Rebind space
        self.canvas.focus_set()
        self.canvas.bind("<space>", self.jump)


        self.startGame()
