# terminal-coffee-shop
>A terminal-based Coffee Shop ordering system built with Python — featuring OOP concepts like abstract classes, inheritance, polymorphism, enums & dataclasses. No frameworks, just clean Python!


---

## 🌸 Features
- ☕ **Hot, Cold & Blended** coffee menu
- 📏 **Size selection** — Small, Medium, Large
- 🧪 **Add-ons** — Extra Shot, Oat Milk, Whipped Cream, Syrups
- 🧾 **Auto bill generation** with 5% tax
- 💳 **Payment** — Cash or UPI/Card
- 📋 **Order History** tracking
- 🖥️ **Clean terminal UI**

---

## 📁 Project Structure
```
terminal-coffee-shop/
└── coffee_shop.py    
```

---

## 🚀 How to Run
```bash
python coffee_shop.py
```
No installation needed — just Python 3.10+!

---

## 🛠️ OOP Concepts Covered

| Concept | Where |
|---------|-------|
| Abstract Class | `BaseBeverage` with `@abstractmethod` |
| Inheritance | `HotCoffee`, `ColdCoffee`, `BlendedCoffee` |
| Polymorphism | `prepare()` & `get_price()` per type |
| Encapsulation | Private `_name`, `_price`, `_items` |
| Enums | `Size`, `CoffeeType`, `AddOn` |
| Dataclass | `OrderItem` |
| Class Variable | `Order._order_counter` |
| Class Method | `Order.total_orders_placed()` |
| Static Method | `Order.format_price()` |
| Magic Methods | `__str__`, `__repr__`, `__len__` |

---

## 🧾 Sample Output
```
════════════════════════════════════════
  ORDER #1  |  Pooja
────────────────────────────────────────
  • Cappuccino (Large)
    Add-ons : Extra Shot, Oat Milk
    Price   : Rs.316
────────────────────────────────────────
  Subtotal : Rs.316
  Tax (5%) : Rs.16
  TOTAL    : Rs.332
  Status   : Paid
════════════════════════════════════════
```

---

## ☕ Menu Preview
| # | Coffee | Type | Base Price |
|---|--------|------|-----------|
| 1 | Espresso | ☕ Hot | Rs.150 |
| 2 | Cappuccino | ☕ Hot | Rs.200 |
| 3 | Latte | ☕ Hot | Rs.220 |
| 4 | Iced Latte | 🧊 Cold | Rs.230 |
| 5 | Frappuccino | 🥤 Blended | Rs.280 |

---

Made with ☕ and lots of Python 🐍# terminal-coffee-shop
