class Button:
    def __init__(self, left_side, top_side, bottom_side, right_side):
        self.left_side = left_side
        self.top_side = top_side
        self.bottom_side = bottom_side
        self.right_side = right_side

    def is_clicked(self, mouse_position):
        return self.left_side <= mouse_position[0] <= self.right_side and \
            self.top_side <= mouse_position[1] <= self.bottom_side
