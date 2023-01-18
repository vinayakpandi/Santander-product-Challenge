# Import Libraries
import tkinter as tk
from tkinter import *
from tkinter import ttk
import random
from tkinter import scrolledtext
from tkinter import messagebox

#Define Functions


# checkInput function
# Inputs : None
# Results : None
def checkInput():

  # Import Global Variables
  global maxNum  # Maximum Number
  global boolNegativeNums  # Boolean Value for Negative Numbers
  global boolModulus  # Boolean Value for Modulus Operator
  global correctCount  # Number of Correct Attempts
  global wrongCount  # Number of Wrong Attempts
  global totalCount  # Number of Total Attempts
  global systemLog  # System Message Log Interface
  global numOfQuestions

  boolNegativeNums = inclNegativeNums.get(
  )  # Reassign boolNegativeNums value based on User Input
  boolModulus = inclModulus.get(
  )  # Reassign boolModulus value based on User Input
  levelSelection = combo.get(
  )  # Capture combobox input and store to levelSelection variable
  if levelSelection not in combo["values"]:
    # Invalid Level Selected
    systemLog.config(text="Invalid Level Selected! Try Again!")
  else:
    try:
      numOfQuestions = int(maxNumSelection.get())
      # Further validate input
      if levelSelection == "Level 1 (1-3)":
        questionDisplay.config(bg="green",
                               fg="white")  # Change frame background
        maxNum = 3  # Reassign maximum number value
      elif levelSelection == "Level 2 (1-6)":
        questionDisplay.config(bg="yellow")  # Change frame background
        maxNum = 6  # Reassign maximum number value
      elif levelSelection == "Level 3 (1-9)":
        questionDisplay.config(bg="orange")  # Change frame background
        maxNum = 9  # Reassign maximum number value
      elif levelSelection == "Level 4 (1-12)":
        questionDisplay.config(bg="red", fg="white")  # Change frame background
        maxNum = 12  # Reassign maximum number value
      systemLog.config(
        text="Game has started! Vroom Vroom!")  # Reset System Log to start
      pastQuestion.config(text="")
      # Reset All Game Counter Values
      totalCount = 0
      correctCount = 0
      wrongCount = 0
      # Reset Game Counter Value Displays
      numCorrect_value.config(text=correctCount)
      numTotal_value.config(text=totalCount)
      numWrong_value.config(text=wrongCount)
      # Reset Progress Bar
      gameProgress["value"] = 0
      gen_question()  # Invoke gen_question function to initially start
    except:
      systemLog.config(
        text="Improper input! Enter an integer for number of questions!")


# gen_question function
# Inputs : None
# Results : None
def gen_question():
  # Import Global Variables
  global boolModulus
  global operators
  global maxNum
  global boolNegativeNums
  global num1
  global num2
  global expression
  global leastNum
  global answer

  if boolModulus:
    # If user selected modulus operator, add it into operators list
    operators.append("%")

  if boolNegativeNums:
    # Least Number = Negative Maximum Number
    leastNum = 0 - maxNum
  else:
    # Least Number = 1
    leastNum = 1

  if leastNum == 0:
    leastNum = 1

  # Generate random numbers and assign them to variables
  num1 = random.randint(leastNum, maxNum)
  num2 = random.randint(leastNum, maxNum)

  # Generate random operator and assign it to variable
  operator = random.choice(operators)

  # Generate expression, assign it to variable and display it
  if operator == "%":

    # Assuming user selects negative numbers too, absolute them for positive value
    num1 = abs(num1)
    num2 = abs(num2)

    # Define larger / smaller numbers
    if num1 >= num2:
      largerNum = num1
      smallerNum = num2
    else:
      largerNum = num2
      smallerNum = num1
    
    # Create expression with larger / smaller numbers
    expression = f"{largerNum} {operator} {smallerNum}"
  
  # Incase of Division operator
  elif operator == "/":
    # Calculate product first
    resultSample = num1 * num2
    expression = f"{resultSample} {operator} {num1}"
  else:
    # All other clauses (addition, subtraction & multiplication)
    expression = f"{num1} {operator} {num2}"

  # Display question in game to questionDisplay widget
  questionDisplay.config(text=expression)

  # Generate answer and assign it to global variable
  answer = float(eval(expression))


