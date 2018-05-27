from requests import get
from priority_queue import PriorityQueue


def get_user_id(user_name,access_token):
    a=get('https://api.vk.com/method/utils.resolveScreenName?screen_name={}&access_token={}&v=5.74'.format(user_name, access_token)).json()["response"]
    return a['object_id']


def get_friends(user_id, access_token):
    a = get('https://api.vk.com/method/friends.get?user_id={}&access_token={}&v=5.74'.format(user_id,access_token)).json()["response"]["items"]
    return a

def get_user_name(user_id, access_token):
    user = get('https://api.vk.com/method/users.get?user_ids={}&access_token={}&v=5.74'.format(user_id,access_token)).json()["response"][0]
    return user["first_name"] + " " + user["last_name"]


def get_user_friends_count(user_id, access_token):
    return len(get_friends(user_id, access_token))


def get_user_photos_likes(user_id, access_token):
    photos = get('https://api.vk.com/method/photos.get?owner_id={}&album_id=profile&extended=1&access_token={}&v=5.74'.format(user_id,access_token)).json()["response"]
    a = sum(int(i['likes']["count"]) for i in photos["items"])
    return a


def get_friends_sorted_by_popularity(user_id, access_token):
    a = 1
    q = PriorityQueue()
    for i in get_friends(user_id, access_token):
        try:
            print(a)
            a+=1
            q.enqueue(get_user_name(i, access_token), get_user_friends_count(i, access_token) + get_user_photos_likes(i,access_token))
        except Exception:
            pass
    while not q.empty:
        yield q.dequeue()


def main():
    try:
        user_id = input("Введите id или имя пользователя: ")
        access_token = "e886e972e886e972e886e97218e8e4ef4eee886e886e972b27d5f2420099a0bae2a5d4b"
        friend_number = 1
        if not user_id.isnumeric():
            user_id = get_user_id(user_id, access_token)
        for (friend_name, popularity) in get_friends_sorted_by_popularity(user_id, access_token):
            print("{}) {}. Популярность = {}".format(friend_number, friend_name, popularity))
            friend_number += 1
    except Exception:
        print('Что-то пошло не так :(')

if __name__ == "__main__":
    main()
