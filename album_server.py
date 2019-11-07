from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album as album_proc


@route("/album/<album_item>")
def albums(album_item):
    album_list = album_proc.find_album(album_item)
    result = ''
    if not album_list:
        message = "Альбом {} не найден".format(album_item)
        result = HTTPError(404, message)
    else:
        for album in album_list:
            result += "Информация по альбому {}<br>".format(album.album)
            result += '<br>'
            result += "Год выпуска {}<br>".format(album.year)
            result += "Исполнитель {}<br>".format(album.artist)
            result += "Жанр {}<br>".format(album.genre)
    return result


@route("/albums/<artist>")
def albums(artist):
    albums_list = album_proc.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        # album_names = [album.album for album in albums_list]
        result = "Список альбомов {} - {} альбомов<br>".format(artist, len(albums_list))
        result += '<br>'
        # result += "<br>".join(album_names)

        i = 1
        for album in albums_list:
            result += '{}. {} год - альбом {}<br>'.format(i, album.year, album.album)
            i += 1

    return result


@route("/albums", method="POST")
def album_new():
    """
        пример запроса
        http -f POST localhost:8090/albums year=2019 artist=Spleen genre=Rock album=NewAlbum
    """
    album_new_album = request.forms.get("album")
    # ищем, есть ли такой альбом в БД или нет
    album_find = album_proc.find_album(album_new_album)
    if album_find:
        message = "Альбом {} уже найден в БД".format(album_new_album)
        HTTPError(409, message)
    else:
        album_data = {
            "year": request.forms.get("year"),
            "artist": request.forms.get("artist"),
            "genre": request.forms.get("genre"),
            "album": album_new_album
        }
        # если получаем сообщение - это сообщение об ошибке, иначе - если получаем пусто - все хорошо
        message = album_proc.add_album(album_data)
        if message:
            HTTPError(409, message)
        else:
            message = 'Запись добавлена'

    return message


@route("/artists")
def albums():
    artists_list = album_proc.find_dist_artist()
    if not artists_list:
        message = "Исполнителей не найдено"
        result = HTTPError(404, message)
    else:
        result = 'Список исполнителей, количество альбомов:<br>'
        for artist_name, artist_cnt in artists_list:
            result += '{} - {}<br>'.format(artist_name, artist_cnt)
    return result


if __name__ == "__main__":
    run(host="localhost", port=8090, debug=True)
