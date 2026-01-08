import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagram_project.settings')
django.setup()

from instagram_app.models import UserProfile, Follow, Post, PostContent, PostLike, Comment, CommentLike
from django.core.files.base import ContentFile
from PIL import Image
import io


def create_fake_image(username):
    """Создает простое изображение для аватара"""
    img = Image.new('RGB', (200, 200),
                    color=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return ContentFile(buffer.read(), name=f'{username}_avatar.jpg')


def create_fake_post_image(post_id):
    """Создает простое изображение для поста"""
    img = Image.new('RGB', (600, 600),
                    color=(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)))
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return ContentFile(buffer.read(), name=f'post_{post_id}.jpg')


def clear_data():
    """Очищает все данные"""
    print("Очистка данных...")
    CommentLike.objects.all().delete()
    Comment.objects.all().delete()
    PostLike.objects.all().delete()
    PostContent.objects.all().delete()
    Post.objects.all().delete()
    Follow.objects.all().delete()
    UserProfile.objects.filter(is_superuser=False).delete()
    print("Данные очищены")


def create_users():
    """Создает пользователей"""
    print("Создание пользователей...")
    users_data = [
        {
            'username': 'anna_ivanova',
            'email': 'anna.ivanova@email.com',
            'first_name': 'Анна',
            'last_name': 'Иванова',
            'bio': 'Люблю путешествовать 🌍 | Фотография моя страсть 📸 | Кофе - моя слабость ☕',
            'is_official': False,
            'user_link': 'https://annaivanova.com',
            'phone_number': '+996555123456'
        },
        {
            'username': 'dmitry_petrov',
            'email': 'dmitry.petrov@email.com',
            'first_name': 'Дмитрий',
            'last_name': 'Петров',
            'bio': 'Фитнес тренер 💪 | Мотивационный спикер | Живу полной жизнью',
            'is_official': True,
            'user_link': 'https://dmitryfit.com',
            'phone_number': '+996555234567'
        },
        {
            'username': 'elena_smirnova',
            'email': 'elena.smirnova@email.com',
            'first_name': 'Елена',
            'last_name': 'Смирнова',
            'bio': 'Фуд блогер 🍕 | Создаю рецепты | Обожаю готовить',
            'is_official': True,
            'user_link': 'https://elenacooks.com',
            'phone_number': '+996555345678'
        },
        {
            'username': 'alex_volkov',
            'email': 'alex.volkov@email.com',
            'first_name': 'Александр',
            'last_name': 'Волков',
            'bio': 'IT специалист 💻 | Обзоры гаджетов | Всегда на связи',
            'is_official': False,
            'user_link': 'https://alextech.com',
            'phone_number': '+996555456789'
        },
        {
            'username': 'maria_novikova',
            'email': 'maria.novikova@email.com',
            'first_name': 'Мария',
            'last_name': 'Новикова',
            'bio': 'Модельер ✨ | Икона стиля | Живу в Бишкеке',
            'is_official': True,
            'user_link': 'https://mariafashion.com',
            'phone_number': '+996555567890'
        },
        {
            'username': 'sergey_kozlov',
            'email': 'sergey.kozlov@email.com',
            'first_name': 'Сергей',
            'last_name': 'Козлов',
            'bio': 'Музыкальный продюсер 🎵 | DJ | Живу музыкой',
            'is_official': False,
            'user_link': 'https://sergeybeats.com',
            'phone_number': '+996555678901'
        }
    ]

    users = []
    for user_data in users_data:
        user = UserProfile.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password='password123',
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            bio=user_data['bio'],
            is_official=user_data['is_official'],
            user_link=user_data['user_link'],
            phone_number=user_data['phone_number']
        )
        user.user_image = create_fake_image(user.username)
        user.save()
        users.append(user)
        print(f"Создан пользователь: {user.username}")

    return users


def create_follows(users):
    """Создает подписки между пользователями"""
    print("\nСоздание подписок...")
    follows = []

    # Каждый пользователь подписывается на случайных других пользователей
    for user in users:
        # Выбираем 3-4 случайных пользователей для подписки
        num_follows = random.randint(3, 4)
        potential_follows = [u for u in users if u != user]
        to_follow = random.sample(potential_follows, min(num_follows, len(potential_follows)))

        for followed_user in to_follow:
            follow = Follow.objects.create(
                follower=user,
                following=followed_user
            )
            follows.append(follow)
            print(f"{user.username} подписался на {followed_user.username}")

    return follows