# resetValue function
# Inputs : None
# Results : None
def resetValue():
  # Import Global Variables
  global correctCount
  global wrongCount
  global totalCount
  global systemLog
  global pastQuestion
  global gameOver

  # Past Game Counters
  totalCount_old = totalCount
  correctCount_old = correctCount

  # Reset Game Counters
  totalCount = 0
  correctCount = 0
  wrongCount = 0

  # Display Game Counters (after reset)
  numCorrect_value.config(text=correctCount)
  numTotal_value.config(text=totalCount)
  numWrong_value.config(text=wrongCount)

  # Reset frame 1 background color
  frame1.config(bg="#5F2423")

  # Reset question display
  questionDisplay.config(text="")

  # Empty questionInput entry
  questionInput.delete(0, 'end')

  # Log game reset message
  if gameOver:
    global highScore
    scoreStr = "Game Over! Click Start Game to play again!"
    systemLog.config(text=scoreStr)

    try:
      score = (correctCount_old / totalCount_old) * 100
      score = round(score, 2)
    except:
      score = 0.00

    percentStr = f"You scored a {score}%"
    pastQuestion.config(text=percentStr)
    gameOver = False
    if score > highScore:
      highScore = score
      messagebox.showinfo(
        "New High Score Achieved!",
        f"Congrats! You have a new high score of {highScore}%!")
      highScoreLabel.config(text=f"Your High Score : {highScore}%")
  else:
    # Reset Progress Bar
    gameProgress["value"] = 0
    messagebox.showwarning("Game Has Been Reset. To play again, press 'Start Game'.")
    systemLog.config(
      text="Game has been reset. Press 'Start Game' to try again!")
    # Reset past question
    pastQuestion.config(text="")


# updateScore function
# Inputs : None
# Results : None
def updateScore():
  # Import Global Variables
  global correctCount
  global wrongCount
  global totalCount

  # Update displays of game counters
  numCorrect_value.config(text=correctCount)
  numTotal_value.config(text=totalCount)
  numWrong_value.config(text=wrongCount)


# checkAnswer function
# Inputs : None
# Results : None
def checkAnswer():
  # Import Global Variables
  global correctCount
  global wrongCount
  global totalCount
  global pastQuestion
  global numOfQuestions
  global systemLog
  global gameOver
  global errorLogWidget

  # Try to get user given answer
  try:
    # Use float to accommodate possible decimal values
    attempt = float(questionInput.get())
  except:
    # Due to bad input, update attempt value to ""
    attempt = ""

  # If answer is correct :
  if answer == attempt:

    # Update counters
    correctCount += 1
    totalCount += 1

    # Update score and display question as past question
    updateScore()
    pastQuestionMessage = f"Past Question :   {expression} = {questionInput.get()} (Correct!)"
    pastQuestion.config(text=pastQuestionMessage)
    updateProgressbar()
  else:
    # Update counters
    wrongCount += 1
    totalCount += 1

    # Update score and display question as past question
    updateScore()
    pastQuestionMessage = f"Past Question :   {expression} = {questionInput.get()} (Correct Answer = {answer})"
    pastQuestion.config(text=pastQuestionMessage)
    errorLogWidget.configure(state='normal')
    errorLogWidget.insert(tk.INSERT, f"""\n{pastQuestionMessage}\n""")
    errorLogWidget.configure(state='disabled')
    updateProgressbar()

  # Empty questionInput entry
  questionInput.delete(0, 'end')

  # Generate next question
  if totalCount < numOfQuestions:
    gen_question()
  else:
    systemLog.config(text="Game is over! Play again!")
    gameOver = True
    resetValue()


