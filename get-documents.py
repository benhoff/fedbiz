import pandas as pd
from leadgen import config
from leadgen import get_fbo_attachments
from leadgen.db import db
from leadgen.db.db_utils import get_db_url, session_scope, DataAccessLayer
from leadgen.predict import Predict

files = ['1.csv']
# files = ['1.csv', '2.csv', '3.csv', '4.csv', '5.csv']

data_access = DataAccessLayer(config.sql_path)
data_access.connect()
predict = Predict(None, model_path='/Users/hoff/swdev/srt-fbo-scraper/models/rpa-ml.pkl')

for f in files:
    df = pd.read_csv(f)
    urls = ['https://www.fbo.gov' + s for s in df['url']]
    data = get_fbo_attachments.FboAttachments.get_data(urls)
    # NOTE: is expecting `attachments` and
    data = predict.get_predictions(data)
    print(data)
    counter = 0
    for doc in data:
        attachment =  db.Attachment(notice_type_id = notice_type_id,
                                    filename = doc['filename'],
                                    machine_readable = doc['machine_readable'],
                                    attachment_text = doc['text'],
                                    prediction = doc['prediction'],
                                    decision_boundary = doc['decision_boundary'],
                                    validation = doc['validation'],
                                    attachment_url = doc['url'],
                                    trained = doc['trained'])
        data_access.Session.add(attachment)
        counter += 1
        if counter > 10:
            counter = 0
            data_access.Session.commit()