def create_posts(users):
    """Создает посты"""
    print("\nСоздание постов...")
    posts_data = [
        {'description': 'Невероятный закат на берегу 🌅 #закат #море #природа', 'hashtag': 'закат'},
        {'description': 'Моя утренняя тренировка 💪 #фитнес #мотивация #спорт', 'hashtag': 'фитнес'},
        {'description': 'Вкусная домашняя паста 🍝 #еда #готовка #паста', 'hashtag': 'еда'},
        {'description': 'Распаковка нового гаджета! #технологии #гаджеты #обзор', 'hashtag': 'технологии'},
        {'description': 'Атмосфера недели моды ✨ #мода #стиль #образдня', 'hashtag': 'мода'},
        {'description': 'Ночная студийная сессия 🎵 #музыка #продюсер #биты', 'hashtag': 'музыка'},
        {'description': 'Прогулка по городу 🏙️ #бишкек #прогулка #город', 'hashtag': 'бишкек'},
        {'description': 'Вкусный завтрак 🥞 #завтрак #еда #вкусно', 'hashtag': 'завтрак'},
        {'description': 'Новый день - новые возможности 🌟 #мотивация #жизнь #успех', 'hashtag': 'мотивация'},
        {'description': 'Красота природы Кыргызстана 🏔️ #кыргызстан #горы #природа', 'hashtag': 'кыргызстан'},
        {'description': 'Вечерний город 🌃 #вечер #город #красота', 'hashtag': 'вечер'},
        {'description': 'Любимое хобби 🎨 #хобби #творчество #искусство', 'hashtag': 'хобби'},
    ]

    posts = []
    for i, user in enumerate(users):
        # Каждый пользователь создает 5-6 постов
        num_posts = random.randint(5, 6)
        for j in range(num_posts):
            post_data = random.choice(posts_data)
            days_ago = random.randint(0, 30)

            post = Post.objects.create(
                user=user,
                description=post_data['description'],
                hashtag=post_data['hashtag']
            )
            # Устанавливаем дату создания в прошлом
            post.created_date = (datetime.now() - timedelta(days=days_ago)).date()
            post.save()

            # Создаем контент для поста
            post_content = PostContent.objects.create(
                post=post,
                post_content=create_fake_post_image(post.id)
            )

            posts.append(post)
            print(f"Создан пост #{post.id} от {user.username}")

    return posts


def create_post_likes(users, posts):
    """Создает лайки на посты"""
    print("\nСоздание лайков на посты...")
    likes = []

    for post in posts:
        # Случайное количество лайков (3-8)
        num_likes = random.randint(3, 8)
        # Выбираем случайных пользователей, исключая автора поста
        potential_likers = [u for u in users if u != post.user]
        likers = random.sample(potential_likers, min(num_likes, len(potential_likers)))

        for liker in likers:
            like = PostLike.objects.create(
                post=post,
                user=liker,
                like=True
            )
            likes.append(like)

    print(f"Создано {len(likes)} лайков на посты")
    return likes


def create_comments(users, posts):
    """Создает комментарии к постам"""
    print("\nСоздание комментариев...")
    comments_text = [
        'Потрясающе! 😍',
        'Обожаю! ❤️',
        'Как красиво!',
        'Отличный контент!',
        'Так держать! 💪',
        'Это великолепно!',
        'Жду еще!',
        'Вдохновляет! ✨',
        'Невероятно красиво!',
        'Браво! 👏',
        'Супер! 🔥',
        'Класс! 👍',
        'Круто! 😎',
        'Шикарно! ✨',
        'Восхитительно! 🌟',
        'Молодец! 👌',
        'Красавчик! 💯',
        'Огонь! 🔥',
        'Талант! 🎨',
        'Мне нравится! 💖'
    ]

    comments = []
    for post in posts:
        # Каждый пост получает 4-6 комментариев
        num_comments = random.randint(4, 6)

        for i in range(num_comments):
            commenter = random.choice([u for u in users if u != post.user])
            comment = Comment.objects.create(
                post=post,
                user=commenter,
                text=random.choice(comments_text)
            )
            comments.append(comment)

            # Некоторые комментарии получают ответы
            if random.random() < 0.3:  # 30% шанс
                replier = random.choice(users)
                reply = Comment.objects.create(
                    post=post,
                    user=replier,
                    text=random.choice(comments_text),
                    parent=comment
                )
                comments.append(reply)

    print(f"Создано {len(comments)} комментариев")
    return comments


def create_comment_likes(users, comments):
    """Создает лайки на комментарии"""
    print("\nСоздание лайков на комментарии...")
    likes = []

    for comment in comments:
        # Случайное количество лайков (2-5)
        num_likes = random.randint(2, 5)
        # Выбираем случайных пользователей
        potential_likers = [u for u in users if u != comment.user]
        likers = random.sample(potential_likers, min(num_likes, len(potential_likers)))

        for liker in likers:
            like = CommentLike.objects.create(
                comment=comment,
                user=liker,
                like=True
            )
            likes.append(like)

    print(f"Создано {len(likes)} лайков на комментарии")
    return likes


def main():
    print("=" * 50)
    print("Запуск скрипта наполнения базы данных")
    print("=" * 50)

    # Очищаем старые данные
    clear_data()

    # Создаем данные
    users = create_users()
    follows = create_follows(users)
    posts = create_posts(users)
    post_likes = create_post_likes(users, posts)
    comments = create_comments(users, posts)
    comment_likes = create_comment_likes(users, comments)

    print("\n" + "=" * 50)
    print("Статистика:")
    print(f"Пользователей: {len(users)}")
    print(f"Подписок: {len(follows)}")
    print(f"Постов: {len(posts)}")
    print(f"Лайков на посты: {len(post_likes)}")
    print(f"Комментариев: {len(comments)}")
    print(f"Лайков на комментарии: {len(comment_likes)}")
    print("=" * 50)
    print("✅ Скрипт успешно завершен!")
    print("\nДанные для входа:")
    print("Логин: anna_ivanova, Пароль: password123")
    print("Логин: dmitry_petrov, Пароль: password123")
    print("Логин: elena_smirnova, Пароль: password123")
    print("Логин: alex_volkov, Пароль: password123")
    print("Логин: maria_novikova, Пароль: password123")
    print("Логин: sergey_kozlov, Пароль: password123")


if __name__ == '__main__':
    main()