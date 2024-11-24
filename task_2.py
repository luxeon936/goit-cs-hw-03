from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Підключення до локальної бази даних MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["cats_database"]  # Створення/вибір бази даних
collection = db["cats_collection"]  # Створення/вибір колекції

# Функція для додавання нового кота до бази даних
def create_cat(name, age, features):
    try:
        collection.insert_one({
            "name": name,  # Ім'я кота
            "age": age,  # Вік кота
            "features": features  # Характеристики кота
        })
        print(f"Кіт '{name}' успішно доданий до бази даних.")
    except DuplicateKeyError:
        print("Помилка: Кіт із таким ім'ям вже існує!")  # Помилка дублювання ключа
    except Exception as e:
        print(f"Помилка: {e}")  # Інші помилки

# Функція для виведення усіх котів із бази даних
def read_all_cats():
    try:
        cats = collection.find()  # Пошук усіх записів
        for cat in cats:
            print(cat)  # Виведення записів
    except Exception as e:
        print(f"Помилка: {e}")

# Функція для пошуку кота за іменем
def read_cat_by_name(name):
    try:
        cat = collection.find_one({"name": name})  # Пошук кота за ім'ям
        if cat:
            print(cat)
        else:
            print(f"Кіт з ім'ям '{name}' не знайдений.")  # Якщо не знайдено
    except Exception as e:
        print(f"Помилка: {e}")

# Функція для оновлення віку кота
def update_cat_age(name, new_age):
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})  # Оновлення віку
        if result.matched_count:
            print(f"Вік кота '{name}' оновлено до {new_age}.")
        else:
            print(f"Кіт з ім'ям '{name}' не знайдений.")  # Якщо не знайдено
    except Exception as e:
        print(f"Помилка: {e}")

# Функція для додавання нової характеристики до кота
def add_feature_to_cat(name, feature):
    try:
        result = collection.update_one({"name": name}, {"$addToSet": {"features": feature}})  # Додавання до масиву
        if result.matched_count:
            print(f"До кота '{name}' додано характеристику: {feature}.")
        else:
            print(f"Кіт з ім'ям '{name}' не знайдений.")  # Якщо не знайдено
    except Exception as e:
        print(f"Помилка: {e}")

# Функція для видалення кота за іменем
def delete_cat_by_name(name):
    try:
        result = collection.delete_one({"name": name})  # Видалення запису
        if result.deleted_count:
            print(f"Кіт з ім'ям '{name}' видалений.")
        else:
            print(f"Кіт з ім'ям '{name}' не знайдений.")  # Якщо не знайдено
    except Exception as e:
        print(f"Помилка: {e}")

# Функція для видалення всіх записів
def delete_all_cats():
    try:
        collection.delete_many({})  # Видалення усіх записів
        print("Усі записи видалені з бази даних.")
    except Exception as e:
        print(f"Помилка: {e}")

# Основний код для тестування функцій
if __name__ == "__main__":
    create_cat("Барсик", 3, ["рудий", "дає себе гладити", "ходить в капці"])
    create_cat("Мурзик", 5, ["білий", "грає на піаніно", "ласкавий"])

    print("\nВсі коти в базі:")
    read_all_cats()

    print("\nІнформація про кота 'Барсик':")
    read_cat_by_name("Барсик")

    print("\nОновлення віку 'Барсик':")
    update_cat_age("Барсик", 4)

    print("\nДодавання характеристики до 'Барсик':")
    add_feature_to_cat("Барсик", "грає на піаніно")

    print("\nВидалення кота 'Мурзик':")
    delete_cat_by_name("Мурзик")

    print("\nВидалення всіх записів:")
    delete_all_cats()
