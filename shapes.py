from enum import Enum

class Square(Enum):
    SQUARE = 1

class Domino(Enum):
    DOMINO = 1

class ThreeSquareShape(Enum):
    """
    ThreeSquareShape represents a tromino, a piece consisting of three squares.
    There are two different shapes:

    I-tromino (straight):
        ###
    
    L-tromino:   
        #
    
        ##
    """
    I = 1
    L = 2


class FourSquareShape(Enum):
    """
    FourSquareShape represents a tetromino, a piece consisting of four squares.
    There are seven different shapes:

    I-tetromino (straight):
        ####

    O-tetronimo (square):
        ##
        
        ##
    
    T-tetromino:
        ###
         
          #
    
    J-tetromino:
        ###
    
            #
    
    L-tetromino:   
            #
    
        ###
    
    S-tetromino:  
           ##
        ##
    
    Z-tetromino:
        ##
           ##
    """
    I = 1
    O = 2
    T = 3
    J = 4
    L = 5
    S = 6
    Z = 7


class FiveSquareShape(Enum):
    """
    FiveSquareShape represents a pentomino, a piece consisting of five squares.
    There are eighteen different shapes:

    F-pentomino:
          ##
        ##
          #
    
    F-pentomino (mirror):
        ##
           ##
          #
    
    I-pentomino (straight):
        ######
    
    L-pentomino:   
               #
    
        ####
    
    L-pentomino (mirror):   
        #
    
         ####

    N-pentonimo:
        ##
    
          ###
    
    N-pentonimo (mirror):
          ###
    
        ##
    
    P-pentomino:
        ###
    
          ##
    
    P-pentomino (mirror):
        ###
    
        ##
    
    T-pentomino:  
        ###
         
          #
    
          #
    
    U-pentomino:
        #      #

        ###

    V-pentomino:
        ###
    
        #
    
        #
    
    W-pentomino:
        ##
    
          ##
    
            #  

    X-pentomino:  
          #
         
        ###
    
          #
    
    Y-pentomino:
             #
        ####
    
    Y-pentomino (mirror):
        ####
    
            #

    Z-pentomino:
        ##
          #
    
          ##
    
    Z-pentomino (mirror):
          ##
    
          #
    
        ##
    """
    F = 1
    F_MIRROR = 2
    I = 3
    L = 4
    L_MIRROR = 5
    N = 6
    N_MIRROR = 7
    P = 8
    P_MIRROR = 9
    T = 10
    U = 11
    V = 12
    W = 13
    X = 14
    Y = 15
    Y_MIRROR = 16
    Z = 17
    Z_MIRROR = 18