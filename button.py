# This class represents the buttons available in the game
class Button:
    def __init__(self, left_side, top_side, bottom_side, right_side):
        self.left_side = left_side  # Left border side of the button
        self.top_side = top_side    # Top border side of the button
        self.bottom_side = bottom_side  # Bottom border side of the button
        self.right_side = right_side    # Right border side of the button

    # This method just return a boolean value that indicates if the click is inside the button
    def is_clicked(self, mouse_position):
        return self.left_side <= mouse_position[0] <= self.right_side and \
            self.top_side <= mouse_position[1] <= self.bottom_side
