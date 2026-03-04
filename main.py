
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import os



class Size(Enum):
    SMALL  = ("Small",  1.0)
    MEDIUM = ("Medium", 1.3)
    LARGE  = ("Large",  1.6)

    def __init__(self, label, multiplier):
        self.label      = label
        self.multiplier = multiplier

    def __str__(self):
        return self.label


class CoffeeType(Enum):
    HOT     = "☕ Hot"
    COLD    = "🧊 Cold"
    BLENDED = "🥤 Blended"


class AddOn(Enum):
    EXTRA_SHOT    = ("Extra Shot",    30)
    OAT_MILK      = ("Oat Milk",      40)
    WHIPPED_CREAM = ("Whipped Cream", 25)
    CARAMEL_SYRUP = ("Caramel Syrup", 20)
    VANILLA_SYRUP = ("Vanilla Syrup", 20)

    def __init__(self, label, price):
        self.label = label
        self.price = price

    def __str__(self):
        return f"{self.label} (+Rs.{self.price})"



#  ABSTRACT BASE CLASS


class BaseBeverage(ABC):
    """Abstract class — sab coffees isse inherit karenge"""

    def __init__(self, name: str, base_price: float, coffee_type: CoffeeType):
        self._name        = name
        self._base_price  = base_price
        self._coffee_type = coffee_type

    # --- Properties (Encapsulation) ---
    @property
    def name(self):
        return self._name

    @property
    def base_price(self):
        return self._base_price

    @property
    def coffee_type(self):
        return self._coffee_type

    # --- Abstract Methods (Polymorphism) ---
    @abstractmethod
    def prepare(self, size: Size) -> str:
        pass

    @abstractmethod
    def get_price(self, size: Size) -> float:
        pass

    # --- Magic Methods ---
    def __str__(self):
        return f"{self._coffee_type.value}  {self._name:<20} Rs.{self._base_price:.0f}"

    def __repr__(self):
        return f"<{self.__class__.__name__}(name={self._name!r})>"



#  CONCRETE COFFEE CLASSES (Inheritance)


class HotCoffee(BaseBeverage):
    def __init__(self, name: str, base_price: float):
        super().__init__(name, base_price, CoffeeType.HOT)

    def prepare(self, size: Size) -> str:
        return f"Brewing hot {self._name} ({size.label})... Steaming milk... Done!"

    def get_price(self, size: Size) -> float:
        return round(self._base_price * size.multiplier, 2)


class ColdCoffee(BaseBeverage):
    def __init__(self, name: str, base_price: float):
        super().__init__(name, base_price, CoffeeType.COLD)

    def prepare(self, size: Size) -> str:
        return f"Chilling {self._name} ({size.label})... Adding ice... Done!"

    def get_price(self, size: Size) -> float:
        return round(self._base_price * size.multiplier + 10, 2)  # +10 for ice


class BlendedCoffee(BaseBeverage):
    def __init__(self, name: str, base_price: float):
        super().__init__(name, base_price, CoffeeType.BLENDED)

    def prepare(self, size: Size) -> str:
        return f"Blending {self._name} ({size.label})... Whirring... Done!"

    def get_price(self, size: Size) -> float:
        return round(self._base_price * size.multiplier + 20, 2)  # +20 for blending



#  DATACLASS — OrderItem


@dataclass
class OrderItem:
    beverage : BaseBeverage
    size     : Size
    add_ons  : list = field(default_factory=list)

    @property
    def total_price(self) -> float:
        addon_total = sum(a.price for a in self.add_ons)
        return round(self.beverage.get_price(self.size) + addon_total, 2)

    def __str__(self):
        addon_str = ", ".join(a.label for a in self.add_ons) or "None"
        return (
            f"  • {self.beverage.name} ({self.size.label})\n"
            f"    Add-ons : {addon_str}\n"
            f"    Price   : Rs.{self.total_price:.0f}"
        )



#  ORDER CLASS


class Order:
    _order_counter = 0  # Class variable

    def __init__(self, customer_name: str):
        Order._order_counter += 1
        self._order_id      = Order._order_counter
        self._customer_name = customer_name
        self._items         : list[OrderItem] = []
        self._timestamp     = datetime.now()
        self._is_paid       = False

    # --- Class Method ---
    @classmethod
    def total_orders_placed(cls) -> int:
        return cls._order_counter

    # --- Static Method ---
    @staticmethod
    def format_price(price: float) -> str:
        return f"Rs.{price:.0f}"

    def add_item(self, item: OrderItem):
        self._items.append(item)

    @property
    def subtotal(self) -> float:
        return round(sum(i.total_price for i in self._items), 2)

    @property
    def tax(self) -> float:
        return round(self.subtotal * 0.05, 2)  # 5% tax

    @property
    def grand_total(self) -> float:
        return round(self.subtotal + self.tax, 2)

    @property
    def is_paid(self):
        return self._is_paid

    def pay(self):
        self._is_paid = True

    # --- Magic Methods ---
    def __len__(self):
        return len(self._items)

    def __str__(self):
        lines = [
            f"\n{'═'*40}",
            f"  ORDER #{self._order_id}  |  {self._customer_name}",
            f"  {self._timestamp.strftime('%d %b %Y, %I:%M %p')}",
            f"{'─'*40}",
        ]
        for item in self._items:
            lines.append(str(item))
        lines += [
            f"{'─'*40}",
            f"  Subtotal : {Order.format_price(self.subtotal)}",
            f"  Tax (5%) : {Order.format_price(self.tax)}",
            f"  TOTAL    : {Order.format_price(self.grand_total)}",
            f"  Status   : {'Paid' if self._is_paid else 'Pending'}",
            f"{'═'*40}",
        ]
        return "\n".join(lines)