# updateProgressbar function
# Inputs : None
# Results : None
def updateProgressbar():
  global numOfQuestions
  step = 100 / numOfQuestions
  gameProgress["value"] += step

# quitGame function
# Inputs : None
# Results : None
def quitGame():
  messagebox.showerror("Closing Game", "Thanks for playing! See you again, racer!")
  window.destroy()

# backToGame function
# Inputs : None
# Results : None
def backToGame():
  # Go back to gameplay tab
  notebook.select(0)

# backToErrorLog function
# Inputs : None
# Results : None
def backToErrorLog():
  # Go back to error log
  notebook.select(1)

# Define global variables
num1 = 0  # Random number 1
num2 = 0  # Random number 2
operators = ["*", "+", "-", "/"]  # Initial operators (with division)
expression = ""  # Expression string
answer = ""  # Answer to expression

maxNum = 0  # Maximum possible value for random number
leastNum = 1  # Least possible value for random number
boolNegativeNums = False  # Boolean value for negative numbers
boolModulus = False  # Boolean value for modulus
numOfQuestions = 0
gameOver = False
highScore = 0.0

correctCount = 0  # Number of correct attempts
wrongCount = 0  # Number of wrong attempts
totalCount = 0  # Number of total attempts

# Create Tkinter Window
window = tk.Tk()
window.title("Flash - Math Game")
# window.geometry("645x290")

style = ttk.Style()

style.layout('Tabless.TNotebook.Tab', []) # new style with tabs turned off

# Game Notebook (for tabs)
notebook = ttk.Notebook(window, style='Tabless.TNotebook')
notebook.grid(row=0, column=0)

# Game Container
gameContainer = tk.Frame(notebook)
gameContainer.grid(row=0, column=0)

# Error Log
errorLogContainer = tk.Frame(notebook)
errorLogContainer.grid(row=0, column=0)
errorLogContainer.config(bg="#5F2423")

# Design Error Log Container
errorLogTitle = Label(
  errorLogContainer,
  text="Past Errors Log",
  font="Helvetica 16 bold italic",
  bg="red",fg="white"
)
errorLogTitle.grid(row=0, column=1)

highScoreLabel = Label(
  errorLogContainer,
  text=f"High Score : {highScore}",
  font="Helvetica 12 bold italic",
  bg="green",fg="white"
)
highScoreLabel.grid(row=1, column=1)

errorLogWidget = scrolledtext.ScrolledText(errorLogContainer,
                                           wrap=tk.WORD,
                                           width=55,
                                           height=10,
                                           font="Helvetica 12 bold italic")

errorLogWidget.insert(tk.INSERT, """
""")
errorLogWidget.configure(state='disabled')
errorLogWidget.grid(column=1, row=2, pady=10, padx=10)

# Images Added on Sides
img1 = PhotoImage(file='img1.png')
lbl1_errorlog = Label(errorLogContainer, image=img1, borderwidth=0, highlightthickness=0)
lbl1_errorlog.grid(row=2, column=0,sticky="w",padx=5)

img2 = PhotoImage(file='img2.png')
lbl2_errorlog = Label(errorLogContainer, image=img2, borderwidth=0, highlightthickness=0)
lbl2_errorlog.grid(row=2, column=2,sticky="e",padx=5)

# App Favicon
window.iconphoto(False, img1)

quitBtn = tk.Button(errorLogContainer,
                             text="Quit Game",
                             font="Helvetica 12 bold italic",
                             fg='white',
                             command=quitGame)
quitBtn.config(bg="#009A4E")
quitBtn.grid(row=4,
                      column=1,
                      columnspan=1,
                      sticky='ew',
                      pady=10,
                      padx=10)

# Button to reset game
backBtn = tk.Button(errorLogContainer,
                     text="Go Back To Game",
                     font="Helvetica 12 bold italic",
                     fg='red',
                     command=backToGame)
