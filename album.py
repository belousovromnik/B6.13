import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find_album(album_item):
    """
    Находит альбом в базе данных по заданному альбому
    """
    session = connect_db()
    return session.query(Album).filter(func.upper(Album.album) == func.upper(album_item)).all()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(func.upper(Album.artist) == func.upper(artist)).order_by(Album.year).all()
    return albums


def find_dist_artist():
    """
    Находит все всех исполнителей в БД
    """
    session = connect_db()
    return session.query(Album.artist, func.count(Album.artist)).group_by(Album.artist).all()


def add_album(album_data):
    """
    Добавление альбома в БД
    """
    # если все хорошо - возвращаем результатом пусто, в случае ошибки - текст ошибки возвращаем
    result = ''

    album = album_data['album']
    if len(album) == 0:
        result = 'Наименование альбома не может быть пустым'

    year = 0
    try:
        year = int(album_data['year'])
    except ValueError:
        result = 'Год выпуска альбома указан не верно'

    artist = album_data['artist']
    if len(artist) == 0:
        result = 'Наименование исполнителя не может быть пустым'

    if not result:
        album = Album(
            year=year,
            artist=artist,
            genre=album_data['genre'],
            album=album
        )
        session = connect_db()
        session.add(album)
        # сохраняем все изменения, накопленные в сессии
        session.commit()

    return result


if __name__ == "__main__":
    # для тестирования 
    album_data = {
        "year": '2019',
        "artist": 'Spleen',
        "genre": 'Rock',
        "album": 'NewAlbum'
    }
    result = add_album(album_data)
