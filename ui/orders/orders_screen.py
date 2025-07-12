import flet as ft
from utils.shared import theme, font_size, language
from database.products import ProductDatabase
from database.orders import OrderDatabase
from ui.components import make_button,button
# from database.products_mysql import ProductDatabase
# from database.orders_mysql import OrderDatabase
import time

# English: Main class for the Orders Screen UI in the application
# Arabic: الكلاس الرئيسي لواجهة شاشة الطلبات في التطبيق
class OrdersScreen(ft.View):
    
    # English: Initialize the Orders Screen with a page object
    # Arabic: تهيئة شاشة الطلبات باستخدام كائن الصفحة
    def __init__(self, page: ft.Page):
        super().__init__(route="/orders_screen")
        self.page = page
        self.page.window.bgcolor = theme["background_colors"]
        self.lng = language["orders"]  # Language settings for orders screen / إعدادات اللغة لشاشة الطلبات
        
        #init functions 
        self.make_button = make_button
        self.button = button
        
        # English: Input field for numeric entries (e.g., quantities)
        # Arabic: حقل إدخال للقيم الرقمية (مثل الكميات)
        self.number_text = ft.TextField(
            text_size=font_size["subtitle"],
            color=theme["text_color"],
            height=70,
            border_color=theme["input_border_color"],
            fill_color=theme["input_fill_color"],
            hover_color=theme["input_hover_color"],
            cursor_color=theme["input_cursor_color"],
            selection_color=theme["input_selection_color"],
            focused_border_color=theme["input_focused_border_color"],
        )
        
        # English: Search button to open the product search dialog
        # Arabic: زر البحث لفتح نافذة البحث عن المنتجات
        self.search_button = self.make_button(text="البحث في المخزون", on_click=lambda e: self.open_dlg_search(e), width=350, height=70)
        
        # English: Search field inside the dialog for product filtering
        # Arabic: حقل البحث داخل النافذة لتصفية المنتجات
        self.search_field_dialog = ft.TextField(
            label=self.lng[ "top_container"]["search_in_stock"]["label"],
            text_size=font_size["input"],
            border=ft.InputBorder.OUTLINE,
            border_radius=8,
            text_align=ft.TextAlign.CENTER,
            filled=True,
            hint_text=self.lng[ "top_container"]["search_in_stock"]["hint_text"],
            width=350,
            color=theme["text_color"],
            border_color=theme["input_border_color"],
            fill_color=theme["input_fill_color"],
            hover_color=theme["input_hover_color"],
            cursor_color=theme["input_cursor_color"],
            selection_color=theme["input_selection_color"],
            focused_border_color=theme["input_focused_border_color"],
        )
        
        # English: Modal dialog for product search, database connections, and UI components
        # Arabic: نافذة حوارية للبحث عن المنتجات، اتصالات قاعدة البيانات، ومكونات الواجهة
        self.dlg_modal_search = self.create_modal_dialog_search()
        self.batch_size = 10  # Pagination batch size / حجم دفعة التصفح
        self.current_index = 0  # Current index for pagination / المؤشر الحالي للتصفح
        self.db_products = ProductDatabase()  # Instance for product database / مثيل لقاعدة بيانات المنتجات
        self.db_orders = OrderDatabase()  # Instance for orders database / مثيل لقاعدة بيانات الطلبات
        self.data = self.db_products.get_all_products()  # All products data / بيانات جميع المنتجات
        self.data_search = []  # Search results storage / تخزين نتائج البحث
        self.table = self.create_table()  # Main table for selected products / الجدول الرئيسي للمنتجات المختارة
        self.list_view = self.create_list_view()  # List view wrapping the table / عرض القائمة يحتوي على الجدول
        
        # English: Variables for keyboard input handling
        # Arabic: متغيرات لمعالجة إدخال لوحة المفاتيح
        self.input_keyboard = ""
        self.input_keyboard_time = time.time()
        self.last_row = None  # Last selected row in the table / آخر صف تم تحديده في الجدول
        
        # English: Price displays: red for original total, white for adjusted total
        # Arabic: عروض الأسعار: الأحمر للإجمالي الأصلي، الأبيض للإجمالي المعدل
        self.price = ft.Text("0", size=font_size["subtitle"], color=ft.colors.RED_400)
        self.sub_price = ft.Text("0", size=font_size["subtitle"], color=theme["text_color"])
        
        self.setup_keyboard_event()  # Setup keyboard event listener / إعداد مستمع أحداث لوحة المفاتيح
        self.face_focus = ft.TextButton("Hidden", visible=False)  # Hidden focus element / عنصر تركيز مخفي
        
        # English: Default button style for consistency across UI - Must be defined before create_main_layout
        # Arabic: نمط الزر الافتراضي للحفاظ على التناسق في الواجهة - يجب تعريفه قبل create_main_layout
        self.default_button_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=theme["button_border_radius"]),
            bgcolor=theme["button_bg_color"],
            color=theme["button_text_color"],
            overlay_color=theme["button_overlay_color"],
            padding=ft.padding.all(10),
        )
        
        # English: Define the main layout after all required attributes are set
        # Arabic: تعريف التخطيط الرئيسي بعد تعيين جميع السمات المطلوبة
        self.main_layout = self.create_main_layout()  # Main layout setup / إعداد التخطيط الرئيسي
        
        # English: Add main layout to the view's controls
        # Arabic: إضافة التخطيط الرئيسي إلى عناصر التحكم في العرض
        self.controls = [
            ft.Container(
                content=self.main_layout,
                expand=True,
                alignment=ft.alignment.center
            )
        ]
    
        