#  MENU (Encapsulation + Class Methods)


class Menu:
    _items: list[BaseBeverage] = [
        HotCoffee("Espresso",       150),
        HotCoffee("Cappuccino",     200),
        HotCoffee("Latte",          220),
        HotCoffee("Americano",      180),
        ColdCoffee("Iced Latte",    230),
        ColdCoffee("Cold Brew",     250),
        ColdCoffee("Iced Mocha",    260),
        BlendedCoffee("Frappuccino",280),
        BlendedCoffee("Mocha Blend",290),
    ]

    @classmethod
    def display(cls):
        print(f"\n{'═'*45}")
        print(f"  ☕  WELCOME TO BADDIE'S COFFEE  ☕")
        print(f"{'═'*45}")
        current_type = None
        for i, item in enumerate(cls._items, 1):
            if item.coffee_type != current_type:
                current_type = item.coffee_type
                print(f"\n  {current_type.value}")
                print(f"  {'─'*35}")
            print(f"  [{i}] {item}")
        print(f"{'═'*45}")

    @classmethod
    def get_item(cls, index: int) -> BaseBeverage:
        return cls._items[index - 1]

    @classmethod
    def count(cls) -> int:
        return len(cls._items)



#  COFFEE SHOP (Main controller)


class CoffeeShop:
    def __init__(self, shop_name: str):
        self._shop_name    = shop_name
        self._order_history: list[Order] = []

    def _clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def _get_int(self, prompt: str, min_val: int, max_val: int) -> int:
        while True:
            try:
                val = int(input(prompt))
                if min_val <= val <= max_val:
                    return val
                print(f"Please enter a number between {min_val} and {max_val}.")
            except ValueError:
                print("Invalid input. Enter a number.")

    def _choose_size(self) -> Size:
        sizes = list(Size)
        print("\n  📏 Choose Size:")
        for i, s in enumerate(sizes, 1):
            print(f"  [{i}] {s.label}")
        choice = self._get_int("  → ", 1, len(sizes))
        return sizes[choice - 1]

    def _choose_addons(self) -> list:
        addons = list(AddOn)
        print("\n  🧪 Add-ons (enter numbers separated by comma, or press Enter to skip):")
        for i, a in enumerate(addons, 1):
            print(f"  [{i}] {a}")
        raw = input("  → ").strip()
        if not raw:
            return []
        selected = []
        for part in raw.split(","):
            part = part.strip()
            if part.isdigit():
                idx = int(part)
                if 1 <= idx <= len(addons):
                    selected.append(addons[idx - 1])
        return selected

    def _take_order(self, customer_name: str) -> Order:
        order = Order(customer_name)

        while True:
            self._clear()
            Menu.display()
            print(f"\n  Items in cart: {len(order)}")
            print(f"  [0] Done / View Cart")
            choice = self._get_int("\n  Select coffee number: ", 0, Menu.count())

            if choice == 0:
                break

            beverage = Menu.get_item(choice)
            size     = self._choose_size()
            add_ons  = self._choose_addons()

            item = OrderItem(beverage, size, add_ons)
            order.add_item(item)

            print(f"\nAdded: {beverage.name} ({size.label}) — Rs.{item.total_price:.0f}")
            print(f"  {beverage.prepare(size)}")
            input("\n  Press Enter to continue...")

        return order

    def _process_payment(self, order: Order) -> bool:
        print(order)
        if len(order) == 0:
            print("\nCart is empty!")
            return False

        print("\nPayment Method:")
        print("  [1] Cash")
        print("  [2] UPI / Card")
        choice = self._get_int("  → ", 1, 2)
        method = "Cash" if choice == 1 else "UPI/Card"

        print(f"\n  Processing {method} payment of Rs.{order.grand_total:.0f}...")
        order.pay()
        print(" Payment Successful! Enjoy your coffee!")
        return True

    def _show_history(self):
        if not self._order_history:
            print("\n  No orders yet.")
        else:
            for o in self._order_history:
                print(o)
        input("\n  Press Enter to go back...")

    def run(self):
        while True:
            self._clear()
            print(f"\n{'═'*40}")
            print(f"{self._shop_name.upper()}")
            print(f"{'═'*40}")
            print("  [1] New Order")
            print("  [2] Order History")
            print("  [3] Exit")
            print(f"{'═'*40}")

            choice = self._get_int("  → ", 1, 3)

            if choice == 1:
                name  = input("\n  Enter your name: ").strip() or "Guest"
                order = self._take_order(name)
                if len(order) > 0:
                    paid  = self._process_payment(order)
                    if paid:
                        self._order_history.append(order)
                input("\n  Press Enter to continue...")

            elif choice == 2:
                self._clear()
                print(f"\nOrder History ({Order.total_orders_placed()} total orders)")
                self._show_history()

            else:
                print("\n  Thanks for visiting!  See you soon!\n")
                break

if __name__ == "__main__":
    shop = CoffeeShop("Baddie's Coffee")
    shop.run()
