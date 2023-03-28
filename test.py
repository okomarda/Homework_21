from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def get_free_space(self):
        pass

    @abstractmethod
    def add_item(self, title: str, quantity: int):
        pass

    @abstractmethod
    def remove_item(self, title: str, quantity: int):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def get_unique_items_count(self, value):
        pass

    @abstractmethod
    def check_availability(self, product, amount):
        pass

class Store(Storage):
    """Добавляет скрытые поля: словарь и емкость склада"""
    def __init__(self):
        self._items = {}
        self._capacity = 100

    def get_free_space(self):
        """Определяет наличие свободного места на складе"""
        sum_quantity=sum(self._items.values())
        return self._capacity - sum_quantity

    def add_item(self, title: str, quantity: int):
        """Добавляет товары на склад"""
        while self.get_free_space() > 0 and self.get_free_space() > quantity:
            self._items[title] = self._items.get(title, 0) + quantity
            return f"В хранилище доставлено и размещено {quantity} единиц {title}, осталось {self.get_free_space()} единиц свободных мест"

        self._items[title] = self._items.get (title, 0) + self.get_free_space ( )
        return f"Свободное место для размещения {quantity} единиц {title} отсутствует. Будет размещено товара {title} исходя из доступного количества мест."


    def remove_item(self, title: str, quantity: int):
        """Удаляет товары со склада"""
        if self._items.get (title, 0) > quantity:
            self._items[title] = self._items.get (title, 0) - quantity
            return f"Из хранилища изъято {quantity} единиц {title}"
            return f"В хранилище осталось {quantity} единиц {title}"

        self._items[title] = 0
        return f"В хранилище не осталось товара {title}"

    def get_items(self):
        """Отображает фактическое количество товаров на складе"""
        return self._items

    def get_unique_items_count(self, value):
        """Определеяет уникальные товары, количество которых равно конкретному значению (например,1)"""
        unique_items = [v for v in self._items.values() if v == value]
        return len(unique_items)

    def check_availability(self, product, amount):
        """Проверяет, есть ли необходимое количество товаров на складе"""
        for k in self._items.keys():
            if self._items.get(k) >= amount and k == product:
                return "Нужное количество есть на складе."
        return "Нужного количества нет на складе."

class Shop(Store):
    def __init__(self):
        super().__init__()
        self._capacity = 20

    def add_item(self, title: str, quantity: int):
        while self.get_free_space() > 0 and self.get_free_space() > quantity and len(self._items) < 5:
            self._items[title] = self._items.get(title, 0) + quantity
            return f"В хранилище доставлено и размещено {quantity} единиц {title}, осталось {self.get_free_space()} единиц свободных мест"

        if self.get_free_space() <= 0 and len(self._items) < 5:
                return f"Свободное место для размещения {quantity} единиц {title} отсутствует."
        elif self.get_free_space() < quantity and len(self._items) < 5 :
                self._items[title] = self._items.get (title, 0) + self.get_free_space ( )
                return f"Будет размещено товара {title} исходя из доступного количества мест."
        else:
                return f"Номенклатура товаров магазина достигла {len(self.get_items())}"
class Request():
    def __init__(self, user_str):
        data = self.get_data(user_str)
        self.from_ = data[4]
        self.to = data[6]
        self.amount = int (data[1])
        self.product = data[2]

    def get_data(self, user_str) :
        return user_str.split (" ")

    def __repr__(self) :
        return f'\nПолучен запрос:\nfrom = {self.from_}\nto = {self.to}\namount = {self.amount}\nproduct = {self.product}'

if __name__ == '__main__':
    storage = Store()
    shop = Shop()
    storage.add_item(title='Сушеные_питоны', quantity=5)
    storage.add_item(title='Книги_про_это', quantity= 4)
    storage.add_item(title='Кофе_плохорастворенный', quantity=12)
    storage.add_item (title='Мишки', quantity=1)
    storage.add_item (title='Волки', quantity=15)
    storage.add_item (title='Белки', quantity=80)

    print("Добрый день! Вас приветствует логистическая программа доставки продуктов.")
    print("Сейчас на складе имеется:")
    print(storage.get_items())
    print ("Сейчас в магазине имеется:")
    print (shop.get_items ( ))
    print ("Сейчас свободного места на складе:")
    print(storage.get_free_space())
    print ("Сейчас свободного места в магазине:")
    print (shop.get_free_space ( ))
    user_str = input("Введите свой запрос: ")
    request_1 = Request (user_str)
    print(request_1)
    if request_1.amount <= storage._items.get(request_1.product) and request_1.amount <= shop.get_free_space():
        print("Нужное количество есть на складе")
        print (f"Курьер забрал {request_1.amount} {request_1.product} со {request_1.from_}")
        storage.remove_item(title=str(request_1.product), quantity=int(request_1.amount))
        shop.add_item(title=request_1.product, quantity=request_1.amount)
    elif request_1.amount >= shop.get_free_space():
        print (f"В магазине отсутствует необходимое свободное место, имеется всего {shop.get_free_space ( )} мест")
    elif len(shop._items)>5:
        print((f"В магазине достигнут верхний предел номенклатуры товаров в количестве {len(shop._items)}"))
    else:
        print(f"Нужного количества товаров нет на {request_1.from_}")
        print(f"На {request_1.from_} имеется только {storage._items.get(request_1.product)} {request_1.product}.")
    print(f"\nна {request_1.from_} хранится:\n")
    for product, amount in storage._items.items():
        print(f"{str(product)}: {int(amount)}")
    print(f"\nв {request_1.to} хранится:\n")
    for product, amount in shop._items.items():
        print(f"{str (product)}: {int (amount)}")









    print(storage.get_items())
    print(storage.get_free_space())
    print(storage.get_unique_items_count(1))