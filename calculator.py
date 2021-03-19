
class Calculator():
    def calc_one(self, x, y):
        A1 = 485 - 679
        B1 = 1507 - 552
        C1 = 552*485 - 1507*679

        A2 = 808 - 555
        B2 = 1551 - 470
        C2 = 470*808 - 1551*555
        return A1*x + B1*y + C1, A2*x + B2*y + C2