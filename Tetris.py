# Arjun Vasudevan, arjunvas, Reci T
# Tetris in Python using CMU Graphics!!!
from cmu_graphics import *
import math
import random


def onAppStart(app): #calls restart, sets up initial state
    restart(app)

def redrawAll(app):
    drawLabel('Tetris Lite!', app.width/2, app.height*0.075, size=(min(app.width,app.height)*0.04))
    drawBoard(app) #draws board
    if(app.gameOver): #if game over, show game over text
        drawLabel(f"Score = {app.score} GAME OVER, PRESS R TO RESTART",app.width/2,app.height-40 ,size = (min(app.width,app.height)*0.03), bold = True, fill = 'red')
        drawBoardBorder(app)
    else: #if game is not over, display score instead
        drawLabel(f"Score = {app.score}",app.width/2,app.height*0.95,size=(min(app.width,app.height)*0.05),bold=True,fill='green')
        drawPiece(app) #only draw piece when game is not over
        drawBoardBorder(app)
    

def onStep(app):
    if(not app.paused):
        takeStep(app)
        
def rotate2dListClockwise(L): #rotates pieces clockwise
    oldRows = len(L)
    oldCols = len(L[0])
    newRows = oldCols
    newCols = oldRows
    M = [[None] * newCols for i in range(newRows)]
    for oR in range(oldRows):
        for oC in range(oldCols):
            nR = oC     #sets the new row to the old collumn
            nC = oldRows-1-oR   #sets the new collumn to the inverse of the oldRow
            M[nR][nC] = L[oR][oC]
    return M
    
def rotatePieceClockwise(app): #rotates each piece clockwise using rotate function
    oldPiece = app.piece
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    oldRows = len(app.piece)
    oldCols = len(app.piece[0])
    app.piece = rotate2dListClockwise(app.piece)
    newRows = len(app.piece)
    newCols = len(app.piece[0])
    centerRow = oldTopRow + oldRows//2 #calculates center to recenter piece
    app.pieceTopRow = centerRow - newRows//2
    centerCol = oldLeftCol + oldCols//2
    app.pieceLeftCol = centerCol - newCols//2
    if(pieceIsLegal(app)): #if legal, continue
        return True
    else: #resets piece if illegal after rotate
        app.piece = oldPiece
        app.pieceTopRow = oldTopRow
        app.pieceLeftCol = oldLeftCol
        
    
def restart(app):
    app.gameOver = False
    app.paused = False
    app.stepsPerSecond=1
    app.rows = 15
    app.cols = 10
    app.boardLeft = 195
    app.boardTop = 100
    app.boardWidth = 410
    app.boardHeight = 580
    app.cellBorderWidth = 2
    app.board = [([None] * app.cols) for row in range(app.rows)]
    loadTetrisPieces(app)
    app.piece = app.tetrisPieces[0]
    app.pieceTopRow = 0
    app.pieceLeftCol = 0
    app.pieceIndex = 0
    app.pColor = 0
    app.score=0
    app.nextPieceIndex= random.randrange(len(app.tetrisPieces))
    loadNextPiece(app)
    
def takeStep(app):
    if app.gameOver:
        app.paused=True
    if not movePiece(app, +1, 0):
        # We could not move the piece, so place it on the board:
        placePieceOnBoard(app)
        removeFullRows(app)
        loadNextPiece(app)

def removeFullRows(app): #removes rows when full
    new = []
    fullCount = 0
    for r in app.board:
        if None in r: 
            new.append(r) #if row is not full, add back to list
        else:
            fullCount+=1 #if full, add to fullCount
    for i in range(fullCount):
        new.insert(0,[None]*app.cols) #insert fullcount empty rows back to top of list
    app.board=new
    if(fullCount==0): #handles scoring based on rows cleared
        return
    if(fullCount==1):
        app.score+=1
    elif(fullCount<=3):
        app.score+=2
    elif(fullCount>=4):
        app.score+=4
        
def placePieceOnBoard(app): #sets piece to be on board permanently once it cannot be moved
    for r in range(len(app.piece)):
        for c in range(len(app.piece[0])):
            if(app.piece[r][c]):
                app.board[app.pieceTopRow + r][app.pieceLeftCol + c] = app.pColor
                


def loadNextPiece(app):
    loadPiece(app,app.nextPieceIndex)
    app.nextPieceIndex = random.randrange(len(app.tetrisPieces))
    if(pieceIsLegal(app)):
        return
    else:
        app.gameOver = True #if we cannot place any more peices, it is game over

def drawPiece(app):
    for r in range(len(app.piece)):
        for c in range(len(app.piece[r])):
            if(app.piece[r][c]):
                drawCell(app,r+app.pieceTopRow,c+app.pieceLeftCol,app.pColor) #draws the current piece

def loadPiece(app,pieceIndex): #loads piece into variables
    app.piece = app.tetrisPieces[pieceIndex]
    app.pieceIndex=pieceIndex
    app.pieceTopRow = 0
    app.pieceLeftCol = math.floor(app.cols/2 - (len(app.piece[0])/2)) 
    app.pColor = app.tetrisPieceColors[pieceIndex]

def onKeyPress(app,key):
    if(key=='p'): app.paused= not app.paused
    if(key=='r'): restart(app)
    if(not app.paused):
        if key == 'left':
            movePiece(app,0,-1)
        elif key == 'right':
            movePiece(app,0,+1)
        elif key == 'down':
            movePiece(app,1,0)
        elif key == 'space': hardDropPiece(app)
        elif key == 'up': rotatePieceClockwise(app)

def hardDropPiece(app):
    while movePiece(app, +1, 0): #while it can move down, keep going down
        pass
    placePieceOnBoard(app) #when cannot move down, place permanently
    removeFullRows(app)
    loadNextPiece(app)
    
def movePiece(app,drow,dcol):
    app.pieceTopRow+=drow
    app.pieceLeftCol+=dcol
    if(pieceIsLegal(app)):
        
        return True
    else:
        app.pieceTopRow-=drow
        app.pieceLeftCol-=dcol
        return False
        
        
def cellIsOccupied(app,row,col):
    return app.board[row][col] is not None #checks if there is a peice there already
    
def pieceIsLegal(app):
    for r in range(len(app.piece)):
        for c in range(len(app.piece[0])):
            if app.piece[r][c]:
                pieceRow = app.pieceTopRow + r
                pieceCol = app.pieceLeftCol + c
                if(pieceRow < 0 or pieceRow >= app.rows or pieceCol< 0 or pieceCol >= app.cols or cellIsOccupied(app,pieceRow,pieceCol)):
                    return False
    return True
    

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, app.board[row][col])

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)


def loadTetrisPieces(app):
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]] 
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ 'red', 'yellow', 'magenta', 'pink',
                              'cyan', 'green', 'orange' ]

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def main():
    runApp(800,800)

main()

