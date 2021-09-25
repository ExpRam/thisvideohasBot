import os
import time

import google_auth_oauthlib.flow
import googleapiclient.discovery

from googleapiclient.errors import HttpError


scopes = ["https://www.googleapis.com/auth/youtube.force-ssl","https://www.googleapis.com/auth/youtube.readonly"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"
videoid = ''
print('Starting...')
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)


def main():
    while True:
        snippet = get_stats(videoid)
        result = change_title(videoid, snippet)

        if snippet is None or result is None:
            break
            exit(1)
        time.sleep(9 * 60)


def get_stats(id):
    request = youtube.videos().list(
        part="snippet,statistics",
        id=id
    )

    response = request.execute()

    try:
        snippet = response['items'][0]['snippet']
        stats = response['items'][0]['statistics']
    except IndexError:
        print('Invalid video id!')
        return None

    views = stats['viewCount']
    likes = stats['likeCount']
    dislikes = stats['dislikeCount']
    comments = stats['commentCount']
    title = f'This video has: {views} views, {likes} likes, {dislikes} dislikes, {comments} comments'
    snippet['title'] = title
    return snippet


def change_title(id, snippet):
    request = youtube.videos().update(
        part="snippet",
        body={
            "id": id,
            "snippet": snippet
        }
    )

    try:
        request.execute()
    except HttpError:
        print('Forbidden')
        return None
    return 'Done'


if __name__ == '__main__':
    main()
