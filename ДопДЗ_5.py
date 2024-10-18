import hashlib
import time

class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        # Хэшируем пароль
        self.password = int(hashlib.sha256(password.encode()).hexdigest(), 16)
        self.age = age

    def __str__(self):
        return self.nickname


class Video:
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration  # В секундах
        self.time_now = 0  # Время остановки
        self.adult_mode = adult_mode  # Ограничение по возрасту

    def __str__(self):
        return self.title


class UrTube:
    def __init__(self):
        self.users = []  # Список пользователей
        self.videos = []  # Список видео
        self.current_user = None  # Текущий пользователь

    def log_in(self, nickname, password):
        # Пробуем найти пользователя по имени и хэшированному паролю
        password_hash = int(hashlib.sha256(password.encode()).hexdigest(), 16)
        for user in self.users:
            if user.nickname == nickname and user.password == password_hash:
                self.current_user = user
                print(f"{user.nickname} успешно вошёл в систему")
                return
        print("Неверный логин или пароль")

    def register(self, nickname, password, age):
        # Проверяем, существует ли пользователь с таким никнеймом
        for user in self.users:
            if user.nickname == nickname:
                print(f"Пользователь {nickname} уже существует")
                return
        # Если пользователь не существует, создаём нового и автоматически входим
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user
        print(f"Пользователь {nickname} зарегистрирован и вошёл в систему")

    def log_out(self):
        if self.current_user:
            print(f"{self.current_user.nickname} вышел из системы")
            self.current_user = None
        else:
            print("Никто не авторизован")

    def add(self, *videos):
        for video in videos:
            # Проверяем, есть ли уже видео с таким названием
            if any(v.title == video.title for v in self.videos):
                continue
            self.videos.append(video)
            print(f"Видео '{video.title}' добавлено")

    def get_videos(self, search_term):
        search_term_lower = search_term.lower()
        found_videos = [video.title for video in self.videos if search_term_lower in video.title.lower()]
        return found_videos

    def watch_video(self, title):
        if not self.current_user:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

        # Ищем видео с точным названием
        video_to_watch = next((video for video in self.videos if video.title == title), None)
        if not video_to_watch:
            print("Видео не найдено")
            return

        # Проверяем возрастное ограничение
        if video_to_watch.adult_mode and self.current_user.age < 18:
            print("Вам нет 18 лет, пожалуйста покиньте страницу")
            return

        # Воспроизводим видео, начиная с момента остановки
        for second in range(video_to_watch.time_now + 1, video_to_watch.duration + 1):
            print(second, end=' ', flush=True)
            time.sleep(1)  # Пауза в 1 секунду для симуляции реального времени просмотра

        # Видео просмотрено, сбрасываем время остановки
        video_to_watch.time_now = 0
        print("\nКонец видео")


# Примеры использования:

ur = UrTube()

v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))  # ['Лучший язык программирования 2024 года']
print(ur.get_videos('ПРОГ'))  # ['Лучший язык программирования 2024 года', 'Для чего девушкам парень программист?']

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')  # "Войдите в аккаунт, чтобы смотреть видео"
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')  # "Вам нет 18 лет, пожалуйста покиньте страницу"
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')  # Видео воспроизводится с выводом секунд

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)  # Пользователь с таким ником уже существует
print(ur.current_user)  # urban_pythonist

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')  # Видео не найдено
