import pandas as pd

class DataManager:
    def get_names(self):
        file = pd.read_csv("nomes.csv")

        return file['Nomes:'].tolist()