backBtn.config(bg="#F7d31d")
backBtn.grid(row=3, column=1, columnspan=1, sticky='ew', pady=10, padx=10)

# Adding Tabs to notebook
notebook.add(gameContainer, text="Gameplay")
notebook.add(errorLogContainer, text="Error Log")

# Define 2 sides of app
frame1 = tk.Frame(gameContainer)  # App left side
frame1.config(bg="#5F2423")
frame1.grid(row=0, column=0, sticky="ns")

# Frame 2 Components
frame2 = tk.Frame(gameContainer)  # App right side
frame2.config(bg="red")
frame2.grid(row=0, column=1, sticky="ns")

# App heading
appLabel = tk.Label(
  frame2,
  text="Flash - Math Game",
  font="Helvetica 16 bold italic",
  fg="white",
  bg="red",
)
appLabel.grid(column=0, row=0, padx=6, pady=6)

# App options
optionsFrame = tk.Frame(frame2)
optionsFrame.grid(row=1, column=0, padx=3, pady=3)

# Declare Options Variables
inclNegativeNums = BooleanVar()
inclModulus = BooleanVar()

# Negative Number Checkbox
checkNegativeNums = Checkbutton(optionsFrame,
                                text="Include Negative Numbers",
                                variable=inclNegativeNums,
                                font="Helvetica 11 bold italic",
                                selectcolor="#F7D31D")
checkNegativeNums.grid(column=0, row=1, sticky="NESW")

# Modulus Button Checkbox
checkModulus = Checkbutton(optionsFrame,
                           text="Include Modulus Operator",
                           font="Helvetica 11 bold italic",
                           variable=inclModulus,
                           selectcolor="#F7D31D")
checkModulus.grid(column=0, row=2)

# Create Combobox for level selection
combo_label = Label(optionsFrame,
                    text="Pick A Level :",
                    font="Helvetica 11 bold italic",
                    fg="#BD0000")
combo_label.grid(column=0, row=3, sticky="ew", pady=5)
combo = ttk.Combobox(optionsFrame, font="Helvetica 11 bold italic")
combo['values'] = [
  "Level 1 (1-3)", "Level 2 (1-6)", "Level 3 (1-9)", "Level 4 (1-12)"
]  # Level options
combo.current(0)  # Set the selected item to level 1
combo.grid(row=3, column=1, sticky="ew", pady=5)

maxNumLabel = Label(optionsFrame,
                    text="# Of Questions :",
                    font="Helvetica 11 bold italic",
                    fg="#009A4E")
maxNumLabel.grid(column=0, row=4, sticky="ew", pady=10, padx=5)
maxNumSelection = Entry(optionsFrame)
maxNumSelection.grid(row=4, column=1, padx=5, pady=10)

# Button to submit game options
submitOptionsBtn = tk.Button(optionsFrame,
                             text="Start Game",
                             font="Helvetica 12 bold italic",
                             fg='white',
                             command=checkInput)
submitOptionsBtn.config(bg="#009A4E")
submitOptionsBtn.grid(row=5,
                      column=0,
                      columnspan=2,
                      sticky='ew',
                      pady=10,
                      padx=10)

# Button to reset game
resetBtn = tk.Button(optionsFrame,
                     text="Reset Game",
                     font="Helvetica 12 bold italic",
                     fg='red',
                     command=resetValue)
resetBtn.config(bg="#F7d31d")
resetBtn.grid(row=6, column=0, columnspan=1, sticky='ew', pady=10, padx=10)

# Button to visit Error Log
errorLogBtn = tk.Button(optionsFrame,
                     text="View Error Log",
                     font="Helvetica 12 bold italic",
                     fg='white',
                     command=backToErrorLog)
errorLogBtn.config(bg="#5F2423")
errorLogBtn.grid(row=6, column=1, columnspan=1, sticky='ew', pady=10, padx=10)

# System Message Log widget to display game messages
systemLog = tk.Label(optionsFrame,
                     text="(System Log Messages)",
                     font="Helvetica 9 bold italic")
