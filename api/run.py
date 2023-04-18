import time



def run_scipt():
    file = "D:\stropovani_cen_data.xlsx"
    start = time.time()
    proccesor = StatementGenerator(file)
    output_zip_file = proccesor.generate_statements()
    end = time.time()
    print('Time taken: ' + str(end - start))


if __name__ == "__main__":
    run_scipt()

