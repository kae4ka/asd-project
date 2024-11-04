# method 2 
def is_safe(board, row, col):
    for i in range(row):
        if board[i] == col or abs(board[i] - col) == row - i:
            return False
    return True

def solve_n_queens(board, row, size, solution_count):
    if row == size:
        # Create a list of positions [row, col] for each queen
        positions = [[i, board[i]] for i in range(size)]
        print("[row,col] of solution number ", solution_count[0] +1," :", positions) # Print the solutions in [row, col] format
        solution_count[0] += 1  # Increment the solution count when a valid solution is found
        return True
    for col in range(size):
        if is_safe(board, row, col):
            board[row] = col
            solve_n_queens(board, row + 1, size, solution_count)
            board[row] = -1

def main():
    size = 8
    board = [-1] * size
    solution_count = [0]  # Use a list to allow modification within the function
    solve_n_queens(board, 0, size, solution_count)
    print(f"Total number of solutions: {solution_count[0]}")  # Print the total number of solutions
main()