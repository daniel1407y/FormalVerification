import sys
import solver
import solver_iterative

 # reads file content
def get_board(filename):
    try:
        with open(filename, 'r') as file:
            contents = file.read()
            return contents
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Error : Wrong number of arguments")
        return
    
    filename = sys.argv[1]
    solver_engine = None
    steps=None
    

        
    file_contents = get_board(filename) # reads file content
    if file_contents:
        print("INPUT BOARD : ")
        print(file_contents)
    
    if len(sys.argv)==2:
        solver.main(file_contents, filename, solver_engine, steps) # default
    elif len(sys.argv)>=3:
        solver_engine=sys.argv[2]
        if solver_engine=="iterative": # iterative
            solver_iterative.main(file_contents, filename, solver_engine, steps)
            return
        elif len(sys.argv)==4: # SAT with custom step limit
            steps = sys.argv[3]
        solver.main(file_contents, filename, solver_engine, steps) # BBD/SAT
    
    else:
        print("Error : Wrong number of arguments")




if __name__ == "__main__":
    main()