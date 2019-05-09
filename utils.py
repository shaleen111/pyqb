
# BASIC ERROR HANDLING


class BasicError(Exception):
    def __init__(self, errdesc, pos_start, pos_end):
        self.errdesc = errdesc
        self.pos_start = pos_start
        self.pos_end = pos_end

    def arrows(self, pos_start, pos_end):
        # zero-indexed
        space = ""
        arr = ""
        for i in range(0, pos_start):
            space += " "

        for i in range(pos_start, pos_end + 1):
            arr += "^"

        return space + arr

    def gen_err(self, errloc):
        print(self.errdesc)
        print("\t" + errloc)
        print("\t" + self.arrows(self.pos_start, self.pos_end))

# OPERATORS
RELATIONAL_OPERATORS = ("DEQUAL", "EQUAL", "NEQUAL", "LEQ", "GEQ",
                        "GREATERTHAN", "LESSTHAN")
