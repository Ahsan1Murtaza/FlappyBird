from tkinter import *
class Window:
    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(master, width=800, height=800)
        self.canvas.pack()

        self.topPipe = self.canvas.create_rectangle(700, 0, 800, 300, fill="green")
        self.bottomPipe = self.canvas.create_rectangle(700, 500, 800, 800, fill="green")

        self.bird = self.canvas.create_oval(100, 200, 230, 260, fill="yellow")

        self.canvas.focus_set()
        self.canvas.bind("<space>", self.jump)

        self.applyGravity()
        self.movePipes()
        
    def jump(self, event):
        self.canvas.move(self.bird, 0, -80)

    def applyGravity(self):
        self.canvas.move(self.bird, 0, 15)
        self.gravityId = self.master.after(100, self.applyGravity)

    def movePipes(self):
        self.canvas.move(self.topPipe, -10, 0)
        self.canvas.move(self.bottomPipe, -10, 0)

        self.movePipeId = self.master.after(100, self.movePipes) 

        self.checkCollision()

     
        

    def reLocatePipe(self):
        
        self.topPipe = self.canvas.create_rectangle(700, 0, 800, 300, fill="green")
        self.bottomPipe = self.canvas.create_rectangle(700, 500, 800, 800, fill="green")
        self.movePipe()

    def checkCollision(self):
        birdCoordinates = self.canvas.coords(self.bird) # x1,y1, x2, y2
        topPipeCoordinates = self.canvas.coords(self.topPipe) # x1,y1, x2, y2
        bottomPipeCoordinates = self.canvas.coords(self.bottomPipe) # x1,y1, x2, y2

        # NO COLLISION BUT PASSES THE PIPE
        if (topPipeCoordinates[2] < birdCoordinates[0]):
            self.canvas.delete(self.topPipe)
            self.canvas.delete(self.bottomPipe)
            self.reLocatePipe()
            return
        
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
        self.canvas.unbind("<space>")
        