#-------------------------------------------search_dialog---------------------------------------------
    # English: Closes the search dialog when called
    # Arabic: يغلق نافذة البحث عند استدعائها
    def close_dlg_search(self, e=None):
        """Closes the search dialog."""
        self.dlg_modal_search.open = False
        if e:
            e.page.update()

    # English: Opens the search dialog and sets focus to the search field
    # Arabic: يفتح نافذة البحث ويضبط التركيز على حقل البحث
    def open_dlg_search(self, e):
        """
        Opens the search dialog and focuses on the search field.
        Handles potential errors during the process.
        """
        try:
            if self.dlg_modal_search not in e.control.page.overlay:
                e.control.page.overlay.append(self.dlg_modal_search)
                e.control.page.update()

            self.search_field_dialog.focus()
            self.dlg_modal_search.open = True
            self.search_field_dialog.update()
            e.control.page.update()
        except Exception as ex:
            print(f"Error opening search dialog: {ex}")
            # يمكن إضافة تنبيه للمستخدم هنا / Can add user alert here

    # English: Handles scrolling in the search list to load more data
    # Arabic: يتعامل مع التمرير في قائمة البحث لتحميل المزيد من البيانات
    def handle_scroll(self, e):
        """
        Handles the scroll event for the product list.
        Loads more data when the user scrolls near the bottom of the list.
        """
        if e.pixels >= e.max_scroll_extent * 0.9:
            self.load_more_data(None)

    # English: Creates the search dialog with a table for product results
    # Arabic: ينشئ نافذة البحث مع جدول لنتائج المنتجات
    def create_modal_dialog_search(self):
        """Creates a modal dialog for searching products."""
        self.table_search = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text(self.lng[ "top_container"]["search_in_stock"]["id"],color=theme["text_color"])),
                ft.DataColumn(ft.Text(self.lng[ "top_container"]["search_in_stock"]["name"],color=theme["text_color"]),),
                ft.DataColumn(ft.Text(self.lng[ "top_container"]["search_in_stock"]["recommanded"],color=theme["text_color"]),),
                ft.DataColumn(ft.Text(self.lng[ "top_container"]["search_in_stock"]["Current_quantity"],color=theme["text_color"]),),
                ft.DataColumn(ft.Text(self.lng[ "top_container"]["search_in_stock"]["price"],color=theme["text_color"]),),
                ft.DataColumn(ft.Text(self.lng[ "top_container"]["search_in_stock"]["price_per_item"],color=theme["text_color"]),),
            ],
            rows=[],
        )

        self.list_view_search = ft.ListView(
            controls=[self.table_search],
            expand=True,
            spacing=10,
            auto_scroll=False,
            on_scroll=lambda e: self.handle_scroll(e),
        )

        dialog = ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    self.search_field_dialog,
                                    self.make_button(self.lng["search"], lambda e: self.search(e), width=150, height=50),
                                ],
                            ),
                            expand=True
                        ),
                        ft.IconButton(icon=ft.Icons.CLOSE, on_click=lambda e: self.close_dialog(e))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                self.list_view_search,
            ],
        )

        return ft.AlertDialog(
            content=ft.Container(
                width=self.page.width // 1.2,
                height=500,
                content=dialog,
                alignment=ft.alignment.center,
            ),
            bgcolor=theme["container_bg_colors"],
            actions_alignment=ft.MainAxisAlignment.START,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

    # English: Closes the search dialog explicitly
    # Arabic: يغلق نافذة البحث بشكل صريح
    def close_dialog(self, e=None):
        """Closes the search dialog."""
        self.dlg_modal_search.open = False
        self.dlg_modal_search.update()

    # English: Updates the total prices (original and adjusted)
    # Arabic: يحدث الأسعار الإجمالية (الأصلي والمعدل)
    def update_prices(self, original_price_change, sub_price_change):
        try:
            current_price = float(self.price.value)  # Current original total / الإجمالي الأصلي الحالي
            current_sub_price = float(self.sub_price.value)  # Current adjusted total / الإجمالي المعدل الحالي
            
            if not(current_price + original_price_change)>0:
                self.price.value = "0.00"
            else:       
                self.price.value = str(round(current_price + original_price_change, 2))
            
            if not(current_sub_price + sub_price_change)>0:
                self.sub_price.value = "0.00"
            else:    
                self.sub_price.value = str(round(current_sub_price + sub_price_change, 2))
            
            self.price.update()
            self.sub_price.update()
        except Exception as e:
            print(f"خطأ في تحديث الأسعار: {e}")

    # English: Adds a selected product to the main table and updates prices
    # Arabic: يضيف منتجًا مختارًا إلى الجدول الرئيسي ويحدث الأسعار
    def add_row_on_selected(self, e, id, name, price, current_quantity):
        def on_select(e, id):
            for row in self.table.rows:
                if row.cells[1].content.value == str(id) and row.cells[0].content.value == False:
                    self.last_row = row
                    row.cells[0].content.value = True
                elif row.cells[0].content.value == True and row.cells[1].content.value == str(id):
                    self.last_row = None
                    row.cells[0].content.value = False
                elif row.cells[0].content.value == True:
                    row.cells[0].content.value = False
                self.table.update()

        original_price_per_item = float(price)
        initial_quantity = 1  
        total_original_price = original_price_per_item * initial_quantity
        
        self.update_prices(total_original_price, total_original_price)

        row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Checkbox(value=False)),
                ft.DataCell(ft.Text(str(id))),
                ft.DataCell(ft.Text(str(name))),
                ft.DataCell(ft.Text(str(original_price_per_item))),
                ft.DataCell(ft.Text(str(int(current_quantity)))),
                ft.DataCell(ft.Text(str(initial_quantity))),
                ft.DataCell(
                    ft.Row(
                        controls=[
                            self.button(
                                title="حذف",
                                on_click=lambda _: self.delete_row(id),
                            ),
                        ],
                    )
                ),
            ],
            on_select_changed=lambda e: on_select(e, id)
        )
        
        found = False
        for i in self.table.rows:

            if row.cells[1].content.value == i.cells[1].content.value:
                i.cells[5].content.value = str(int(i.cells[5].content.value) + 1)
                found = True
                break
            
        self.dlg_modal_search.open = False
        self.dlg_modal_search.update()
        if not found:
            self.table.rows.append(row)
        self.last_row = row
        self.table.update()

    # English: Loads more data into the search table with pagination.Highlights products with low stock in red.
    # Arabic: يحمل المزيد من بيانات المنتجات إلى جدول البحث مع التصفح

    def load_more_data(self, e):

        if self.current_index < len(self.data_search):
            next_batch = self.data_search[self.current_index: self.current_index + self.batch_size]
            self.current_index += self.batch_size

            for item in next_batch:
                if item[3] < item[2]:
                    self.table_search.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Checkbox(value=False)),
                                ft.DataCell(ft.Text(str(item[0]), color=theme["text_color"])),
                                ft.DataCell(ft.Text(item[1], color=theme["text_color"])),
                                ft.DataCell(ft.Text("     " + str(item[2]), color=theme["text_color"])),
                                ft.DataCell(ft.Text("   " + str(item[3]), color="red")),
                                ft.DataCell(ft.Text("  " + str(item[4]), color=theme["text_color"])),
                                ft.DataCell(ft.Text("  " + str(item[5]), color=theme["text_color"])),
                            ],
                            on_select_changed=lambda e, item=item: self.add_row_on_selected(e, int(item[0]), item[1], float(item[4]), float(item[3]))
                        )
                    )
                else:
                    self.table_search.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(item[0]), color=theme["text_color"])),
                                ft.DataCell(ft.Text(item[1], color=theme["text_color"])),
                                ft.DataCell(ft.Text("     " + str(item[2]), color=theme["text_color"])),
                                ft.DataCell(ft.Text("   " + str(item[3]), color=theme["text_color"])),
                                ft.DataCell(ft.Text("  " + str(item[4]), color=theme["text_color"])),
                                ft.DataCell(ft.Text("  " + str(item[5]), color=theme["text_color"])),
                            ],
                            on_select_changed=lambda e, item=item: self.add_row_on_selected(e, int(item[0]), item[1], float(item[4]), float(item[3]))
                        )
                    )
            self.page.update()

    # English: Searches products based on input and updates the search list
    # Arabic: يبحث عن المنتجات بناءً على الإدخال ويحدث قائمة البحث
    def search(self, e):
        """
        Searches for products based on the input in the search field.
        Updates the product list with the search results.
        """
        self.data_search = self.db_products.search_product(self.search_field_dialog.value)
        if not self.data_search:
            self.table_search.rows.clear()
        self.refresh_products()
        
    # English: Refreshes the search product list with pagination
    # Arabic: ينعش قائمة المنتجات المبحوث عنها مع التصفح
    def refresh_products(self):
        self.table_search.rows.clear()
        self.current_index = 0
        self.load_more_data(None)    
