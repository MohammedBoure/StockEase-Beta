"# StockEase-Beta" 


inventory_management_flet/
│── flet_app/                    # المجلد الرئيسي لتطبيق Flet
│   ├── main.py                   # نقطة البداية للتطبيق
│   ├── ui/                        # مكونات الواجهة الأمامية
│   │   ├── dashboard.py           # لوحة التحكم
│   │   ├── products_screen.py      # شاشة المنتجات
│   │   ├── orders_screen.py        # شاشة الطلبات
│   │   ├── customers_screen.py     # شاشة العملاء
│   │   └── components.py          # مكونات UI قابلة لإعادة الاستخدام
│   ├── logic/                     # منطق الأعمال
│   │   ├── inventory_manager.py    # إدارة المخزون
│   │   ├── orders_manager.py       # إدارة الطلبات
│   │   ├── users_manager.py        # إدارة المستخدمين
│   ├── database/                   # قاعدة البيانات
│   │   ├── db_helper.py            # وظائف الاتصال بقاعدة البيانات
│   │   ├── models.py               # تعريف الجداول
│   ├── utils/                      # أدوات مساعدة
│   │   ├── encryption.py           # التشفير
│   │   ├── helpers.py              # وظائف مساعدة عامة
│── tests/                           # اختبارات المشروع
│   ├── test_inventory.py           # اختبارات المخزون
│   ├── test_orders.py              # اختبارات الطلبات
│── .gitignore                       # استبعاد الملفات غير المطلوبة في Git
│── requirements.txt                 # المكتبات المطلوبة
│── README.md                        # توثيق المشروع




الفروع

main                    # الفرع الرئيسي (يحوي النسخة المستقرة)
│── ui-development      # تطوير الواجهة الأمامية
│── business-logic      # تطوير منطق الأعمال
│── database-integration # التكامل مع قاعدة البيانات





