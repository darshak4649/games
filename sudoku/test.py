import random

class Sudoku:
    def __init__(self):
        self.grid = [[0]*9 for _ in range(9)]
        self.solution = None

    def print_grid(self, grid=None):
        if grid is None:
            grid = self.grid
        for i, row in enumerate(grid):
            print(" ".join(str(num) if num != 0 else "." for num in row))
            if (i+1) % 3 == 0 and i != 8:
                print("-"*21)

    # -------- Sudoku Logic --------
    def get_row(self, r):
        return self.grid[r]

    def get_col(self, c):
        return [self.grid[r][c] for r in range(9)]

    def get_box(self, r, c):
        br, bc = (r//3)*3, (c//3)*3
        return [self.grid[br+i][bc+j] for i in range(3) for j in range(3)]

    def is_valid(self, num, r, c):
        return num not in self.get_row(r) and num not in self.get_col(c) and num not in self.get_box(r,c)

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    return r,c
        return None

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True
        r,c = empty
        for num in range(1,10):
            if self.is_valid(num,r,c):
                self.grid[r][c] = num
                if self.solve():
                    return True
                self.grid[r][c] = 0
        return False

    # -------- Generator --------
    def fill_box_randomly(self,sr,sc):
        nums = list(range(1,10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                self.grid[sr+i][sc+j] = nums.pop()

    def generate_full_solution(self):
        for i in range(0,9,3):
            self.fill_box_randomly(i,i)
        self.solve()
        self.solution = [row[:] for row in self.grid]

    # -------- Remove Numbers with Balanced Distribution --------
    def remove_numbers_balanced(self, difficulty="medium"):
        levels = {"easy":35,"medium":45,"hard":55}
        total_blanks = levels.get(difficulty,45)
        blanks_per_group = total_blanks // 9  # per row/col/box

        # Track blanks per row, col, box
        row_blanks = [0]*9
        col_blanks = [0]*9
        box_blanks = [0]*9

        positions = [(r,c) for r in range(9) for c in range(9)]
        random.shuffle(positions)

        removed = 0
        for r,c in positions:
            if removed >= total_blanks:
                break
            b = (r//3)*3 + (c//3)
            if row_blanks[r] < blanks_per_group and col_blanks[c] < blanks_per_group and box_blanks[b] < blanks_per_group and self.grid[r][c]!=0:
                self.grid[r][c]=0
                row_blanks[r]+=1
                col_blanks[c]+=1
                box_blanks[b]+=1
                removed+=1


# -------- Example Usage --------
if __name__=="__main__":
    sudoku = Sudoku()
    sudoku.generate_full_solution()
    print("Full Sudoku Solution:")
    sudoku.print_grid()

    sudoku.remove_numbers_balanced(difficulty="medium")
    print("\nPuzzle (Medium Difficulty, Balanced Blanks):")
    sudoku.print_grid()
