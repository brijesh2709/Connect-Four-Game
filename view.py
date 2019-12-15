'''This is the view module for the connectfour tkinter GUI.'''
# We import necessary modules
from tkinter import *
from tkinter import messagebox
import control


class View:
    '''This class view deals with all the gui related functions.'''
    def __init__(self):
        '''We initiate and assign variables to be used.'''
        self.c = control.control()
        self.Board_C = self.c.columns
        self.Board_R = self.c.rows
        self.w = self.Board_C * control.size
        self.h = (self.Board_R + 1) * control.size

    def game_window(self):
        '''
        Generates the game window for connect four
        '''
        self.window = Tk()
        self.menu1.destroy()
        # This creates the window with backgroung blue
        self.connect_board = Canvas(self.window, width=self.w,
                                    height=self.h, bg='blue')
        # This calls for the function to detect clicks and call the motion
        # method
        self.window.bind('<Button 1>', self.motion)
        # This creates the board with required rows and columns
        self.pieces(self.c.board, self.connect_board)
        # we pack all this in a tkinter window and our window is ready
        self.connect_board.pack()
        self.window.mainloop()

    def motion(self, event):
        '''
        registers the clicks that the user makes
        '''
        x, y = event.x, event.y
        # We call the game game action in control module
        self.c.game_action(x, y)
        # The we generate new board after every move
        self.pieces(self.c.board, self.connect_board)
        if self.c.winner != 0:
            self.window.destroy()
            self.print_winner()

    def rules(self):
        '''
        Opens a info window that displays the rules.
        '''
        # When the rules button is pressed a message bos appears
        messagebox.showinfo('Rules', 'These are the rules: There are two ' \
                            + 'players with different colors. Each player ' \
                            + 'can either pop their color in the circles or'\
                            + ' they can drop their color in a circle. Click' \
                            + ' on the column you want to drop your color.' \
                            + ' Click on the bottomost existing color to pop'\
                            + ' it out. The first player to connect four of' \
                            + ' his own colored circles, wins')

    def pieces(self, board, connect_board):
        '''
        Generates a board from number of columns and rows for playing the game.
        '''
        for c in range(self.Board_C + 1):
            for r in range(self.Board_R):
                connect_board.create_oval(c * control.size,
                                          r * control.size + control.size,
                                          c * control.size + control.size,
                                         r * control.size + 2 * control.size,
                                         fill='white', outline='blue',
                                          width=5)
        for c in range(self.Board_C):
            for r in range(self.Board_R):
                if board[c][r] == 1:
                    connect_board.create_oval(c*control.size,
                                            (r*control.size + control.size),
                                            c*control.size + control.size,
                                            (r*control.size + 2*control.size),
                                            fill='orange', outline='blue',
                                              width=5)
                elif board[c][r] == 2:
                    connect_board.create_oval(c*control.size,
                                             (r*control.size + control.size),
                                            c*control.size + control.size,
                                            (r*control.size + 2*control.size),
                                            fill='limegreen', outline='blue',
                                              width=5)

    def menu(self):
        '''
        main menu of the game
        '''
        self.menu1 = Tk()
        self.menu1.geometry('200x200')
        # We create various buttons and we attach command to it
        rules_button = Button(self.menu1, text='Rules', bd=5,
                              command=self.rules)
        start_button = Button(self.menu1, text='Start Game', bd=5,
                              command=self.game_window)
        option_button = Button(self.menu1, text='Options', bd=5,
                               command=self.option)
        quit_button = Button(self.menu1, text='Quit', bd=5,
                             command=self.menu1.destroy)
        # We place then in a grid
        rules_button.place(x=80, y=95)
        quit_button.place(x=82, y=135)
        start_button.place(x=65, y=20)
        option_button.place(x=73, y=55)
        self.menu1.mainloop()

    def option(self):
        '''When the option button is pressed, this function is called
        and a new window for enrty pops up.'''
        self.option1 = Tk()
        self.menu1.destroy()
        # We restrict the game board because if the game board is too
        # big it won't fit on the screen
        message = Label(self.option1, text='Pick your custom board size:'
                                          '(input number bigger or equal to 4,'
                        'columns should be less than 13\n and rows should be '
                        'less than 9 or else default board will be generated.')
        c = Label(self.option1, text='Columns:')
        r = Label(self.option1, text='Rows:')
        self.col = Entry(self.option1)
        self.row = Entry(self.option1)
        # Once confirm button is pressed the rows and column inputs are
        # recorded
        confirm = Button(self.option1, text='Confirm', command=self.entry)
        # We organize the enttry andthe button in a grid.
        message.grid(row=0)
        c.grid(row=1)
        r.grid(row=2)
        self.col.grid(row=1, column=1)
        self.row.grid(row=2, column=1)
        confirm.grid()

        self.option1.mainloop()

    def entry(self):
        '''This method deals with the entry of rows and columns and then
        creates a board.'''
        col = self.col.get()
        row = self.row.get()
        try:
            # We restrict the board size because a board size bigger than
            # would not fit on some small screen computers
            # If the user nputs an invalid input, the default board is
            # set up
            if 12 >= int(col) >= 4 and 8 >= int(row) >= 4:
                self.c.change_board_size(int(col), int(row))
                self.__init__()
        except ValueError:
            pass
        self.option1.destroy()
        self.menu()

    def print_winner(self):
        ''' This method deals with detecting the winner and printing it
        in a tkinter window.'''
        winner = Tk()
        if self.c.winner == 1:
            text = 'Orange Won!'
        else:
            text = 'Green Won!'
        message = Label(winner, text=text)
        # After a player wins we give the option to quit
        q = Button(winner, text='Quit', command=winner.destroy)
        message.pack()
        q.pack()
        winner.mainloop()


if __name__ == '__main__':
    x = View()
    # We start with the menu function.
    x.menu()
