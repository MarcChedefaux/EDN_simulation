import os
import certifi

if __name__ == "__main__" :
    os.system("python3 -m pip install numpy pandas requests bs4")

    with open(certifi.where(), "a") as fout :
        with open("cert/cngsante.crt", "r") as fin :
            fout.write(fin.read())