import flet as ft
from utils.file_utils import theme, font_size,language
from database.products import ProductDatabase
import random

class ProductScreenView(ft.View):
    """
    A view class for managing and displaying product-related operations.
    This class handles the UI and logic for adding, updating, deleting, and searching products.
    It also manages the display of product data in a table with pagination and sorting.
    """
    def __init__(self, page: ft.Page):
        """
        Initializes the ProductScreenView with the necessary UI components and data.
        Sets up the layout, buttons, search field, and data table.
        Also initializes modal dialogs for adding, updating, and deleting products.
        """
        super().__init__(route="/product_screen")
        self.page = page
        self.lng = language["product"]
        self.db_products = ProductDatabase()
        self.data = self.db_products.get_all_products()  
        self.batch_size = 20
        self.current_index = 0
        self.list_selected = []
        self.status = True  

        self.special_button = self.make_button(
            self.lng["left_container"]["hide_special_button"], lambda e: self.hide_show(), width=250, height=50
        )

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
        self.left_container = ft.Container(
            content=ft.Column(
                controls=[
                    self.special_button,
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

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Checkbox(on_change=self.select_all_rows)),
                ft.DataColumn(self.button("ID", lambda e: self.on_click_id_btn(e, 0))),
                ft.DataColumn(self.button(self.lng["table"]["Name"], lambda e: self.on_click_id_btn(e, 1))),
                ft.DataColumn(self.button(self.lng["table"]["recommended_quantity"], lambda e: self.on_click_id_btn(e, 2))),
                ft.DataColumn(self.button(self.lng["table"]["Quantity"], lambda e: self.on_click_id_btn(e, 3))),
                ft.DataColumn(self.button(self.lng["table"]["Price"], lambda e: self.on_click_id_btn(e, 4))),
                ft.DataColumn(self.button(self.lng["table"]["Price_Per_Item"], lambda e: self.on_click_id_btn(e, 5))),
            ],
            rows=[],
        )

        self.list_view = ft.ListView(
            controls=[self.table],
            expand=True,
            spacing=10,
            auto_scroll=False,
            on_scroll=lambda e:self.handle_scroll(e),
        )

        self.main_content_container = ft.Container(
            content=ft.Stack(
                [
                    ft.Container(
                        content=ft.Icon(name=ft.Icons.SHOPIFY_ROUNDED, size=600, opacity=0.3,color="grey"),
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

        self.vertical_containers = ft.Column(
            controls=[
                self.top_container,
                self.main_content_container
            ],
            expand=True,
        )

        self.main_layout = ft.Row(
            controls=[
                self.left_container,
                self.vertical_containers
            ],
            expand=True,
            spacing=20,
        )

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

        self.dlg_modal_add = self.create_modal_dialog_add()
        self.dlg_modal_update = self.create_modal_dialog_update()
        self.dlg_modal_delete = self.create_modal_dialog_delete()
        self.load_more_data(None)
    
    #for dialog_delete
    def close_dlg_delete(self,e,status):
        """
        Closes the delete confirmation dialog and performs the deletion if confirmed.
        Deletes selected products from the database and updates the product list.
        """
        if status == True:
            for i in self.list_selected:
                self.db_products.delete_product(i[0])
            self.list_selected = []
            self.data = self.db_products.get_all_products()

        self.refresh_products()
        self.dlg_modal_delete.open = False
        e.page.update()     
    def open_dlg_delete(self,e):
        """
        Opens the delete confirmation dialog.
        Ensures the dialog is added to the page overlay if not already present.
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
        Creates and returns a modal dialog for confirming product deletion.
        The dialog includes 'Yes' and 'No' buttons to confirm or cancel the deletion.
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
    #--------end_dialog_delete-----------
     
   #for dialog_update
    def close_dlg_update(self,e):
        """
        Closes the update product dialog and refreshes the product list.
        """
        self.refresh_products()
        self.dlg_modal_update.open = False
        e.page.update()
    def dlg_update(self,e,name, recommended_quantity, current_quantity, price, purchase_price):
        """
        Handles the logic for updating a product in the database.
        Validates the input and updates the product details if the input is valid.
        Refreshes the product list after the update.
        """
        if len(self.list_selected)!=1:
            self.text_invailed.value = self.lng["left_container"]["Edit_Product"]["invailed_text"]
            self.text_invailed.update()
            return
        try:

            self.db_products.update_product(
                self.list_selected[0][0],
                name,
                int(recommended_quantity),
                int(current_quantity),
                float(price),
                float(purchase_price),
            )
        except:
            self.text_invailed.value = self.lng["left_container"]["Edit_Product"]["invailed_text"]
            self.text_invailed.update()
            return
        
        for i in range(len(self.data)):
            if self.data[i][0] == self.list_selected[0][0]:
                self.data[i]=(
                    self.list_selected[0][0],
                    name,
                    int(recommended_quantity),
                    int(current_quantity),
                    float(price),
                    float(purchase_price))
        
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
    def open_dlg_update(self,e):
        """
        Opens the update product dialog and pre-fills the form with the selected product's details.
        Ensures the dialog is added to the page overlay if not already present.
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
        Creates and returns a modal dialog for updating product details.
        The dialog includes input fields for product name, quantities, price, and purchase price.
        """
        def Text(lbl,y,hint):
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
        #id,name, recommended_quantity, current_quantity, price, purchase_price
        self.name_field = Text(lbl=self.lng["left_container"]["Edit_Product"]["Name"], y=300,hint="string")
        self.recommended_quantity_field = Text(lbl=self.lng["left_container"]["Edit_Product"]["Recommended_quantity"], y=300,hint="integer")
        self.current_quantity_field = Text(lbl=self.lng["left_container"]["Edit_Product"]["Current_quantity"], y=300,hint="integer")
        self.price_field = Text(lbl=self.lng["left_container"]["Edit_Product"]["price"], y=300,hint="real")
        self.purchase_price_field = Text(lbl=self.lng["left_container"]["Edit_Product"]["Purchase_price"], y=300,hint="real")
        self.text_invailed = ft.Text("",color="red")
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
                                e,
                                self.name_field.value,
                                self.recommended_quantity_field.value,
                                self.current_quantity_field.value,
                                self.price_field.value,
                                self.purchase_price_field.value,
                                ), width=200, height=50),
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
    #--------end_dialog_update-----------

    #for dialog_add
    def on_click_generate_barcode(self, e):
        """
        Generates a unique invalid EAN-13 barcode for a new product.
        Ensures the generated barcode does not conflict with existing barcodes in the database.
        Updates the ID field in the add product dialog with the generated barcode.
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
    def close_dlg_add(self,e):
        """
        Closes the add product dialog and refreshes the product list.
        """
        self.refresh_products()
        self.dlg_modal_add.open = False
        e.page.update()
    def dlg_add(self,e,id,name, recommended_quantity, current_quantity, price, purchase_price):
        """
        Handles the logic for adding a new product to the database.
        Validates the input and adds the product if the input is valid.
        Updates the product list after the addition."""
        
        try:
            self.db_products.add_product(
                int(id),
                name,
                int(recommended_quantity),
                int(current_quantity),
                float(price),
                float(purchase_price),
            )
            self.data.append((int(id),
                name,
                int(recommended_quantity),
                int(current_quantity),
                float(price),
                float(purchase_price))
            )
        except:
            return
            
        
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
    def open_dlg_add(self,e):
        """
        Opens the add product dialog and ensures it is added to the page overlay if not already present.
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
        Creates and returns a modal dialog for adding a new product.
        The dialog includes input fields for product ID, name, quantities, price, and purchase price.
        Also includes a button to generate a unique barcode for the product.
        """
        def Text(lbl,y,hint):
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
        #id,name, recommended_quantity, current_quantity, price, purchase_price
        self.id_field_add = Text(lbl="ID", y=250,hint="#############")
        self.name_field_add = Text(lbl=self.lng["left_container"]["Add_Product"]["Name"], y=300,hint="string")
        self.recommended_quantity_field_add = Text(lbl=self.lng["left_container"]["Add_Product"]["Recommended_quantity"], y=300,hint="integer")
        self.current_quantity_field_add = Text(lbl=self.lng["left_container"]["Add_Product"]["Current_quantity"], y=300,hint="integer")
        self.price_field_add = Text(lbl=self.lng["left_container"]["Add_Product"]["price"], y=300,hint="Real")
        self.purchase_price_field_add = Text(lbl=self.lng["left_container"]["Add_Product"]["Purchase_price"], y=300,hint="real")
        
        dialog = ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(self.lng["left_container"]["Add_Product"]["Add_Product"],
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER),
                        ft.IconButton(ft.Icons.CLOSE,
                                      on_click=lambda e: self.close_dlg_add(e)),
                    ],
                ),
                ft.Divider(),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            spacing=10,
                            controls=[
                                ft.Row(controls=[self.id_field_add,
                                        ft.IconButton(icon=ft.Icons.QR_CODE_2, on_click=lambda e: self.on_click_generate_barcode(e),
                                                    style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=theme["icon_button_border_radius"]),
                                                    overlay_color=theme["icon_button_overlay_color"],
                                                    icon_color=theme["icon_button_icon_color"],
                                                    ),
                                            ),]),
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
                                e,
                                self.id_field_add.value,
                                self.name_field_add.value,
                                self.recommended_quantity_field_add.value,
                                self.current_quantity_field_add.value,
                                self.price_field_add.value,
                                self.purchase_price_field_add.value,
                                ), width=200, height=50),
                            self.make_button(text=self.lng["left_container"]["Add_Product"]["exit"], on_click=lambda e: self.close_dlg_add(e), width=200, height=50),
                        ],
                    ),
                    alignment=ft.alignment.center,  
                    expand=True,  
                )
