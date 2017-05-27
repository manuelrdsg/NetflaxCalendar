from celery import Celery
import json
import dropbox
import credentials
from dropbox.files import WriteMode

token = credentials.dropbox_token
dbx = dropbox.Dropbox(token)

app = Celery(
    'download',
    broker='pyamqp://guest@localhost//',
    backend = 'rpc://'
)

@app.task
def update(day, month, year, name):

    path = "/netflax.json"
    file_temp = "netflax.json"
    dbx.files_download_to_file(file_temp, path)

    with open(file_temp,"r") as f:
        data = f.read()

    d = json.loads(data)

    # Now, separate info from the tweet which has just been tweeted
    num_of_elements = len(d)
    id = num_of_elements

    d[id+1] = {
        "Day":day,
        "Month":month,
        "Year":year,
        "Name":name
    }

    print(type(d))
    print(type(data))

    # Encode again to JSON
    data = json.dumps(d)
    with open("netflax.json","w") as f:
        f.write(data)

    # And finally, returns it to Dropbox!
    with open("netflax.json", "rb") as f:
        data = f.read();

    response = dbx.files_upload(data, path, mode=WriteMode('overwrite'))
    print(response);
