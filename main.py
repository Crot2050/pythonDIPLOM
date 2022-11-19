import requests, json, time, os, sys
from pprint import pprint
from tqdm import tqdm

VK_USER_ID = input('Введите id пользователя vk: ')
VK_TOKEN = ''
YA_TOKEN = ''

class VkLoading:

    def __init__(self, vk_token):
        self.vk_token = VK_TOKEN

#Собираем информацию о  фото в  Vk
    def get_photo_data(offset=0, count=5):
        vk_url = requests.get('https://api.vk.com/method/photos.get', params={
            'owner_id': VK_USER_ID,
            'access_token': VK_TOKEN,
            'offset': offset,
            'count': count,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 0,
            'v': '5.131'
        })
        get_photos = requests.get(method_photos_get, params=params)
        if get_photos.status_code == 200:
            info_json = get_photos.json()
            return info_json.get('response')
        sys.exit(f"Ошибка ответа, код: {get_photos.status_code}")

#Делаем выборку фото
    def selection_photos(self):
        photos_items = self.get_photo_data().get('items')
        selection_list = []
        json_file = {
            "count": self.count,
            "info": selection_list
                    }
        for photo_info in photos_items:
            count_likes = photo_info['likes']['count']
            max_size_url = find_max_size_photos(photo_info['sizes'])
            date_of_download = time_convert(photo_info['date'])
            selection_list.append({
                "name": f"{count_likes}.jpg",
                "id": photo_info['id'],
                'date': date_of_download[0],
                'time': date_of_download[1],
                "likes": count_likes,
                'url': max_size_url[0],
                'size': max_size_url[1]
                                   })
        return json_file


 class YaDisk:
    def __init__(self):
        self.token = YA_TOKEN
        self.headers = {'Authorization': self.token}

#Создаем папку
    def create_folder(self):
        params = {
            "path": self.folder_path
        }
        create_folder = requests.put(self.url, headers=self.headers, params=params)
        if create_folder.status_code == 409:
            return f'Здесь /{self.folder_path} уже существует папка '
        elif create_folder.status_code != 201 != 409:
            sys.exit(f"Ошибка ответа, код: {create_folder.status_code}")
        return f'Здесь /{self.folder_path} папка успешно создана'

# Загружаем фото
    def upload_files(self, info_list):
        print(self.create_folder())
        url_upload = self.url + "/upload"
        info = info_list['info']
        for index in tqdm(range(len(info)), desc="Прогресс загрузки фото", unit=" File"):
            name = info[index]['name']
            url_photo = info[index]['url']
            params = {
                "path": f"{self.folder_path}/{name}",
                "url": url_photo
            }
            upload_photo = requests.post(url_upload, headers=self.headers, params=params)
            if upload_photo.status_code != 202:
                self.delete_folder()
                sys.exit(f"Ошибка ответа, код: {upload_photo.status_code}
        return "Все файлы успешно загружены"

if __name__ == '__main__':
    json_name = input('Введите название папки:')
    VKreq = VKRequest(VK_TOKEN)
    with open(json_name + ".json", "w") as file:
        json.dump(VKreq.json_info_photos(), file, indent=4)
    yandex = YAuploader(yatoken, json_name)
    print(yandex.upload_files(VKreq.json_info_photos()))
