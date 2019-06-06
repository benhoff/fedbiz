import pandas as pd
from leadgen import config
from leadgen import get_fbo_attachments
from leadgen.db import db
from leadgen.db.db_utils import get_db_url, session_scope, DataAccessLayer
from leadgen.predict import Predict
from code import interact
import shutil
from itertools import islice

def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())

# files = ['1.csv']
# files = ['1.csv', '2.csv', '3.csv', '4.csv', '5.csv']
files = ['2.csv', '3.csv', '4.csv', '5.csv']

data_access = DataAccessLayer(config.sql_path)
data_access.connect()
session = data_access.Session()
predict = Predict(None, model_path='/home/ubuntu/rpa-ml.pkl')

for f in files:
    df = pd.read_csv(f)
    all_urls = ['https://www.fbo.gov' + s for s in df['url'] if isinstance(s, str)]
    iter_urls = chunk(all_urls, 100)
    for index, urls in enumerate(iter_urls):
        print("Getting data " + str(index))
        data = get_fbo_attachments.FboAttachments.get_data(urls)
        print("Getting Predictions" + str(index))
        predict.get_predictions(data)
        counter = 0
        for d in data:
            for doc in d['attachments']:
                attachment =  db.Attachment(filename = doc['filename'],
                                            machine_readable = doc['machine_readable'],
                                            attachment_text = doc['text'],
                                            prediction = doc['prediction'],
                                            decision_boundary = doc['decision_boundary'],
                                            validation = doc['validation'],
                                            attachment_url = doc['url'],
                                            trained = doc['trained'])
                session.add(attachment)
                counter += 1
                if counter > 10:
                    counter = 0
                    print("Commiting " + str(index))
                    session.commit()

    shutil.rmtree('attachments')
