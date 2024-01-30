import time

from app.filehandle.services import StatementGenerator



def run_scipt():
    file = "C:/Users/JakubUrban/ČEZ Energo, s.r.o/Jiří Března - Zastropování cen EE a ZP/Výkazy/stropovani_cen_data_final.xlsx"
    start = time.time()
    proccesor = StatementGenerator(file)
    proccesor.generate_statements()
    end = time.time()
    print('Time taken: ' + str(end - start))


if __name__ == "__main__":
    run_scipt()