#---------------------------------------end_search_dialog----------------------------------------------


    # English: Creates the main table structure for selected products
    # Arabic: ينشئ هيكل الجدول الرئيسي للمنتجات المختارة
    def create_table(self):
        """Creates the main table for displaying selected products."""
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("ID", color=theme["text_color"])),
                ft.DataColumn(ft.Text(self.lng["table"]['Name'], color=theme["text_color"])),
                ft.DataColumn(ft.Text(self.lng["table"]["Price"], color=theme["text_color"])),
                ft.DataColumn(ft.Text(self.lng["table"]["quantity"], color=theme["text_color"])),
                ft.DataColumn(ft.Text(self.lng["table"]["Number"], color=theme["text_color"])),
                ft.DataColumn(ft.Text(self.lng["table"]["Status"], color=theme["text_color"])),
            ],
            rows=[],
        )

    # English: Creates a list view to wrap the main table
    # Arabic: ينشئ عرض قائمة لتغليف الجدول الرئيسي
    def create_list_view(self):
        """Creates a ListView to wrap the main table."""
        return ft.ListView(
            controls=[self.table],
            expand=True,
            spacing=10,
            auto_scroll=False,
        )

    # English: Sets up the keyboard event listener for the page
    # Arabic: يعين مستمع أحداث لوحة المفاتيح للصفحة
    def setup_keyboard_event(self):
        """Sets up the keyboard event handler."""
        self.page.on_keyboard_event = self.on_keyboard

    # English: Handles keyboard inputs for product addition or order submission
    # Arabic: يتعامل مع إدخالات لوحة المفاتيح لإضافة منتج أو إرسال طلب
    def on_keyboard(self, e: ft.KeyboardEvent):
        """
        Handles keyboard input for quick product addition or order submission.
        Processes input after a short delay to ensure complete entry.
        """
        if self.dlg_modal_search.open:
            return
        if self.page.route != "/orders_screen":
            return False

        if "E" in e.key:
            products = []
            for row in self.table.rows:
                products.append({"product_id": int(row.cells[1].content.value), "quantity": int(row.cells[5].content.value)})

            try:
                for i in products:
                    for row in self.data:
                        if i["product_id"] == row[0]:
                            self.db_products.update_product(row[0], current_quantity=row[3] - i["quantity"])
            except Exception as ex:
                print(f"Error updating product quantities: {ex}")

            self.table.rows.clear()
            self.table.update()

            try:
                self.db_orders.add_order(float(self.price.value), "", products)
            except Exception as ex:
                print(f"Error adding order: {ex}")

            self.price.value = "0.00"
            self.sub_price.value = "0.00"
            self.price.update()
            self.sub_price.update()
            return

        current_time = time.time()
        if current_time - self.input_keyboard_time > 0.5:
            self.input_keyboard = ""
        self.input_keyboard_time = current_time

        if "Numpad" in e.key:
            self.input_keyboard += e.key.split(" ")[1]
        else:
            self.input_keyboard += e.key

        if len(self.input_keyboard) > 0:
            self.search_keyboard()

    # English: Searches for products using keyboard input (e.g., barcode)
    # Arabic: يبحث عن المنتجات باستخدام إدخال لوحة المفاتيح (مثل الباركود)
    def search_keyboard(self):
        """
        Searches for a product by its ID entered via keyboard input.
        Updates the table by incrementing quantity or adding a new row.
        """
        def on_select(e, id):
            for row in self.table.rows:
                if row.cells[1].content.value == str(id) and row.cells[0].content.value == False:
                    self.last_row = row
                    row.cells[0].content.value = True
                elif row.cells[0].content.value == True and row.cells[1].content.value == str(id):
                    self.last_row = None
                    row.cells[0].content.value = False
                elif row.cells[0].content.value == True:
                    row.cells[0].content.value = False
                self.table.update()
                
        found = False
        for row in self.table.rows:
            if row.cells[1].content.value == self.input_keyboard:
                quantity = self.db_products.get_product_by_id(int(row.cells[1].content.value))[3]
                current_value = int(row.cells[5].content.value)
                if not current_value + 1 > quantity:
                    row.cells[5].content.value = str(current_value + 1)
                    original_price = float(row.cells[3].content.value)
                    self.update_prices(original_price, original_price)
                self.last_row = row
                found = True
                break

        if not found and len(self.input_keyboard) > 0:
            for i in self.data:
                if self.input_keyboard == str(i[0]):
                    original_price = float(i[4])
                    self.update_prices(original_price, original_price)
                    row = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Checkbox(value=False)),
                            ft.DataCell(ft.Text(str(i[0]), color=theme["text_color"])),
                            ft.DataCell(ft.Text(str(i[1]), color=theme["text_color"])),
                            ft.DataCell(ft.Text(str(i[4]), color=theme["text_color"])),
                            ft.DataCell(ft.Text(str(i[3]), color=theme["text_color"])),
                            ft.DataCell(ft.Text("1", color=theme["text_color"])),
                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            self.lng["table"]["delete_bottun"],
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=0),
                                                padding=ft.padding.all(5),
                                                bgcolor=theme["icon_button_bg_color"],
                                                color=theme["icon_button_icon_color"],
                                            ),
                                            on_click=lambda _: self.delete_row(i[0]),
                                        ),
                                    ],
                                    spacing=2,
                                )
                            ),
                        ],
                        on_select_changed=lambda e: on_select(e, i[0])
                    )
                    self.table.rows.append(row)
                    self.last_row = row
                    break

        self.table.update()

    # English: Increases product quantity by one and updates prices
    # Arabic: يزيد كمية المنتج بواحد ويحدث الأسعار
    def number_add(self, e, id):
        """
        Increases the quantity of a product by one and updates prices.
        
        Args:
            e: Event object.
            id: Product ID.
        """
        for row in self.table.rows:
            if row.cells[1].content.value == str(id):
                original_price = float(row.cells[3].content.value)
                discounted_price = original_price * 0.9
                self.update_prices(original_price, discounted_price)
                current_value = int(row.cells[5].content.value)
                row.cells[5].content.value = str(current_value + 1)
                break
        self.table.update()

    # English: Deletes a row from the table and updates prices
    # Arabic: يحذف صفًا من الجدول ويحدث الأسعار
    def delete_row(self, id):
        for row in self.table.rows:
            if row.cells[1].content.value == str(id):
                try:
                    quantity = int(row.cells[5].content.value)
                    price_per_item = float(row.cells[3].content.value)
                    total_price = price_per_item * quantity
                    self.update_prices(-total_price, -total_price)
                    self.table.rows.remove(row)
                except Exception as e:
                    print(f"خطأ في حذف الصف: {e}")
                break
        if len(self.table.rows) == 0:
            self.price.value = "0"
            self.sub_price.value = "0"
            self.price.update()
            self.sub_price.update()
        self.table.update()

    # English: Creates the main layout with input panel, table, and navigation
    # Arabic: ينشئ التخطيط الرئيسي مع لوحة الإدخال، الجدول، والتنقل
    def create_main_layout(self):
        def CLR(e):
            self.number_text.value = ""
            self.number_text.update()

        def Entr(self, e):
            if not self.last_row:
                return
            try:
                new_quantity = int(float(self.number_text.value))  # الكمية الجديدة المدخلة
                old_quantity = int(self.last_row.cells[5].content.value)  # الكمية الحالية
                price_per_item = float(self.last_row.cells[3].content.value)  # السعر لكل عنصر
                
                # الحصول على الكمية المتوفرة في المخزون من قاعدة البيانات
                product_id = int(self.last_row.cells[1].content.value)  # معرف المنتج
                available_quantity = self.db_products.get_product_by_id(product_id)[3]  # الكمية المتوفرة
                
                # التحقق من الكمية المتوفرة
                if new_quantity > available_quantity:
                    new_quantity = available_quantity
                
                # تحديث الكمية في الجدول
                self.last_row.cells[5].content.value = str(new_quantity)
                
                # حساب التغيير في السعر بناءً على تغيير الكمية
                quantity_change = new_quantity - old_quantity
                price_change = price_per_item * quantity_change
                
                # تحديث كلا السعرين: السعر الأحمر (الإجمالي الأصلي) والأبيض (الإجمالي المعدل)
                self.update_prices(price_change, price_change)
                
                self.table.update()
            except ValueError:
                print("Invalid quantity entered")
            except Exception as e:
                print(f"Error checking stock: {e}")

        # English: Subtracts a discount from the adjusted price and updates the UI
        # Arabic: يطرح خصمًا من السعر المعدل ويحدث الواجهة
        def Sub_button(self, e):
            if not self.last_row:
                try:
                    subtract_value = float(self.number_text.value)
                    self.update_prices(0, -subtract_value)  
                except ValueError:
                    print("قيمة الخصم غير صالحة")
            else:
                try:
                    subtract_value = float(self.number_text.value)
                    
                    
                    self.update_prices(0, -subtract_value)
                    
                    self.table.update()
                except ValueError:
                    print("قيمة الخصم غير صالحة")

        # English: Adds an amount to the adjusted price and updates the UI
        # Arabic: يضيف مبلغًا إلى السعر المعدل ويحدث الواجهة
        def Add_button(self, e):
            if not self.last_row:
                try:
                    add_value = float(self.number_text.value)
                    self.update_prices(0, add_value)  # السعر الأحمر لا يتغير
                except ValueError:
                    print("قيمة الإضافة غير صالحة")
            else:
                try:
                    add_value = float(self.number_text.value)
                    
                    self.update_prices(0, add_value)
                    
                    self.table.update()
                except ValueError:
                    print("قيمة الإضافة غير صالحة")

        def add_number(e, num):
            self.number_text.value += str(num)
            self.page.update()

        def remove_last(e):
            self.number_text.value = self.number_text.value[:-1]
            self.page.update()

        # English: Numeric keypad for quantity and price adjustments
        # Arabic: لوحة مفاتيح رقمية لتعديل الكميات والأسعار
        number_buttons = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextButton("7", on_click=lambda e: add_number(e, 7), style=self.default_button_style, expand=True, height=70),
                        ft.TextButton("8", on_click=lambda e: add_number(e, 8), style=self.default_button_style, expand=True, height=70),
                        ft.TextButton("9", on_click=lambda e: add_number(e, 9), style=self.default_button_style, expand=True, height=70),
                        ft.TextButton("CLR", on_click=lambda e: CLR(e), style=self.default_button_style, expand=True, height=70),
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.TextButton("4", on_click=lambda e: add_number(e, 4), style=self.default_button_style, expand=True, height=70),
                        ft.TextButton("5", on_click=lambda e: add_number(e, 5), style=self.default_button_style, expand=True, height=70),
                        ft.TextButton("6", on_click=lambda e: add_number(e, 6), style=self.default_button_style, expand=True, height=70),
                        ft.TextButton("Entr", on_click=lambda e: Entr(self, e), style=self.default_button_style, expand=True, height=70),
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.TextButton("1", on_click=lambda e: add_number(e, 1), style=self.default_button_style, expand=True, height=70),
                        ft.TextButton("2", on_click=lambda e: add_number(e, 2), style=self.default_button_style, expand=True, height=70),
                        ft.TextButton("3", on_click=lambda e: add_number(e, 3), style=self.default_button_style, expand=True, height=70),
                        ft.TextButton("-", on_click=lambda e: Sub_button(self, e), style=self.default_button_style, expand=True, height=70),
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.TextButton("⌫", on_click=remove_last, style=self.default_button_style, expand=True, height=70),
                        ft.TextButton("0", on_click=lambda e: add_number(e, 0), style=self.default_button_style, expand=True, height=70),
                        ft.TextButton(".", on_click=lambda e: add_number(e, "."), style=self.default_button_style, expand=True, height=70),
                        ft.TextButton("+", on_click=lambda e: Add_button(self, e), style=self.default_button_style, expand=True, height=70),
                    ]
                )
            ],
            spacing=8,
        )

        # English: Left container with input panel and price displays
        # Arabic: الحاوية اليسرى مع لوحة الإدخال وعروض الأسعار
        left_container = ft.Container(
            content=ft.Column(
                controls=[
                    self.number_text,
                    number_buttons,
                    ft.Column(
                        controls=[
                            ft.Text(self.lng["left_container"]["price"], size=font_size["subtitle"], color=theme["text_color"]),
                            self.price,
                            self.sub_price,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                    ),
                    self.face_focus
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=400,
            padding=20,
            bgcolor=theme["container_bg_colors"],
            border_radius=ft.border_radius.all(theme["container_border_radius"]),
            border=ft.border.all(width=1, color=theme["container_border_color"]),
        )

        # English: Top container with navigation buttons
        # Arabic: الحاوية العلوية مع أزرار التنقل
        top_container = ft.Container(
            content=ft.Row(
                controls=[
                    self.make_button(self.lng["top_container"]["Dashboard"], lambda e: self.page.go("/"), 350, 70),
                    self.search_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=10,
            bgcolor=theme["container_bg_colors"],
            border_radius=ft.border_radius.all(theme["container_border_radius"]),
            border=ft.border.all(width=1, color=theme["container_border_color"]),
        )

        # English: Main content area with table and shopping cart icon
        # Arabic: منطقة المحتوى الرئيسية مع الجدول وأيقونة عربة التسوق
        main_content_container = ft.Container(
            content=ft.Stack(
                [
                    ft.Container(
                        content=ft.Icon(name=ft.Icons.SHOPPING_CART, size=600, opacity=0.4, color="grey"),
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

        vertical_containers = ft.Column(
            controls=[
                top_container,
                main_content_container
            ],
            expand=True,
        )

        return ft.Row(
            controls=[
                left_container,
                vertical_containers
            ],
            expand=True,
            spacing=20,
        )
    # English: Helper method to create styled buttons
    # Arabic: دالة مساعدة لإنشاء أزرار منسقة
