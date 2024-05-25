# update worker_row, worker_col according to movement
def worker_location_change(rows, columns):
    model_content = f'''
next(worker_row):=
case
    movement = u & (up_step | up_push): worker_row - 1;
    movement = d & (down_step | down_push): worker_row + 1;
    TRUE: worker_row;
esac;

next(worker_col):=
case
    movement = r & (right_step | right_push): worker_col + 1;
    movement = l & (left_step | left_push): worker_col - 1;
    TRUE: worker_col;
esac;
    '''
    return model_content


# board FDS
def moves(i,j, rows, columns, board):
    model_content=""
    # right
    if i>=0 and j-2>=0 and board[i][j-2]!="x":
        model_content+=f"\tmovement=r & right_push & worker_row={i} & worker_col={j-2} : TRUE;\n"
    if i>=0 and j-1>=0 and board[i][j-1]!="x":
        model_content+=f"\tmovement=r & right_push & worker_row={i} & worker_col={j-1} : FALSE;\n"
    
    # down
    if i-2>=0 and j>=0 and board[i-2][j]!="x":
        model_content+=f"\tmovement=d & down_push & worker_row={i-2} & worker_col={j} : TRUE;\n"
    if i-1>=0 and j>=0 and board[i-1][j]!="x":
        model_content+=f"\tmovement=d & down_push & worker_row={i-1} & worker_col={j} : FALSE;\n"

    # left
    if i>=0 and j+2<columns and board[i][j+2]!="x":
        model_content+=f"\tmovement=l & left_push & worker_row={i} & worker_col={j+2} : TRUE;\n"
    if i>=0 and j+1<columns and board[i][j+1]!="x":
        model_content+=f"\tmovement=l & left_push & worker_row={i} & worker_col={j+1} : FALSE;\n"

    # up
    if i+2<rows and j>=0 and board[i+2][j]!="x":
        model_content+=f"\tmovement=u & up_push & worker_row={i+2} & worker_col={j} : TRUE;\n"
    if i+1<rows and j>=0 and board[i+1][j]!="x":
        model_content+=f"\tmovement=u & up_push & worker_row={i+1} & worker_col={j} : FALSE;\n"
    model_content+=f"\n"    

    return model_content


# main function to generate the .smv file
def generate_nusmv_model(rows ,columns, board, worker_holder):
    model_content = f'''
MODULE main
DEFINE rows:={rows}; columns:={columns};
-- new  XSB     definition
-- a      @      warehouse keeper
-- o      +      warehouse keeper on goal
-- b      $      box
-- v      *      box on goal
-- x      #      wall
-- g      .      goal
-- _      _      floor
VAR
    worker_row : 0..{rows-1}; --current worker row
    worker_col : 0..{columns-1}; --current worker col
    movement : {{u, d, l, r, 0}};
    board : array 0..{rows-1} of array 0..{columns-1} of boolean;
    
ASSIGN
'''
    for i in range(rows):
        for j in range(columns):
            if board[i][j]=='b':
                model_content+=f"init(board[{i}][{j}]):=TRUE;\t"
            else:
                model_content+=f"init(board[{i}][{j}]):=FALSE;\t"
        model_content+=f"\n"

    model_content+=f'''
init(movement) := 0;

init(worker_row) := {worker_holder[0]}; init(worker_col) := {worker_holder[1]};
'''

    model_content += worker_location_change(rows, columns)
    model_content+=f"next(movement):={{u, d ,l ,r}};"
    for i in range(rows):
        for j in range(columns):
            if board[i][j]=='x': # state 'x' cant change
                model_content += f"\nnext(board[{i}][{j}]):= board[{i}][{j}];\n"
            else:
                model_content+= f"\nnext(board[{i}][{j}]):=\ncase\n"
                model_content+=moves(i,j, rows, columns, board)
                model_content+= f"\tTRUE: board[{i}][{j}];\nesac;\n"


    model_content += f'''
    
DEFINE
    down_step := worker_row<{rows-1} & !walls[worker_row+1][worker_col] & !board[worker_row+1][worker_col];
    down_push := worker_row<{rows-2} & board[worker_row+1][worker_col] & !walls[worker_row+2][worker_col] & !board[worker_row+2][worker_col];

    right_step := worker_col<{columns-1} & !walls[worker_row][worker_col+1] & !board[worker_row][worker_col+1];
    right_push := worker_col<{columns-2} & board[worker_row][worker_col+1] & !walls[worker_row][worker_col+2] & !board[worker_row][worker_col+2];

    left_step := worker_col>0 & !walls[worker_row][worker_col - 1] & !board[worker_row][worker_col - 1];
    left_push := worker_col>1 & board[worker_row][worker_col - 1] & !walls[worker_row][worker_col - 2] & !board[worker_row][worker_col - 2];

    up_step := worker_row>0 & !walls[worker_row - 1][worker_col] & !board[worker_row - 1][worker_col];
    up_push := worker_row>1 & board[worker_row - 1][worker_col] & !walls[worker_row - 2][worker_col] & !board[worker_row - 2][worker_col];
'''
    model_content += f'''
walls :='''
    # creating the walls constant
    model_content += " [\n"
    for i in range(rows):
        model_content += "["
        for j in range(columns):
            if board[i][j] == 'x':
                model_content += " TRUE"
            else:
                model_content += "FALSE"
            if j < columns - 1:
                model_content += ", "
        model_content += "]"
        if i < rows - 1:
            model_content += ",\n"

    model_content += "];"

    model_content+=f"\nJUSTICE"
    model_content+=f"\n\t"
    for i in range(rows):
        for j in range(columns):
            if board[i][j]!='x' and board[i][j]!='.':
                border = ((board[i][j+1]=='x' or board[i][j-1]=='x') and (board[i-1][j]=='x' or board[i+1][j]=='x'))
                if border:
                    model_content += f"!board[{i}][{j}] & "
            if board[i][j]=='x':
                model_content += f"!board[{i}][{j}] & "
    model_content = model_content[:-3]  # remove the last " & "
    model_content+=f";\n"


    model_content += f"DEFINE\n"
    model_content +=f"\treach:= "
    for i in range(rows):
        for j in range(columns):
            if board[i][j]=='.':
                    model_content += f"board[{i}][{j}] & "
    model_content = model_content[:-3]  # remove the last " & "
    model_content+=";"
    
    model_content += f"\n\tLTLSPEC G(!reach)"
    return model_content