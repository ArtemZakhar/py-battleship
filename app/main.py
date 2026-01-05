class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks = []
        self.is_drowned = is_drowned
        x_axis = end[0] - start[0]
        y_axis = end[1] - start[1]

        max_axis = max(x_axis, y_axis)

        if start == end:
            self.decks.append(Deck(*start))
            return

        for i in range(max_axis):
            if i == 0:
                self.decks.append(Deck(start[0], start[1]))

            if x_axis > y_axis:
                self.decks.append(Deck(start[0] + 1 + i, start[1]))
            else:
                self.decks.append(Deck(start[0], start[1] + 1 + i))

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column and deck.is_alive:
                return deck

    def fire(self, row: int, column: int) -> str:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        deck.is_alive = False

        if any(rest_deck.is_alive for rest_deck in self.decks):
            return "Hit!"
        else:
            self.is_drowned = True
            return "Sunk!"


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]]
    ) -> None:
        self.field: dict[tuple[int, int], Ship] = {}
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        for ship in ships:
            start, end = ship
            self.field[ship] = Ship(start, end)

    def fire(self, location: tuple[int, int]) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        keys = self.field.keys()
        validated = False
        ship_key = None

        for key in keys:
            start_point = None
            end_point = None
            value_to_check = None

            start, end = key
            if (
                start[0] == end[0] == location[0]
                and start[1] == end[1] == location[1]
            ):
                ship_key = key
                validated = True
                break

            if start[0] == end[0] and start[0] == location[0]:
                start_point = start[1]
                end_point = end[1]
                value_to_check = location[1]
                ship_key = key

            if start[1] == end[1] and start[1] == location[1]:
                start_point = start[0]
                end_point = end[0]
                value_to_check = location[0]
                ship_key = key

            if (
                start_point is not None
                and end_point is not None
                and value_to_check is not None
            ):
                validated = start_point <= value_to_check <= end_point
                if validated:
                    break

        if validated:
            result = self.field[ship_key].fire(*location)
            if any(ship.is_drowned is False for ship in self.field.values()):
                return result
            else:
                return "You won!"

        return "Miss!"
