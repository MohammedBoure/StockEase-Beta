import flet as ft
from utils.file_utils import theme, font_size,language
from database.products import ProductDatabase
from database.orders import OrderDatabase
import time
import threading

class OrdersScreen(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/orders_screen")
        self.page = page
        self.page.window.bgcolor = theme["background_colors"]
        self.lng = language["orders"]
        self.number_text = ft.TextField(
            text_size=font_size["input"],
            color=theme["text_color"],
            height=40,
            border_color=theme["input_border_color"],
            fill_color=theme["input_fill_color"],
            hover_color=theme["input_hover_color"],
            cursor_color=theme["input_cursor_color"],
            selection_color=theme["input_selection_color"],
            focused_border_color=theme["input_focused_border_color"],
        )
        self.number_buttons = self.create_number_buttons()
        self.dlg_modal = self.create_modal_dialog()
        self.db_products = ProductDatabase()
        self.db_orders = OrderDatabase()
        self.data = self.db_products.get_all_products()
        self.table = self.create_table()
        self.list_view = self.create_list_view()
        self.input_keyboard = ""
        self.input_keyboard_time = time.time()
        self.last_row = None
        self.price = ft.Text("0", size=font_size["subtitle"], color=theme["text_color"])
        self.setup_keyboard_event()
        self.main_layout = self.create_main_layout()

        # Add the main layout to the views controls
        self.controls = [
            ft.Container(
                content=self.main_layout,
                expand=True,
                alignment=ft.alignment.center
            )
        ]

    def create_number_buttons(self):
        return ft.GridView(
            runs_count=3,
            max_extent=100,
            spacing=10,
            run_spacing=10,
            controls=[
                ft.TextButton(
                    str(i),
                    on_click=lambda e, i=i: self.number_add(i),
                    style=ft.ButtonStyle(
                        bgcolor=theme["button_bg_color"],
                        color=theme["button_text_color"],
                        shape=ft.RoundedRectangleBorder(radius=theme["button_border_radius"]),
                        overlay_color=theme["button_overlay_color"],
                        padding=ft.Padding(12, 8, 12, 8),
                    )
                ) for i in range(10)
            ] + [
                ft.TextButton(
                    "+",
                    on_click=lambda e: print("+ clicked"),
                    style=ft.ButtonStyle(
                        bgcolor=theme["button_bg_color"],
                        color=theme["button_text_color"],
                        shape=ft.RoundedRectangleBorder(radius=theme["button_border_radius"]),
                        overlay_color=theme["button_overlay_color"],
                        padding=ft.Padding(12, 8, 12, 8),
                    )
                ),
                ft.TextButton(
                    "-",
                    on_click=lambda e: print("- clicked"),
                    style=ft.ButtonStyle(
                        bgcolor=theme["button_bg_color"],
                        color=theme["button_text_color"],
                        shape=ft.RoundedRectangleBorder(radius=theme["button_border_radius"]),
                        overlay_color=theme["button_overlay_color"],
                        padding=ft.Padding(12, 8, 12, 8),
                    )
                ),
            ],
        )

    def close_dlg_number(self,e,status):
        self.dlg_modal.open = False
        e.page.update()

    def open_dlg_number(self,e):
        try:
            if self.dlg_modal not in e.control.page.overlay:
                e.control.page.overlay.append(self.dlg_modal)
                e.control.page.update()  

            self.dlg_modal.open = True
            e.control.page.update() 
        except Exception as ex:
            print(f"Exception: {ex}")
            
    def create_modal_dialog(self):
        return ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Text("Number Input", rtl=True),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        on_click=lambda _: self.close_dlg_number(_, False),
                        icon_color=theme["button_text_color"],
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Enter a number:"),
                        self.number_text,
                        ft.Divider(),
                        self.number_buttons,
                    ],
                    spacing=10,
                ),
                height=400,
            ),
            actions=[
                ft.TextButton(
                    "Submit",
                    on_click=lambda _: self.close_dlg_number(_, True),
                    style=ft.ButtonStyle(
                        bgcolor=theme["button_bg_color"],
                        color=theme["button_text_color"],
                        shape=ft.RoundedRectangleBorder(radius=theme["button_border_radius"]),
                        overlay_color=theme["button_overlay_color"],
                        padding=ft.Padding(12, 8, 12, 8),
                    )
                ),
                ft.TextButton(
                    "Cancel",
                    on_click=lambda _: self.close_dlg_number(_, False),
                    style=ft.ButtonStyle(
                        bgcolor=theme["button_bg_color"],
                        color=theme["button_text_color"],
                        shape=ft.RoundedRectangleBorder(radius=theme["button_border_radius"]),
                        overlay_color=theme["button_overlay_color"],
                        padding=ft.Padding(12, 8, 12, 8),
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

    def create_table(self):
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", color=theme["text_color"])),
                ft.DataColumn(ft.Text(self.lng["table"]['Name'], color=theme["text_color"])),
                ft.DataColumn(ft.Text(self.lng["table"]["Price"], color=theme["text_color"])),
                ft.DataColumn(ft.Text(self.lng["table"]["Price_Per_Item"], color=theme["text_color"])),
                ft.DataColumn(ft.Text(self.lng["table"]["Number"], color=theme["text_color"])),
                ft.DataColumn(ft.Text(self.lng["table"]["Status"], color=theme["text_color"])),
            ],
            rows=[],
        )

    def create_list_view(self):
        return ft.ListView(
            controls=[self.table],
            expand=True,
            spacing=10,
            auto_scroll=False,
        )

    def setup_keyboard_event(self):
        self.page.on_keyboard_event = self.on_keyboard

    def on_keyboard(self, e: ft.KeyboardEvent):
        if not self.page.route or self.page.route != "/orders_screen":
            return False

        if "E" in e.key:
            products = []
            for row in self.table.rows:
                products.append({"product_id":int(row.cells[0].content.value),"quantity":int(row.cells[4].content.value)})
              
            for i in products:
                for row in self.data:
                    if i["product_id"]==row[0]:
                        self.db_products.update_product(row[0],current_quantity=row[3]-i["quantity"])
                  
            self.table.rows.clear()
            self.table.update()

            
            self.db_orders.add_order(float(self.price.value),"",products)
            
            
            
            self.price.value = "0.00"
            self.price.update()
            
            return
                
        if time.time() - self.input_keyboard_time > 0.5:
            threading.Timer(0.2, self.search_keyboard).start()
            self.input_keyboard = ""
            self.input_keyboard_time = time.time()

        if "Numpad" in e.key:
            self.input_keyboard += e.key.split(" ")[1]
        else:
            self.input_keyboard += e.key

    def search_keyboard(self):
        
        
        if not (len(self.input_keyboard) == 2) and self.last_row:
            quantity = self.db_products.get_product_by_id(int(self.last_row.cells[0].content.value))[3]
            
            try:int(self.input_keyboard)
            except:return
                        
            if int(self.input_keyboard)>quantity:
                self.last_row.cells[4].content.value =str(quantity)
            else:
                self.last_row.cells[4].content.value = self.input_keyboard
            p = 0
            for row in self.table.rows:
                p = round(float(row.cells[2].content.value) * float(row.cells[4].content.value)+p, 2)
            self.price.value = str(p)
            self.table.update()
            self.price.update()
            return False

        found = False
        for row in self.table.rows:
            if row.cells[0].content.value == self.input_keyboard:
                quantity = self.db_products.get_product_by_id(int(row.cells[0].content.value))[3]
                
                current_value = int(row.cells[4].content.value)
                if not int(row.cells[4].content.value) +1 > quantity:
                    row.cells[4].content.value = str(current_value + 1)
                    self.price.value = str(round(float(row.cells[2].content.value) + float(self.price.value), 2))
                    self.price.update()
                self.last_row = row
                found = True
                break

        if not found:
            for i in self.data:
                if self.input_keyboard == str(i[0]):
                    self.price.value = str(round(i[4] + float(self.price.value), 2))
                    self.price.update()
                    row = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(i[0]), color=theme["text_color"])),
                            ft.DataCell(ft.Text(str(i[1]), color=theme["text_color"])),
                            ft.DataCell(ft.Text(str(i[4]), color=theme["text_color"])),
                            ft.DataCell(ft.Text(str(i[5]), color=theme["text_color"])),
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
                                        ft.ElevatedButton(
                                            self.lng["table"]["number_bottun"],
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=0),
                                                padding=ft.padding.all(5),
                                                bgcolor=theme["icon_button_bg_color"],
                                                color=theme["icon_button_icon_color"],
                                            ),
                                            on_click=lambda e: self.open_dlg_number(e),
                                        ),
                                    ],
                                    spacing=2,
                                )
                            ),
                        ],
                    )
                    self.table.rows.append(row)
                    self.last_row = row
                    break

        self.table.update()

    def number_add(self, e, id):
        for row in self.table.rows:
            if row.cells[0].content.value == str(id):
                self.price.value = str(round(float(row.cells[2].content.value) + float(self.price.value), 2))
                self.price.update()
                current_value = int(row.cells[4].content.value)
                row.cells[4].content.value = str(current_value + 1)
                break
        self.table.update()

    def delete_row(self, id):
        for row in self.table.rows:
            if row.cells[0].content.value == str(id):
                try:
                    current_value = int(row.cells[4].content.value)
                    price_of_item = float(row.cells[2].content.value)
                except:self.db_products.delete_product(int(row.cells[0]))
                
                self.price.value = str(round(float(self.price.value) - current_value * price_of_item, 2))
                self.price.update()
                self.table.rows.remove(row)
                break
        self.table.update()

    def create_main_layout(self):
        left_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(self.lng["left_container"]["price"], size=font_size["subtitle"], color=theme["text_color"]),
                    self.price,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=300,
            padding=20,
            bgcolor=theme["container_bg_colors"],
            border_radius=ft.border_radius.all(theme["container_border_radius"]),
            border=ft.border.all(width=1, color=theme["container_border_color"]),
        )

        top_container = ft.Container(
            content=ft.Row(
                controls=[
                    self.make_button(self.lng["top_container"]["Product"], lambda e: self.page.go("/product_screen"), 150, 70),
                    self.make_button(self.lng["top_container"]["Orders"], lambda e: self.page.go("/orders_screen"), 150, 70),
                    self.make_button(self.lng["top_container"]["Customers"], lambda e: self.page.go("/customers_screen"), 150, 70),
                    self.make_button(self.lng["top_container"]["Dashboard"], lambda e: self.page.go("/"), 150, 70),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=20,
            bgcolor=theme["container_bg_colors"],
            border_radius=ft.border_radius.all(theme["container_border_radius"]),
            border=ft.border.all(width=1, color=theme["container_border_color"]),
        )

        main_content_container = ft.Container(
            content=ft.Stack(
                [
                    ft.Container(
                        content=ft.Icon(name=ft.Icons.SHOPPING_CART, size=600, opacity=0.4,color="grey"),
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

    def make_button(self, text, on_click, width, height):
        return ft.ElevatedButton(
            width=width,
            height=height,
            text=text,
            on_click=on_click,
            bgcolor=theme["button_bg_color"],
            color=theme["button_text_color"],
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=theme["button_border_radius"]),
                overlay_color=theme["button_overlay_color"],
            )
        )