import pandas as pd
from sqlalchemy import create_engine
import json
import csv


def read_json():
    f = open('raw1.json')
    data = json.load(f)
    f.close()
    print(data)

def create_db(): 
    try: 
        engine = create_engine('postgresql://username:password@localhost:5432/viper') 
        print(engine)
    except Exception as e:
        print(e)
    #df=pd.read_csv('raw_images.csv') 
    try:
        df=pd.read_json('raw1.json')
        print(df)
        df.to_sql('raw_images', engine)
    except Exception as e:
        print(e) 



if __name__ == "__main__":
    #create_db()
    read_json()
