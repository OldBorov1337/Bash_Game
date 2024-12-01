import pyodbc
import numpy as np

# Подключение к SQL Server
def get_connection():
    conn = pyodbc.connect(
        "Driver={Your driver};"
        "Server= your server"
        "Database= your database;"
        "Trusted_Connection=yes;"
    )
    return conn


# Создание таблицы
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='boxes' AND xtype='U')
        CREATE TABLE boxes (
            boxeId INT IDENTITY(1,1) PRIMARY KEY,
            boxNumber INT NOT NULL,
            stoneNumber INT NOT NULL
        )
        """)
        conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()


# Очистка базы данных
def clear_database():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM boxes")
        conn.commit()
    except Exception as e:
        print(f"Error clearing database: {e}")
    finally:
        conn.close()


# Инициализация базы данных
def init_replation_database():
    clear_database()  # Очистить базу данных перед инициализацией
    conn = get_connection()
    cursor = conn.cursor()
    stone_list = [1, 2]
    box_numbers = range(1, 12)
    try:
        for box_number in box_numbers:
            for stone_number in stone_list:
                cursor.execute("INSERT INTO boxes (boxNumber, stoneNumber) VALUES (?, ?)", box_number, stone_number)
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()


# Получение данных из базы
def get_boxes_and_stones():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT boxNumber, stoneNumber FROM boxes")
        rows = cursor.fetchall()
        return [[row[0], row[1]] for row in rows]
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
    finally:
        conn.close()


# Выбор хода
def select_stones(player_data, stone_number):
    options = [row[1] for row in player_data if row[0] == stone_number]
    if options:
        return np.random.choice(options)
    else:
        return np.random.choice([1, 2])


# Сохранение обучающего набора
def save_training_set(training_set):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for move in training_set:
            box_number = int(move[0])
            stone_number = int(move[1])
            cursor.execute("INSERT INTO boxes (boxNumber, stoneNumber) VALUES (?, ?)", box_number, stone_number)
        conn.commit()
    except Exception as e:
        print(f"Error saving training set: {e}")
    finally:
        conn.close()


# Основная игра
def play_game(epochs=100):
    for epoch in range(epochs):
        print(f"Epoch {epoch + 1}")
        player_1_data = get_boxes_and_stones()
        player_2_data = get_boxes_and_stones()
        stone_number = 11
        training_set1 = []
        training_set2 = []
        current_player = 1

        while stone_number > 0:
            if current_player == 1:
                move = select_stones(player_1_data, stone_number)
                training_set1.append([stone_number, move])
            else:
                move = select_stones(player_2_data, stone_number)
                training_set2.append([stone_number, move])

            print(f"Player {current_player} takes {move} stones")
            stone_number -= move

            if stone_number == 0:
                print(f"Player {current_player} wins!")
                if current_player == 1:
                    save_training_set(training_set1)
                else:
                    save_training_set(training_set2)
                break

            current_player = 3 - current_player


# Запуск игры
if __name__ == "__main__":
    create_table()
    init_replation_database()
    play_game(epochs=100)
