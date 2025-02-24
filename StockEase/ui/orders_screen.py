import flet as ft
from utils.file_utils import theme,font_size
import random
import time
import threading

def orders_screen(page: ft.Page):
    
    def close_dlg_accoun_name(e, confirmed):
        dlg_modal.open = False
        e.page.update()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Number", rtl=True),
        content=ft.Text("-------------", rtl=True),
        actions=[
            ft.TextButton(
                "نعم",
                on_click=lambda _: close_dlg_accoun_name(_, True),
                style=ft.ButtonStyle(
                    bgcolor=theme["button_bg_color"],
                    color=theme["button_text_color"],
                    shape=ft.RoundedRectangleBorder(radius=10),
                    overlay_color=theme["button_overlay_color"],
                    padding=ft.Padding(12, 8, 12, 8),
                )
            ),
            ft.TextButton(
                "لا",
                on_click=lambda _: close_dlg_accoun_name(_, False),
                style=ft.ButtonStyle(
                    bgcolor=theme["button_bg_color"],
                    color=theme["button_text_color"],
                    shape=ft.RoundedRectangleBorder(radius=10),
                    overlay_color=theme["button_overlay_color"],
                    padding=ft.Padding(12, 8, 12, 8),
                )
            ),
            ft.IconButton(
                icon=ft.icons.CLOSE,
                on_click=lambda _: close_dlg_accoun_name(_, False),
                icon_color=theme["button_text_color"],
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    number_buttons = ft.GridView(
        runs_count=3,
        max_extent=100,
        spacing=10,
        run_spacing=10,
        controls=[
            ft.TextButton(
                str(i),
                on_click=lambda e, i=i: print(f"Number {i} clicked"),
                style=ft.ButtonStyle(
                    bgcolor=theme["button_bg_color"],
                    color=theme["button_text_color"],
                    shape=ft.RoundedRectangleBorder(radius=10),
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
                    shape=ft.RoundedRectangleBorder(radius=10),
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
                    shape=ft.RoundedRectangleBorder(radius=10),
                    overlay_color=theme["button_overlay_color"],
                    padding=ft.Padding(12, 8, 12, 8),
                )
            ),
        ],
    )

    dlg_modal.content = ft.Column(
        controls=[
            dlg_modal.content,
            number_buttons,
        ],
    )


    def open_dlg_accoun_name(e):
        try:

            if dlg_modal not in e.control.page.overlay:
                e.control.page.overlay.append(dlg_modal)
                e.control.page.update()  

            dlg_modal.open = True
            e.control.page.update() 

        except Exception as ex:
            print(f"Exception: {ex}")
    
    # Left Container (Price)
    num_records = 1000
    data = [
        (
            random.randint(1, 100),  # ID عشوائي
            random.choice(["soker", "gold", "silver", "platinum", "bronze"]),  # اسم عشوائي
            random.randint(1, 20),  # الكمية السابقة
            random.randint(5, 50),  # الكمية الحالية
            random.randint(10, 100),  # السعر الإجمالي
            random.randint(5, 20),  # السعر لكل وحدة
        )
        for _ in range(num_records)
    ]
    
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID",)), 
            ft.DataColumn(ft.Text("Name",)),
            ft.DataColumn(ft.Text("Price",)),
            ft.DataColumn(ft.Text("Price Per Item",)),
            ft.DataColumn(ft.Text("number",)),
            ft.DataColumn(ft.Text("          status",)),
        ],
        rows=[],
    )
    
    list_view = ft.ListView(
        controls=[table],
        expand=True,
        spacing=10,
        auto_scroll=False,
    )
    
    input_keyboard = ""
    input_keyboard_time = time.time()
    
    
    def search_keyboard():
        nonlocal input_keyboard
        nonlocal price

        found = False
        for row in table.rows:
            if row.cells[0].content.value == input_keyboard:
                current_value = int(row.cells[4].content.value)  
                row.cells[4].content.value = str(current_value + 1)
                price.value = str(float(row.cells[2].content.value) + float(price.value))
                price.update()
                found = True
                break

        if not found:
            for i in data:
                if input_keyboard == str(i[0]):
                    price.value = str(i[4] + float(price.value))
                    price.update()
                    table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(i[0]))),
                                ft.DataCell(ft.Text(str(i[1]))),
                                ft.DataCell(ft.Text(str(i[4]))),
                                ft.DataCell(ft.Text(str(i[5]))),
                                ft.DataCell(ft.Text("1")),
                                ft.DataCell(
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton(
                                                "delete",
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=0),
                                                    padding=ft.padding.all(5),
                                                    bgcolor="#700d0d",
                                                    color="#ffffff",
                                                ),
                                                on_click=lambda _:delete_row(i[0]),
                                            ),
                                            ft.ElevatedButton(
                                                "number",
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=0),
                                                    padding=ft.padding.all(5),
                                                    bgcolor="#1b5210",
                                                    color="#ffffff",
                                                ),
                                                on_click=lambda e: number_add(e,i[0]),
                                            ),
                                        ],
                                        spacing=2,
                                    )
                                ),
                            ],
                        )
                    )
                    break

        table.update()
        
    def on_keyboard(e: ft.KeyboardEvent):
        nonlocal input_keyboard
        nonlocal input_keyboard_time
        if time.time() - input_keyboard_time > 1:
            threading.Timer(0.2,search_keyboard).start()

            
            input_keyboard = ""
            input_keyboard_time = time.time()
        if "Numpad" in e.key:
            input_keyboard += e.key.split(" ")[1]
        else:
            input_keyboard += e.key
    
    page.on_keyboard_event = on_keyboard

    price = ft.Text("0", size=font_size["subtitle"], color=theme["text_color0"])
    
    def number_add(e,id):
        nonlocal price
        open_dlg_accoun_name(e)
        for row in table.rows:
            if row.cells[0].content.value == str(id):
                price.value = str(float(row.cells[2].content.value) + float(price.value))
                price.update()
                current_value = int(row.cells[4].content.value)  
                row.cells[4].content.value = str(current_value + 1) 
                break
        table.update()
    
    def delete_row(id):
        nonlocal price
        for row in table.rows:
            if row.cells[0].content.value == str(id):
                current_value = int(row.cells[4].content.value)
                price_of_item = float(row.cells[2].content.value)
                price.value = str(float(price.value) - current_value*price_of_item)
                price.update()
                table.rows.remove(row)
                break
        table.update()
    
    left_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("price", size=font_size["subtitle"], color=theme["text_color0"]),
                price,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=300,  # Fixed width for the left container
        padding=20,
        bgcolor=theme["container_bg_colors"],
        border_radius=ft.border_radius.all(theme["container_border_radius"]),
        border=ft.border.all(width=1, color=theme["container_border_color"]),
    )

    top_container = ft.Container(
        content=ft.Row(controls=[
                    ft.ElevatedButton(
                    width=150,
                    height=50,
                    text="Add Product",   
                    on_click=lambda e: print("Add Product Clicked"),
                    bgcolor=theme["button_bg_color"],
                    color=theme["button_text_color"],
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        overlay_color=theme["button_overlay_color"],
                    )
                ),
                ft.ElevatedButton(
                    width=150,
                    height=50,
                    text="Add Product",
                    on_click=lambda e: print("Edit Product Clicked"),
                    bgcolor=theme["button_bg_color"],
                    color=theme["button_text_color"],
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        overlay_color=theme["button_overlay_color"],
                    )
                ),
                ft.ElevatedButton(
                    width=150,
                    height=50,
                    text="Add Product",
                    on_click=lambda e: print("Delete Product Clicked"),
                    bgcolor=theme["button_bg_color"],
                    color=theme["button_text_color"],
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        overlay_color=theme["button_overlay_color"],
                    )
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
               
        padding=20,
        bgcolor=theme["container_bg_colors"],
        border_radius=ft.border_radius.all(theme["container_border_radius"]),
        border=ft.border.all(width=1, color=theme["container_border_color"]),
    )

    main_content_container = ft.Container(
        content=list_view,
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

    main_layout = ft.Row(
        controls=[
            left_container,
            vertical_containers
        ],
        expand=True,
        spacing=20,
    )

    main_container = ft.Container(
        content=main_layout,
        expand=True,
        padding=20,
        bgcolor=theme["background_colors"],
    )


    return ft.View(
        route="/orders_screen",
        controls=[  
            ft.Container(
                content=main_container,
                expand=True,
                alignment=ft.alignment.center
            )
        ],
       
    )