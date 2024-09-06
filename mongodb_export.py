import csv
from pymongo import MongoClient


def main():
    db_host='localhost'
    db_port=27017
    db_user='sg4mongo'
    db_password='h8pCJthItB3bw464'
    db_name='stt_api'
    out_path='out.csv'

    client = MongoClient("mongodb://sg4mongo:h8pCJthItB3bw464@localhost", 27017, maxPoolSize=50)

    db = client['stt_api']
    collection = db['transcribedclips']
    cursor = collection.find({})
    transcriptions = []
    for transcribed_clip in collection.find({}):
        if "!DOCTYPE html" in transcribed_clip['transcription']:
            continue

        transcription = {
                'id': str(transcribed_clip['id'].as_uuid(3)),
                'created': transcribed_clip['created'].strftime("%Y-%m-%d %H:%M:%S"),
                'clip': transcribed_clip['audio_file'],
                'transcription': transcribed_clip['transcription'],
                'rating': None if len(transcribed_clip['ratings']) == 0 else transcribed_clip['ratings'][0]['rating']
        }
        print(transcription)
        transcriptions.append(transcription)

    csv_columns = ['id', 'created', 'clip', 'transcription', 'rating']
    with open(out_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in transcriptions:
            writer.writerow(data)


if __name__ == '__main__':
    main()