with open("input") as f:
    lines = f.readlines()

down = (0, 1)
up = (0, -1)
left = (-1, 0)
right = (1, 0)

turn_left = "left"
straight = "straight"
turn_right = "right"

cart_symbols = {
    ">": (right, '-'),
    '<': (left, '-'),
    "^": (up, '|'),
    "v": (down, "|")
}


class Cart:
    def __init__(self, grid, pos, direction):
        self.grid = grid
        self.pos = pos
        self.direction = direction
        self.next_turn = turn_left

    def move(self):
        print(f"Moving {str(self)}...")
        self.pos = (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1])
        symbol = self.grid[self.pos[1]][self.pos[0]]
        if symbol == ' ':
            raise Exception(f"Fallen off the track: {str(self)}")
        if self.direction == up and symbol == "/":
            self.direction = right
        elif self.direction == up and symbol == "\\":
            self.direction = left
        elif self.direction == right and symbol == "\\":
            self.direction = down
        elif self.direction == right and symbol == "/":
            self.direction = up
        elif self.direction == left and symbol == "\\":
            self.direction = up
        elif self.direction == left and symbol == "/":
            self.direction = down
        elif self.direction == down and symbol == "\\":
            self.direction = right
        elif self.direction == down and symbol == "/":
            self.direction = left
        elif symbol == "+":
            if self.next_turn == turn_left:
                if self.direction == up:
                    self.direction = left
                elif self.direction == right:
                    self.direction = up
                elif self.direction == down:
                    self.direction = right
                elif self.direction == left:
                    self.direction = down
                else:
                    raise Exception("Ooops")
                self.next_turn = straight
            elif self.next_turn == straight:
                self.next_turn = turn_right
            elif self.next_turn == turn_right:
                if self.direction == up:
                    self.direction = right
                elif self.direction == right:
                    self.direction = down
                elif self.direction == down:
                    self.direction = left
                elif self.direction == left:
                    self.direction = up
                else:
                    raise Exception("Ooops")
                self.next_turn = turn_left
            else:
                raise Exception("Ooops")

    def __str__(self):
        return f"Cart at {self.pos} facing {self.direction}. Next turn {self.next_turn}"


carts = []
rows = []
for y, line in enumerate(lines):
    row = list(line.replace("\r", ""))
    for x, cell in enumerate(row):
        if cell in cart_symbols:
            symbol = cart_symbols[cell]
            carts.append(Cart(rows, (x, y), symbol[0]))
            row[x] = symbol[1]
    rows.append(row)

for row in rows:
    print("".join(row))

tick = 0
while len(carts) > 1:
    print(tick)
    carts.sort(key=lambda cart: cart.pos[1] * 10000 + cart.pos[0])
    remove_carts = []
    for cart in list(carts):
        cart.move()
        for other_cart in carts:
            if cart == other_cart:
                continue
            if cart.pos == other_cart.pos:
                print(f"Crash between carts {str(cart)} and {str(other_cart)}")
                carts.remove(cart)
                carts.remove(other_cart)

    tick = tick + 1

print(str(carts[0]))
