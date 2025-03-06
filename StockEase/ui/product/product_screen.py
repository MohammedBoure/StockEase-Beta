import flet as ft
from utils.shared import theme, font_size, language
from database.products import ProductDatabase
# from database.products_mysql import ProductDatabase
import random

class ProductScreenView(ft.View):
    """
    ENGLISH: A view class for managing and displaying product-related operations.
    This class handles the UI and logic for adding, updating, deleting, and searching products.
    It also manages the display of product data in a table with pagination and sorting.

    ARABIC: فئة عرض لإدارة وعرض العمليات المتعلقة بالمنتجات.
    تتعامل هذه الفئة مع واجهة المستخدم والمنطق لإضافة المنتجات وتحديثها وحذفها والبحث عنها.
    كما تدير عرض بيانات المنتجات في جدول مع التقسيم الصفحات والفرز.
    """
    def __init__(self, page: ft.Page):
        """
        ENGLISH: Initializes the ProductScreenView with the necessary UI components and data.
        Sets up the layout, buttons, search field, and data table.
        Also initializes modal dialogs for adding, updating, and deleting products.

        ARABIC: يقوم بتهيئة ProductScreenView بالمكونات اللازمة لواجهة المستخدم والبيانات.
        يُنشئ التخطيط والأزرار وحقل البحث وجدول البيانات.
        كما يُهيئ حوارات النماذج المودالية لإضافة المنتجات وتحديثها وحذفها.
        """
        super().__init__(route="/product_screen")
        self.page = page
        self.lng = language["product"]  # ENGLISH: Loads language settings for localization | ARABIC: يحمل إعدادات اللغة للتوطين
        self.db_products = ProductDatabase()  # ENGLISH: Initializes the product database connection | ARABIC: يُهيئ الاتصال بقاعدة بيانات المنتجات
        self.data = self.db_products.get_all_products()  # ENGLISH: Fetches all products from the database | ARABIC: يجلب جميع المنتجات من قاعدة البيانات
        self.batch_size = 20  # ENGLISH: Sets the number of items to load per batch for pagination | ARABIC: يحدد عدد العناصر المطلوب تحميلها لكل دفعة في التقسيم الصفحات
        self.current_index = 0  # ENGLISH: Tracks the current index for pagination | ARABIC: يتتبع المؤشر الحالي للتقسيم الصفحات
        self.list_selected = []  # ENGLISH: Stores selected products for operations like update/delete | ARABIC: يخزن المنتجات المحددة لعمليات مثل التحديث/الحذف
        self.status = True  # ENGLISH: Tracks the sorting direction (ascending/descending) | ARABIC: يتتبع اتجاه الفرز (تصاعدي/تنازلي)

        # ENGLISH: Search field for filtering products by ID or name
        # ARABIC: حقل البحث لتصفية المنتجات حسب المعرف أو الاسم
        self.search_field = ft.TextField(
            label=self.lng["left_container"]["search_label"],
            text_size=font_size["input"],
            border=ft.InputBorder.OUTLINE,
            border_radius=8,
            text_align=ft.TextAlign.CENTER,
            filled=True,
            hint_text="ID or Product",
            width=250,
            color=theme["text_color"],
            border_color=theme["input_border_color"],
            fill_color=theme["input_fill_color"],
            hover_color=theme["input_hover_color"],
            cursor_color=theme["input_cursor_color"],
            selection_color=theme["input_selection_color"],
            focused_border_color=theme["input_focused_border_color"],
        )
        self.search_text = ft.Row(
            controls=[self.search_field],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.search_label = ft.Column(
            controls=[
                self.search_text,
                ft.Row(
                    controls=[self.make_button(self.lng["left_container"]["Search"], self.search, width=250, height=50)],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # ENGLISH: Left container with buttons for product operations (add, edit, delete, etc.)
        # ARABIC: الحاوية اليسرى تحتوي على أزرار لعمليات المنتجات (إضافة، تعديل، حذف، إلخ)
        self.left_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Divider(height=1, color=theme["border_color"]),
                    self.search_label,
                    ft.Divider(height=1, color=theme["border_color"]),
                    self.make_button(self.lng["left_container"]["Add_Product"]["Add_Product"],
                                     lambda e: self.open_dlg_add(e),
                                     width=250,
                                     height=50,
                                     icon=ft.Icons.ADD_CIRCLE_OUTLINED
                                     ),
                    self.make_button(self.lng["left_container"]["Edit_Product"]["Edit_Product"],
                                     lambda e: self.open_dlg_update(e),
                                     width=250,
                                     height=50,
                                     icon=ft.Icons.EDIT
                                     ),
                    self.make_button(self.lng["left_container"]["Delete_Product"]["Delete_Product"],
                                     lambda e: self.open_dlg_delete(e),
                                     width=250,
                                     height=50,
                                     icon=ft.Icons.DELETE
                                     ),
                    ft.Divider(height=1, color=theme["border_color"]),
                    self.make_button(self.lng["left_container"]["Out_of_stock_products"],
                                     lambda e: self.Out_of_stock_products(e),
                                     width=250,
                                     height=50,
                                     icon=ft.Icons.SHOPPING_BASKET_OUTLINED
                                     ),
                ],
                horizontal_alignment="center",
            ),
            width=300,
            padding=20,
            bgcolor=theme["container_bg_colors"],
            border_radius=ft.border_radius.all(theme["container_border_radius"]),
            border=ft.border.all(width=1, color=theme["container_border_color"]),
        )

        # ENGLISH: Top container with navigation buttons to other screens
        # ARABIC: الحاوية العلوية تحتوي على أزرار التنقل إلى شاشات أخرى
        self.top_container = ft.Container(
            content=ft.Row(
                controls=[
                    self.make_button(self.lng["top_container"]["Product"], lambda e: self.reset_table(), width=150, height=70),
                    self.make_button(self.lng["top_container"]["Orders"], lambda e: self.page.go("/orders_screen"), width=150, height=70),
                    self.make_button(self.lng["top_container"]["Customers"], lambda e: self.page.go("/customers_screen"), width=150, height=70),
                    self.make_button(self.lng["top_container"]["Dashboard"], lambda e: self.page.go("/"), width=150, height=70),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=10,
            bgcolor=theme["container_bg_colors"],
            border_radius=ft.border_radius.all(theme["container_border_radius"]),
            border=ft.border.all(width=1, color=theme["container_border_color"]),
        )

        # ENGLISH: Data table to display product details with sortable columns
        # ARABIC: جدول بيانات لعرض تفاصيل المنتجات مع أعمدة قابلة للفرز
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Checkbox(on_change=self.select_all_rows)),  # ENGLISH: Checkbox for selecting all rows | ARABIC: مربع اختيار لتحديد جميع الصفوف
                ft.DataColumn(self.button("ID", lambda e: self.on_click_id_btn(e, 0))),
                ft.DataColumn(self.button(self.lng["table"]["Name"], lambda e: self.on_click_id_btn(e, 1))),
                ft.DataColumn(self.button(self.lng["table"]["recommended_quantity"], lambda e: self.on_click_id_btn(e, 2))),
                ft.DataColumn(self.button(self.lng["table"]["Quantity"], lambda e: self.on_click_id_btn(e, 3))),
                ft.DataColumn(self.button(self.lng["table"]["Price"], lambda e: self.on_click_id_btn(e, 4))),
                ft.DataColumn(self.button(self.lng["table"]["Price_Per_Item"], lambda e: self.on_click_id_btn(e, 5))),
            ],
            rows=[],
        )

        # ENGLISH: List view to enable scrolling for the data table
        # ARABIC: عرض قائمة لتمكين التمرير لجدول البيانات
        self.list_view = ft.ListView(
            controls=[self.table],
            expand=True,
            spacing=10,
            auto_scroll=False,
            on_scroll=lambda e: self.handle_scroll(e),
        )

        # ENGLISH: Main content container with a decorative icon and the product list
        # ARABIC: حاوية المحتوى الرئيسية تحتوي على أيقونة زخرفية وقائمة المنتجات
        self.main_content_container = ft.Container(
            content=ft.Stack(
                [
                    ft.Container(
                        content=ft.Icon(name=ft.Icons.SHOPIFY_ROUNDED, size=600, opacity=0.3, color="grey"),
                        alignment=ft.alignment.center,
                    ),
                    self.list_view,
                ]
            ),
            padding=20,
            bgcolor=theme["container_bg_colors"],
            border_radius=ft.border_radius.all(theme["container_border_radius"]),
            border=ft.border.all(width=1, color=theme["container_border_color"]),
            expand=True,
        )

        # ENGLISH: Vertical layout combining the top and main content containers
        # ARABIC: تخطيط عمودي يجمع بين الحاوية العلوية وحاوية المحتوى الرئيسية
        self.vertical_containers = ft.Column(
            controls=[
                self.top_container,
                self.main_content_container
            ],
            expand=True,
        )

        # ENGLISH: Main layout combining the left and vertical containers side by side
        # ARABIC: التخطيط الرئيسي يجمع بين الحاوية اليسرى والحاويات العمودية جنبًا إلى جنب
        self.main_layout = ft.Row(
            controls=[
                self.left_container,
                self.vertical_containers
            ],
            expand=True,
            spacing=20,
        )

        # ENGLISH: Main container wrapping the entire layout with consistent styling
        # ARABIC: الحاوية الرئيسية تغلف التخطيط بأكمله مع تنسيق متسق
        self.main_container = ft.Container(
            content=self.main_layout,
            expand=True,
            padding=20,
            bgcolor=theme["background_colors"],
        )

        self.controls.append(
            ft.Container(
                content=self.main_container,
                expand=True,
                alignment=ft.alignment.center
            )
        )

        # ENGLISH: Initialize modal dialogs for add, update, and delete operations
        # ARABIC: تهيئة حوارات النماذج المودالية لعمليات الإضافة والتحديث والحذف
        self.dlg_modal_add = self.create_modal_dialog_add()
        self.dlg_modal_update = self.create_modal_dialog_update()
        self.dlg_modal_delete = self.create_modal_dialog_delete()
        self.load_more_data(None)  # ENGLISH: Load initial batch of product data | ARABIC: تحميل الدفعة الأولية من بيانات المنتجات

    # --- Delete Dialog Methods ---
    def close_dlg_delete(self, e, status):
        """
        ENGLISH: Closes the delete confirmation dialog and performs the deletion if confirmed.
        Deletes selected products from the database and updates the product list.

        ARABIC: يغلق حوار تأكيد الحذف وينفذ الحذف إذا تم التأكيد.
        يحذف المنتجات المحددة من قاعدة البيانات ويحدث قائمة المنتجات.
        """
        if status == True:
            for i in self.list_selected:
                self.db_products.delete_product(i[0])  # ENGLISH: Delete product by ID | ARABIC: حذف المنتج حسب المعرف
            self.list_selected = []  # ENGLISH: Clear selected items after deletion | ARABIC: مسح العناصر المحددة بعد الحذف
            self.data = self.db_products.get_all_products()  # ENGLISH: Refresh product data | ARABIC: تحديث بيانات المنتجات

        self.refresh_products()  # ENGLISH: Refresh the UI with updated data | ARABIC: تحديث واجهة المستخدم بالبيانات المحدثة
        self.dlg_modal_delete.open = False
        e.page.update()

    def open_dlg_delete(self, e):
        """
        ENGLISH: Opens the delete confirmation dialog.
        Ensures the dialog is added to the page overlay if not already present.

        ARABIC: يفتح حوار تأكيد الحذف.
        يضمن إضافة الحوار إلى طبقة التراكب في الصفحة إذا لم يكن موجودًا بالفعل.
        """
        try:
            if self.dlg_modal_delete not in e.control.page.overlay:
                e.control.page.overlay.append(self.dlg_modal_delete)
                e.control.page.update()
            self.dlg_modal_delete.open = True
            e.control.page.update()
        except Exception as ex:
            print(f"Exception: {ex}")

    def create_modal_dialog_delete(self):
        """
        ENGLISH: Creates and returns a modal dialog for confirming product deletion.
        The dialog includes 'Yes' and 'No' buttons to confirm or cancel the deletion.

        ARABIC: ينشئ ويعيد حوارًا موداليًا لتأكيد حذف المنتج.
        يتضمن الحوار أزرار "نعم" و"لا" لتأكيد الحذف أو إلغائه.
        """
        return ft.AlertDialog(
            modal=True,
            title=ft.Text(self.lng["left_container"]["Delete_Product"]["Confirm"], size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            content=ft.Container(
                content=ft.Text(self.lng["left_container"]["Delete_Product"]["comment"], text_align=ft.TextAlign.CENTER),
                alignment=ft.alignment.center,
                padding=ft.padding.all(10),
                height=50,
            ),
            actions=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        self.make_button(text=self.lng["left_container"]["Delete_Product"]["Yes"], on_click=lambda _: self.close_dlg_delete(_, True), width=100, height=40),
                        self.make_button(text=self.lng["left_container"]["Delete_Product"]["No"], on_click=lambda _: self.close_dlg_delete(_, False), width=100, height=40),
                    ],
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

    # --- Update Dialog Methods ---
    def close_dlg_update(self, e):
        """
        ENGLISH: Closes the update product dialog and refreshes the product list.

        ARABIC: يغلق حوار تحديث المنتج ويعيد تحديث قائمة المنتجات.
        """
        self.refresh_products()
        self.dlg_modal_update.open = False
        e.page.update()

    def dlg_update(self, e, name, recommended_quantity, current_quantity, price, purchase_price):
        """
        ENGLISH: Handles the logic for updating a product in the database.
        Validates the input and updates the product details if the input is valid.
        Refreshes the product list after the update.

        ARABIC: يتعامل مع منطق تحديث منتج في قاعدة البيانات.
        يتحقق من صحة الإدخال ويحدث تفاصيل المنتج إذا كان الإدخال صالحًا.
        يعيد تحديث قائمة المنتجات بعد التحديث.
        """
        if len(self.list_selected) != 1:
            self.text_invailed.value = self.lng["left_container"]["Edit_Product"]["invailed_text"]
            self.text_invailed.update()
            return
        try:
            self.db_products.update_product(
                self.list_selected[0][0], name, int(recommended_quantity), int(current_quantity), float(price), float(purchase_price)
            )
        except:
            self.text_invailed.value = self.lng["left_container"]["Edit_Product"]["invailed_text"]
            self.text_invailed.update()
            return

        for i in range(len(self.data)):
            if self.data[i][0] == self.list_selected[0][0]:
                self.data[i] = (self.list_selected[0][0], name, int(recommended_quantity), int(current_quantity), float(price), float(purchase_price))

        # ENGLISH: Clear input fields after successful update
        # ARABIC: مسح حقول الإدخال بعد التحديث الناجح
        self.name_field.value = ""
        self.name_field.update()
        self.recommended_quantity_field.value = ""
        self.recommended_quantity_field.update()
        self.current_quantity_field.value = ""
        self.current_quantity_field.update()
        self.price_field.value = ""
        self.price_field.update()
        self.purchase_price_field.value = ""
        self.purchase_price_field.update()

        self.refresh_products()
        self.dlg_modal_update.open = False
        e.page.update()

    def open_dlg_update(self, e):
        """
        ENGLISH: Opens the update product dialog and pre-fills the form with the selected product's details.
        Ensures the dialog is added to the page overlay if not already present.

        ARABIC: يفتح حوار تحديث المنتج ويملأ النموذج مسبقًا بتفاصيل المنتج المحدد.
        يضمن إضافة الحوار إلى طبقة التراكب في الصفحة إذا لم يكن موجودًا بالفعل.
        """
        if len(self.list_selected) == 1:
            self.name_field.value = self.list_selected[0][1]
            self.recommended_quantity_field.value = self.list_selected[0][2]
            self.current_quantity_field.value = self.list_selected[0][3]
            self.price_field.value = self.list_selected[0][4]
            self.purchase_price_field.value = self.list_selected[0][5]
        try:
            if self.dlg_modal_update not in e.control.page.overlay:
                e.control.page.overlay.append(self.dlg_modal_update)
                e.control.page.update()
            self.dlg_modal_update.open = True
            e.control.page.update()
        except Exception as ex:
            print(f"Exception: {ex}")

    def create_modal_dialog_update(self):
        """
        ENGLISH: Creates and returns a modal dialog for updating product details.
        The dialog includes input fields for product name, quantities, price, and purchase price.

        ARABIC: ينشئ ويعيد حوارًا موداليًا لتحديث تفاصيل المنتج.
        يتضمن الحوار حقول إدخال لاسم المنتج والكميات والسعر وسعر الشراء.
        """
        def Text(lbl, y, hint):
            return ft.TextField(
                hint_text=lbl,
                text_size=font_size["input"],
                border=ft.InputBorder.OUTLINE,
                border_radius=8,
                text_align=ft.TextAlign.CENTER,
                filled=True,
                width=y,
                color=theme["text_color"],
                border_color=theme["input_border_color"],
                fill_color=theme["input_fill_color"],
                hover_color=theme["input_hover_color"],
                cursor_color=theme["input_cursor_color"],
                selection_color=theme["input_selection_color"],
                focused_border_color=theme["input_focused_border_color"],
            )

        # ENGLISH: Input fields for updating product details
        # ARABIC: حقول الإدخال لتحديث تفاصيل المنتج
        self.name_field = Text(lbl=self.lng["left_container"]["Edit_Product"]["Name"], y=300, hint="string")
        self.recommended_quantity_field = Text(lbl=self.lng["left_container"]["Edit_Product"]["Recommended_quantity"], y=300, hint="integer")
        self.current_quantity_field = Text(lbl=self.lng["left_container"]["Edit_Product"]["Current_quantity"], y=300, hint="integer")
        self.price_field = Text(lbl=self.lng["left_container"]["Edit_Product"]["price"], y=300, hint="real")
        self.purchase_price_field = Text(lbl=self.lng["left_container"]["Edit_Product"]["Purchase_price"], y=300, hint="real")
        self.text_invailed = ft.Text("", color="red")  # ENGLISH: Error message display | ARABIC: عرض رسالة الخطأ

        dialog = ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(self.lng["left_container"]["Edit_Product"]["Edit_Product"], size=20, weight=ft.FontWeight.BOLD),
                        ft.IconButton(ft.Icons.CLOSE, on_click=lambda e: self.close_dlg_update(e)),
                    ],
                ),
                ft.Divider(),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            spacing=10,
                            controls=[
                                self.name_field,
                                self.recommended_quantity_field,
                                self.current_quantity_field,
                                self.price_field,
                                self.purchase_price_field,
                            ],
                        )
                    ],
                ),
                ft.Divider(),
                ft.Container(
                    content=self.text_invailed,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            self.make_button(text=self.lng["left_container"]["Edit_Product"]["updating_data"], on_click=lambda e: self.dlg_update(
                                e, self.name_field.value, self.recommended_quantity_field.value, self.current_quantity_field.value,
                                self.price_field.value, self.purchase_price_field.value), width=200, height=50),
                            self.make_button(text=self.lng["left_container"]["Edit_Product"]["exit"], on_click=lambda e: self.close_dlg_update(e), width=200, height=50),
                        ],
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
        )

        return ft.AlertDialog(
            content=ft.Container(
                width=500,
                height=500,
                content=dialog,
                alignment=ft.alignment.center
            ),
            bgcolor=theme["container_bg_colors"],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

    # --- Add Dialog Methods ---
    def on_click_generate_barcode(self, e):
        """
        ENGLISH: Generates a unique invalid EAN-13 barcode for a new product.
        Ensures the generated barcode does not conflict with existing barcodes in the database.
        Updates the ID field in the add product dialog with the generated barcode.

        ARABIC: يولد رمز EAN-13 غير صالح وفريد لمنتج جديد.
        يضمن أن الرمز المولد لا يتعارض مع الرموز الموجودة في قاعدة البيانات.
        يحدث حقل المعرف في حوار إضافة المنتج بالرمز المولد.
        """
        existing_barcodes = {item[0] for item in self.data}

        def calculate_ean13_check_digit(barcode: str) -> int:
            if len(barcode) != 12 or not barcode.isdigit():
                raise ValueError("number < 12")
            total = sum((3 if i % 2 else 1) * int(digit) for i, digit in enumerate(barcode))
            check_digit = (10 - (total % 10)) % 10
            return check_digit

        def generate_unique_invalid_ean13(existing_barcodes):
            while True:
                base_barcode = str(random.randint(10**11, 10**12 - 1))
                correct_check_digit = calculate_ean13_check_digit(base_barcode)
                invalid_check_digit = (correct_check_digit + random.randint(1, 8)) % 10
                full_barcode = base_barcode + str(invalid_check_digit)
                if full_barcode not in existing_barcodes:
                    existing_barcodes.add(full_barcode)
                    return full_barcode

        number_generate = generate_unique_invalid_ean13(existing_barcodes)
        self.id_field_add.value = number_generate
        self.id_field_add.update()

    def close_dlg_add(self, e):
        """
        ENGLISH: Closes the add product dialog and refreshes the product list.

        ARABIC: يغلق حوار إضافة المنتج ويعيد تحديث قائمة المنتجات.
        """
        self.refresh_products()
        self.dlg_modal_add.open = False
        e.page.update()

    def dlg_add(self, e, id, name, recommended_quantity, current_quantity, price, purchase_price):
        """
        ENGLISH: Handles the logic for adding a new product to the database.
        Validates the input and adds the product if the input is valid.
        Updates the product list after the addition.

        ARABIC: يتعامل مع منطق إضافة منتج جديد إلى قاعدة البيانات.
        يتحقق من صحة الإدخال ويضيف المنتج إذا كان الإدخال صالحًا.
        يحدث قائمة المنتجات بعد الإضافة.
        """
        try:
            self.db_products.add_product(int(id), name, int(recommended_quantity), int(current_quantity), float(price), float(purchase_price))
            self.data.append((int(id), name, int(recommended_quantity), int(current_quantity), float(price), float(purchase_price)))
        except:
            return

        # ENGLISH: Clear input fields after successful addition
        # ARABIC: مسح حقول الإدخال بعد الإضافة الناجحة
        self.id_field_add.value = ""
        self.id_field_add.update()
        self.name_field_add.value = ""
        self.name_field_add.update()
        self.recommended_quantity_field_add.value = ""
        self.recommended_quantity_field_add.update()
        self.current_quantity_field_add.value = ""
        self.current_quantity_field_add.update()
        self.price_field_add.value = ""
        self.price_field_add.update()
        self.purchase_price_field_add.value = ""
        self.purchase_price_field_add.update()

    def open_dlg_add(self, e):
        """
        ENGLISH: Opens the add product dialog and ensures it is added to the page overlay if not already present.

        ARABIC: يفتح حوار إضافة المنتج ويضمن إضافته إلى طبقة التراكب في الصفحة إذا لم يكن موجودًا بالفعل.
        """
        try:
            if self.dlg_modal_add not in e.control.page.overlay:
                e.control.page.overlay.append(self.dlg_modal_add)
                e.control.page.update()
            self.dlg_modal_add.open = True
            e.control.page.update()
        except Exception as ex:
            print(f"Exception: {ex}")

    def create_modal_dialog_add(self):
        """
        ENGLISH: Creates and returns a modal dialog for adding a new product.
        The dialog includes input fields for product ID, name, quantities, price, and purchase price.
        Also includes a button to generate a unique barcode for the product.

        ARABIC: ينشئ ويعيد حوارًا موداليًا لإضافة منتج جديد.
        يتضمن الحوار حقول إدخال لمعرف المنتج والاسم والكميات والسعر وسعر الشراء.
        يتضمن أيضًا زرًا لتوليد رمز شريطي فريد للمنتج.
        """
        def Text(lbl, y, hint):
            return ft.TextField(
                hint_text=lbl,
                text_size=font_size["input"],
                border=ft.InputBorder.OUTLINE,
                border_radius=8,
                text_align=ft.TextAlign.CENTER,
                filled=True,
                width=y,
                color=theme["text_color"],
                border_color=theme["input_border_color"],
                fill_color=theme["input_fill_color"],
                hover_color=theme["input_hover_color"],
                cursor_color=theme["input_cursor_color"],
                selection_color=theme["input_selection_color"],
                focused_border_color=theme["input_focused_border_color"],
            )

        # ENGLISH: Input fields for adding a new product
        # ARABIC: حقول الإدخال لإضافة منتج جديد
        self.id_field_add = Text(lbl="ID", y=250, hint="#############")
        self.name_field_add = Text(lbl=self.lng["left_container"]["Add_Product"]["Name"], y=300, hint="string")
        self.recommended_quantity_field_add = Text(lbl=self.lng["left_container"]["Add_Product"]["Recommended_quantity"], y=300, hint="integer")
        self.current_quantity_field_add = Text(lbl=self.lng["left_container"]["Add_Product"]["Current_quantity"], y=300, hint="integer")
        self.price_field_add = Text(lbl=self.lng["left_container"]["Add_Product"]["price"], y=300, hint="Real")
        self.purchase_price_field_add = Text(lbl=self.lng["left_container"]["Add_Product"]["Purchase_price"], y=300, hint="real")

        dialog = ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(self.lng["left_container"]["Add_Product"]["Add_Product"], size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.IconButton(ft.Icons.CLOSE, on_click=lambda e: self.close_dlg_add(e)),
                    ],
                ),
                ft.Divider(),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            spacing=10,
                            controls=[
                                ft.Row(controls=[
                                    self.id_field_add,
                                    ft.IconButton(icon=ft.Icons.QR_CODE_2, on_click=lambda e: self.on_click_generate_barcode(e),
                                                  style=ft.ButtonStyle(
                                                      shape=ft.RoundedRectangleBorder(radius=theme["icon_button_border_radius"]),
                                                      overlay_color=theme["icon_button_overlay_color"],
                                                      icon_color=theme["icon_button_icon_color"],
                                                  ),
                                                  ),
                                ]),
                                self.name_field_add,
                                self.recommended_quantity_field_add,
                                self.current_quantity_field_add,
                                self.price_field_add,
                                self.purchase_price_field_add,
                            ],
                        )
                    ],
                ),
                ft.Divider(),
                ft.Container(
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            self.make_button(text=self.lng["left_container"]["Add_Product"]["inserting_data"], on_click=lambda e: self.dlg_add(
                                e, self.id_field_add.value, self.name_field_add.value, self.recommended_quantity_field_add.value,
                                self.current_quantity_field_add.value, self.price_field_add.value, self.purchase_price_field_add.value), width=200, height=50),
                            self.make_button(text=self.lng["left_container"]["Add_Product"]["exit"], on_click=lambda e: self.close_dlg_add(e), width=200, height=50),
                        ],
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
        )
        return ft.AlertDialog(
            content=ft.Container(
                width=500,
                height=500,
                content=dialog,
                alignment=ft.alignment.center
            ),
            bgcolor=theme["container_bg_colors"],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

    # --- General Utility Methods ---
    def handle_scroll(self, e):
        """
        ENGLISH: Handles the scroll event for the product list.
        Loads more data when the user scrolls near the bottom of the list.

        ARABIC: يتعامل مع حدث التمرير لقائمة المنتجات.
        يحمل المزيد من البيانات عندما يقترب المستخدم من أسفل القائمة.
        """
        if e.pixels >= e.max_scroll_extent * 0.9:
            self.load_more_data(None)

    def make_button(self, text, on_click, width, height, icon=None):
        """
        ENGLISH: Creates and returns a styled button with the specified text, click handler, width, height, and optional icon.
        Applies consistent styling from the theme configuration.

        ARABIC: ينشئ ويعيد زرًا منسقًا بالنص المحدد ومعالج النقر والعرض والارتفاع وأيقونة اختيارية.
        يطبق التنسيق المتسق من إعدادات السمة.
        """
        controls = []
        if icon:
            controls.append(ft.Icon(icon, color=theme["button_text_color"], size=25))
        controls.append(ft.Container(ft.Text(text, text_align=ft.TextAlign.CENTER), expand=True))

        return ft.ElevatedButton(
            width=width,
            height=height,
            on_click=on_click,
            bgcolor=theme["button_bg_color"],
            color=theme["button_text_color"],
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=theme["button_border_radius"]),
                overlay_color=theme["button_overlay_color"],
            ),
            content=ft.Row(
                controls=controls,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8
            )
        )

    def button(self, title, on_click):
        """
        ENGLISH: Creates and returns a text button with the specified title and click handler.
        Used for column headers in the product table.

        ARABIC: ينشئ ويعيد زر نصي بالعنوان المحدد ومعالج النقر.
        يُستخدم لرؤوس الأعمدة في جدول المنتجات.
        """
        return ft.TextButton(
            title,
            on_click=on_click,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=0),
                padding=ft.padding.all(5),
                color=theme["button_text_color"]
            )
        )

    def search(self, e):
        """
        ENGLISH: Searches for products based on the input in the search field.
        Updates the product list with the search results.

        ARABIC: يبحث عن المنتجات بناءً على الإدخال في حقل البحث.
        يحدث قائمة المنتجات بنتائج البحث.
        """
        self.data = self.db_products.search_product(self.search_field.value)
        if not self.data:
            self.table.clean()
        self.refresh_products()

    def refresh_products(self):
        """
        ENGLISH: Refreshes the product list by clearing the current data and reloading it from the database.
        Resets the selected items and the current index for pagination.

        ARABIC: يعيد تحديث قائمة المنتجات بمسح البيانات الحالية وإعادة تحميلها من قاعدة البيانات.
        يعيد تعيين العناصر المحددة والمؤشر الحالي للتقسيم الصفحات.
        """
        self.table.rows.clear()
        self.current_index = 0
        self.list_selected = []
        self.load_more_data(None)

    def reset_table(self):
        """
        ENGLISH: Resets the product table to display all products from the database.
        ARABIC: يعيد تعيين جدول المنتجات لعرض جميع المنتجات من قاعدة البيانات.
        """
        self.data = self.db_products.get_all_products()
        self.refresh_products()

    def on_change(self, e, id, name, last_quantity, quantity, price, price_per_item):
        """
        ENGLISH: Handles the change event for checkboxes in the product table.
        Updates the list of selected items based on the checkbox state.

        ARABIC: يتعامل مع حدث التغيير لمربعات الاختيار في جدول المنتجات.
        يحدث قائمة العناصر المحددة بناءً على حالة مربع الاختيار.
        """
        item = (id, name, last_quantity, quantity, price, price_per_item)
        if e.data == "true":
            if item not in self.list_selected:
                self.list_selected.append(item)
        else:
            if item in self.list_selected:
                self.list_selected.remove(item)
        print("Selected Items:", self.list_selected)

    def select_all_rows(self, e: ft.ControlEvent):
        """
        ENGLISH: Handles the select-all checkbox in the product table.
        Selects or deselects all rows based on the checkbox state.
        Updates the list of selected items accordingly.

        ARABIC: يتعامل مع مربع الاختيار "تحديد الكل" في جدول المنتجات.
        يحدد أو يلغي تحديد جميع الصفوف بناءً على حالة مربع الاختيار.
        يحدث قائمة العناصر المحددة وفقًا لذلك.
        """
        is_checked = e.control.value
        loaded_data = self.data[:self.current_index]
        if is_checked:
            for item in loaded_data:
                if item not in self.list_selected:
                    self.list_selected.append(item)
        else:
            self.list_selected = []
        print("Selected Items after select all:", self.list_selected)
        for row in self.table.rows:
            row.cells[0].content.value = is_checked
        self.page.update()

    def load_more_data(self, e):
        """
        ENGLISH: Loads more product data into the table when the user scrolls down.
        Implements pagination by loading data in batches.

        ARABIC: يحمل المزيد من بيانات المنتجات إلى الجدول عندما يقوم المستخدم بالتمرير لأسفل.
        ينفذ التقسيم الصفحات عن طريق تحميل البيانات على دفعات.
        """
        if self.current_index < len(self.data):
            next_batch = self.data[self.current_index: self.current_index + self.batch_size]
            self.current_index += self.batch_size

            for item in next_batch:
                def make_on_change(item):
                    return lambda e: self.on_change(e, item[0], item[1], item[2], item[3], item[4], item[5])

                if item[3] < item[2]:  # ENGLISH: Highlight low stock in red | ARABIC: تمييز المخزون المنخفض باللون الأحمر
                    self.table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Checkbox(on_change=make_on_change(item))),
                                ft.DataCell(ft.Text(str(item[0]), color=theme["text_color"])),
                                ft.DataCell(ft.Text(item[1], color=theme["text_color"])),
                                ft.DataCell(ft.Text("     " + str(item[2]), color=theme["text_color"])),
                                ft.DataCell(ft.Text("   " + str(item[3]), color="red")),
                                ft.DataCell(ft.Text("  " + str(item[4]), color=theme["text_color"])),
                                ft.DataCell(ft.Text("  " + str(item[5]), color=theme["text_color"])),
                            ]
                        )
                    )
                else:
                    self.table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Checkbox(on_change=make_on_change(item))),
                                ft.DataCell(ft.Text(str(item[0]), color=theme["text_color"])),
                                ft.DataCell(ft.Text(item[1], color=theme["text_color"])),
                                ft.DataCell(ft.Text("     " + str(item[2]), color=theme["text_color"])),
                                ft.DataCell(ft.Text("   " + str(item[3]), color=theme["text_color"])),
                                ft.DataCell(ft.Text("  " + str(item[4]), color=theme["text_color"])),
                                ft.DataCell(ft.Text("  " + str(item[5]), color=theme["text_color"])),
                            ]
                        )
                    )
            print(f"Loaded up to index: {self.current_index}")
            self.page.update()

    def on_click_id_btn(self, e, col_index):
        """
        ENGLISH: Handles the click event for column headers in the product table.
        Sorts the product data based on the clicked column and toggles the sort order.

        ARABIC: يتعامل مع حدث النقر لرؤوس الأعمدة في جدول المنتجات.
        يفرز بيانات المنتجات بناءً على العمود الذي تم النقر عليه ويبدل ترتيب الفرز.
        """
        self.data = sorted(self.data, key=lambda x: x[col_index], reverse=self.status)
        self.status = not self.status
        self.table.rows = []
        self.current_index = 0
        self.load_more_data(None)

    def Out_of_stock_products(self, e):
        """
        ENGLISH: Filters and displays only out-of-stock products (current quantity < recommended quantity).
        ARABIC: يقوم بتصفية وعرض المنتجات التي نفدت من المخزون فقط (الكمية الحالية < الكمية الموصى بها).
        """
        newlist = []
        for item in self.data:
            if item[3] < item[2]:
                newlist.append(item)
        self.data = newlist
        self.refresh_products()