,
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
    #--------end_dialog_add-----------

    def handle_scroll(self, e):
        """
        Handles the scroll event for the product list.
        Loads more data when the user scrolls near the bottom of the list.
        """
        if e.pixels >= e.max_scroll_extent * 0.9:
            self.load_more_data(None)

    def make_button(self, text, on_click, width, height, icon=None):
        """
        Creates and returns a styled button with the specified text, click handler, width, height, and optional icon.
        Applies consistent styling from the theme configuration.
        """
        controls = []
        
        if icon:
            controls.append(ft.Icon(icon, color=theme["button_text_color"],size=25))

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
                alignment=ft.MainAxisAlignment.CENTER,  # يضمن بقاء النص في المنتصف
                spacing=8  
            ) 
        )


    def button(self, title, on_click):
        """
        Creates and returns a text button with the specified title and click handler.
        Used for column headers in the product table.
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

    def hide_show(self):
        """
        Toggles the visibility of the top container (navigation buttons).
        Updates the button text to reflect the current state (hide/show).
        """
        if self.special_button.text == self.lng["left_container"]["hide_special_button"]:
            if self.top_container in self.vertical_containers.controls:
                self.vertical_containers.controls.remove(self.top_container)
            self.special_button.text = self.lng["left_container"]["show_special_button"]
        elif self.special_button.text == self.lng["left_container"]["show_special_button"]:
            self.vertical_containers.controls.insert(0, self.top_container)
            self.special_button.text = self.lng["left_container"]["hide_special_button"]
        self.page.update()

    def search(self, e):
        """
        Searches for products based on the input in the search field.
        Updates the product list with the search results.
        """
        self.data = self.db_products.search_product(self.search_field.value)
        if not self.data:
            self.table.clean()
        self.refresh_products()

    def refresh_products(self):
        """
        Refreshes the product list by clearing the current data and reloading it from the database.
        Resets the selected items and the current index for pagination.
        """
        self.table.rows.clear()
        self.current_index = 0
        self.list_selected = []
        self.load_more_data(None)

    def reset_table(self):
        self.data = self.db_products.get_all_products()
        self.refresh_products()
    
    def on_change(self, e, id, name, last_quantity, quantity, price, price_per_item):
        """
        Handles the change event for checkboxes in the product table.
        Updates the list of selected items based on the checkbox state.
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
        Handles the select-all checkbox in the product table.
        Selects or deselects all rows based on the checkbox state.
        Updates the list of selected items accordingly.
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
        Loads more product data into the table when the user scrolls down.
        Implements pagination by loading data in batches.
        """
        if self.current_index < len(self.data):
            next_batch = self.data[self.current_index: self.current_index + self.batch_size]
            self.current_index += self.batch_size

            for item in next_batch:
                def make_on_change(item):
                    return lambda e: self.on_change(e, item[0], item[1], item[2], item[3], item[4], item[5])
                
                if item[3]<item[2]:
                    self.table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Checkbox(on_change=make_on_change(item))),
                                ft.DataCell(ft.Text(str(item[0]), color=theme["text_color"])),
                                ft.DataCell(ft.Text(item[1], color=theme["text_color"])),
                                ft.DataCell(ft.Text("     "+str(item[2]), color=theme["text_color"])),
                                ft.DataCell(ft.Text("   "+str(item[3]), color="red")),
                                ft.DataCell(ft.Text("  "+str(item[4]), color=theme["text_color"])),
                                ft.DataCell(ft.Text("  "+str(item[5]), color=theme["text_color"])),
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
                                ft.DataCell(ft.Text("     "+str(item[2]), color=theme["text_color"])),
                                ft.DataCell(ft.Text("   "+str(item[3]), color=theme["text_color"])),
                                ft.DataCell(ft.Text("  "+str(item[4]), color=theme["text_color"])),
                                ft.DataCell(ft.Text("  "+str(item[5]), color=theme["text_color"])),
                            ]
                        )
                    )
            print(f"Loaded up to index: {self.current_index}")
            self.page.update()

    def on_click_id_btn(self, e, col_index):
        """
        Handles the click event for column headers in the product table.
        Sorts the product data based on the clicked column and toggles the sort order.
        """
        self.data = sorted(
            self.data,
            key=lambda x: x[col_index],
            reverse=self.status
        )
        self.status = not self.status
        self.table.rows = []
        self.current_index = 0
        self.load_more_data(None)

    def Out_of_stock_products(self,e):
        newlist = []
        for item in self.data:
            if item[3]<item[2]:
                newlist.append(item)
            self.data = newlist
        self.refresh_products()
        