systemLog.grid(row=7, column=0, columnspan=2, sticky='ew', padx=10, pady=10)

# Widget to display past question attempted by user
pastQuestion = tk.Label(optionsFrame, text="", font="Helvetica 11 bold italic")
pastQuestion.grid(row=8, column=0, columnspan=2, sticky='ew', padx=10, pady=10)

#Frame 1 Components
consoleFrame = tk.Frame(
  frame1)  # Console frame to show question and accept answer
consoleFrame.config(bg="red")
consoleFrame.grid(row=1, column=1, padx=10, pady=10)

#Logo
lbl1 = Label(frame1, image=img1, borderwidth=0, highlightthickness=0)
lbl1.grid(row=0, column=1, sticky="w", padx=5, pady=5)

lbl2 = Label(frame1, image=img2, borderwidth=0, highlightthickness=0)
lbl2.grid(row=0, column=1, sticky="e", padx=5, pady=5)

# Display expression for user to attempt
questionDisplay = Label(
  consoleFrame, text="", bg="#F7d31d",
  font="Helvetica 11 bold italic")  # Set intial text to ""
questionDisplay.grid(row=1, column=1, padx=10, pady=10)

# Accept user input to displayed expression
questionInput = Entry(consoleFrame)
questionInput.grid(row=1, column=2, padx=5, pady=10)

# Button to validate user input and check it
checkAnswerBtn = tk.Button(consoleFrame,
                           text="Check Answer",
                           font="Helvetica 11 bold italic",
                           fg='white',
                           command=checkAnswer)
checkAnswerBtn.config(bg="green")
checkAnswerBtn.grid(row=2, column=1, padx=5, pady=5, sticky="ew", columnspan=2)

# A frame widget to display game counters
countFrame = tk.Frame(frame1)
countFrame.config(bg="red")
countFrame.grid(row=2, column=1, padx=10, pady=10)

# Label for correct attempts game counter
numCorrect_label = Label(countFrame,
                         text="Correct Attempts",
                         font="Helvetica 10 bold italic",
                         bg="#F7d31d")
numCorrect_label.grid(row=2, column=1, padx=5, pady=5)

# Label for wrong attempts game counter
numWrong_label = Label(countFrame,
                       text="Wrong Attempts",
                       font="Helvetica 10 bold italic",
                       bg="#F7d31d")
numWrong_label.grid(row=2, column=2, padx=5, pady=5)

# Label for total attempts game counter
numLeft_label = Label(countFrame,
                      text="Total Attempts",
                      font="Helvetica 10 bold italic",
                      bg="#F7d31d")
numLeft_label.grid(row=2, column=3, padx=5, pady=5)

# Value display for correct attempts game counter
numCorrect_value = Label(countFrame, text="", font="Helvetica 10 bold italic")
numCorrect_value.grid(row=1, column=1, padx=5, pady=5)

# Value display for wrong attempts game counter
numWrong_value = Label(countFrame, text="", font="Helvetica 10 bold italic")
numWrong_value.grid(row=1, column=2, padx=5, pady=5)

# Value display for total attempts game counter
numTotal_value = Label(countFrame, text="", font="Helvetica 10 bold italic")
numTotal_value.grid(row=1, column=3, padx=5, pady=5)

# Progress Bar Frame
progressFrame = tk.Frame(
  frame1)  # Console frame to show question and accept answer
progressFrame.config(bg="red")
progressFrame.grid(row=3, column=1, padx=10, pady=10)

gameProgress = ttk.Progressbar(progressFrame,
                               orient=HORIZONTAL,
                               length=300,
                               mode='determinate')
gameProgress.grid(row=1, column=1, padx=5, pady=5)

# To run app
messagebox.showinfo("Welcome To Flash!", 'Welcome! \
To begin playing, please select game options and a level. \
Press "Start Game" to begin gameplay with selected options!')
tk.mainloop()
