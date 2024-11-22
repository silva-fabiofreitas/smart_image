from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

load_dotenv()

from graph.graph import app

if __name__ == '__main__':
    res = app.invoke({'image_path': 'data/imgs/'})
    df = pd.DataFrame([table.dict() for table in res['descriptions']])
    df.to_csv(f'classificacao: {datetime.now()}.csv', sep=';')