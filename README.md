# StockEase-Beta

**StockEase-Beta** is an inventory management application built using **Flet**, designed to provide a seamless and efficient user experience for managing products, orders, and customers.

---

## 🚀 Features
- **Integrated Dashboard**: Displays key inventory statistics and provides navigation to core functionalities.
- **Product Management**: Add, edit, delete, and search products with ease.
- **Order Management**: Track and manage orders efficiently.
- **Customer Management**: Manage customer data, including adding and updating information.
- **Database Integration**: Supports both local SQLite databases and MySQL for secure data storage.
- **Encryption System**: Protects sensitive data with encryption utilities.
- **Customizable Settings**: Configure themes, fonts, and language preferences.
- **Backup Support**: Maintains database backups for data safety.

---

## 📂 Project Structure
```plaintext
StockEase-Beta/
├── config/                         # Configuration files for the application
│   ├── font_sizes.json            # Font size settings for UI customization
│   ├── keys.json                  # Hashed keys for secure interface access
│   ├── language.json              # Language settings for localization
│   ├── settings.json              # General application settings
│   └── themes.json                # Theme settings for the application UI
├── database/                      # Database interaction and schema definitions
│   ├── orders.py                  # Logic for handling orders in SQLite
│   ├── orders_mysql.py            # Logic for handling orders in MySQL
│   ├── products.py                # Logic for handling products in SQLite
│   ├── products_mysql.py          # Logic for handling products in MySQL
├── storage/                       # Storage for database files
│   ├── orders.db                  # SQLite database for orders
│   ├── products.db                # SQLite database for products
├── ui/                            # Frontend UI components
│   ├── customers/                 # Customer management UI
│   │   ├── customers_screen.py    # Screen for managing customer data
│   │   └── functions.py           # Helper functions for customer UI
│   ├── dashboard/                 # Dashboard UI
│   │   ├── dashboard.py           # Main dashboard interface
│   │   └── functions.py           # Helper functions for dashboard
│   ├── orders/                    # Orders management UI
│   │   └── orders_screen.py       # Screen for managing orders
│   ├── product/                   # Product management UI
│   │   └── product_screen.py      # Screen for managing products
│   ├── settings/                  # Settings UI
│   │   └── settings_screen.py     # Screen for application settings
│   ├── statistics/                # Statistics UI components
│   │   └── components.py          # Reusable UI components for statistics
├── utils/                         # Utility functions used across the project
│   ├── file_utils.py              # Functions for file operations (reading/writing)
│   └── shared.py                  # Global variables and shared utilities
├── README.md                      # Project documentation
├── commit_msg                     # File for storing commit messages
├── commit_msgs                    # File for storing multiple commit messages
├── git_push.sh                    # Shell script for automating Git push
└── main.py                        # Main entry point for running the application
```

---

## 📊 Project Statistics
- **Total Folders**: 11
- **Total Files**: 21
- **Total Lines**: 2,584
- **Total Size**: 117.0 KB
- **File Types**:
  - `.py`: 15 files (2,532 lines, 113.2 KB)
  - `.md`: 1 file (52 lines, 3.8 KB)
  - Others: `.json`, `.db`, `.sh`

---

## 🛠️ Requirements
To run the project, install the required dependencies listed in `requirements.txt` using:
```bash
pip install -r requirements.txt
```

---

## 🚀 Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/username/StockEase-Beta.git
   ```
2. Navigate to the project directory:
   ```bash
   cd StockEase-Beta
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

---

## 📝 Notes
- The application supports both SQLite and MySQL databases. Configure the appropriate database settings in the `config/` folder.
- Ensure that you have the necessary permissions to access the database files in the `storage/` folder.
- For UI customization, modify `themes.json`, `font_sizes.json`, or `language.json` in the `config/` folder.