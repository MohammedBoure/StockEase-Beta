# StockEase-Beta

**StockEase-Beta** is an inventory management application built using **Flet**, designed to provide a seamless and efficient user experience.

---

## 🚀 Features
- **Integrated Dashboard** for displaying inventory statistics.
- **Product Management**: Easily add, edit, and delete products.
- **Order Management**: Track and manage orders efficiently.
- **Customer Management**: Add and update customer information.
- **Integrated Database System** for secure data storage.
- **Encryption System** to protect sensitive data.

---

## 📂 Project Structure 1.0
```plaintext
StockEase-Beta/
│── StockEase/                      # Main folder for the Flet application, containing all project files
│   ├── main.py                     # Main file to run the project and manage navigation between interfaces
│   ├── ui/                         # Folder for frontend UI components
│   │   ├── dashboard.py            # Dashboard - the main entry point of the application, containing links to various interfaces
│   │   ├── products_screen.py      # Products screen, allows adding, deleting, updating, and searching for products
│   │   ├── orders_screen.py        # Orders screen, displays current orders and enables their management
│   │   ├── customers_screen.py     # Customers screen, enables management of customer data
│   │   ├── components.py           # Reusable UI components used across different screens
│   │   └── __init__.py             # Defines the folder as a Python module to enable imports between files
│   ├── logic/                      # Folder containing the project's business logic
│   │   ├── inventory_manager.py    # Manages inventory operations such as adding, deleting, and updating
│   │   ├── orders_manager.py       # Manages order operations, such as creating and deleting orders
│   │   ├── users_manager.py        # Manages user and customer data
│   │   └── __init__.py             # Defines the folder as a Python module to enable imports between files
│   ├── database/                   # Folder for database interactions
│   │   ├── db_helper.py            # Helper functions for connecting to the database and executing queries
│   │   ├── models.py               # Defines database tables and entities
│   │   └── __init__.py             # Defines the folder as a Python module to enable imports between files
│   ├── storage/                    # Folder for storing application data and databases
│   │   ├── products.db             # Database for products and their details
│   │   ├── orders.db               # Database for orders and their data
│   │   ├── customers.db            # Database for customers and their information
│   │   ├── backups/                # Folder dedicated to storing database backups
│   ├── config/                     # Folder containing application configuration files
│   │   ├── keys.json               # Stores hashed interface keys for secure access
│   │   ├── themes.json             # Stores theme settings for the application interface
│   ├── utils/                      # Folder containing helper functions used across the project
│   │   ├── shared.py               # Contains global variables used throughout the project
│   │   ├── encryption.py           # Functions for encryption and securing sensitive data
│   │   └── file_utils.py           # Functions for handling file operations like reading and writing
│── requirements.txt                # List of required libraries to run the project
└── README.md                       # Project documentation file
```