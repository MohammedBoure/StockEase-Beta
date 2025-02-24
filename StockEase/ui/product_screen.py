import flet as ft
from utils.file_utils import theme, font_size
import random



def product_screen(page: ft.Page):
    # Left Container (Price)

    hide_show_checkbox = ft.Checkbox(
        label="hide top",
        on_change=lambda e: hide_show(),
        label_style=ft.TextStyle(color=theme["check_box_text_color"]),  # Set text color to white
    )
     
    def hide_show():
        if special_button.text=="hide":
            vertical_containers.controls.remove(top_container)
            special_button.text="show"


        elif special_button.text=="show":
            vertical_containers.controls.insert(0,top_container)    
            special_button.text="hide"
        page.update()


    def make_button(text,on_click,width,height):
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
    
    def refresh_products():
        nonlocal current_index
        nonlocal list_selected
        
        table.rows.clear()
        current_index = 0
        list_selected = []
        
        load_more_data(None)

    special_button=make_button("hide",lambda e: hide_show(),width=150,height=50)
    

    search_text=ft.Row(controls=[ft.Text("search label",color="white",size=font_size["subtitle"])],alignment=ft.MainAxisAlignment.CENTER)

    search_label=ft.Column(controls=[
            search_text,
            
            ft.TextField(
                label="Search",
                label_style=ft.TextStyle(color=theme["text_color0"]),)
            ]
            )
            
                 
             
                 
    


    left_container = ft.Container(
        content=ft.Column(
            controls=[
                    special_button,
                    ft.Divider(height=1, color=theme["divider_color"]),
                    search_label,
                    
                    ft.Divider(height=1, color=theme["divider_color"]),
                    make_button("Add Product",lambda e: print("Add Product Clicked"),width=150,height=50),
                    make_button("Edit Product",lambda e: print("Edit Product Clicked"),width=150,height=50),
                    make_button("Delete Product",lambda e: print("Delete Product Clicked"),width=150,height=50),
                    make_button("hide top",lambda e: print("kk"),width=150,height=50),
                    
                    
                    ],
            horizontal_alignment="center",  # محاذاة أفقية في المنتصف
            ),
  
           
        
        
        
        width=300,  # Fixed width for the left container
        padding=20,
        bgcolor=theme["container_bg_colors"],
        border_radius=ft.border_radius.all(theme["container_border_radius"]),
        border=ft.border.all(width=1, color=theme["container_border_color"]),
    )

    
    # Top Container (Buttons)
    top_container = ft.Container(
        content=ft.Row(controls=[
                    make_button("Product",lambda e: refresh_products(),width=150,height=50),
                    make_button("orders",lambda e:page.go("/orders_screen"),width=150,height=50),
                    make_button("costumers",lambda e:page.go("/customers_screen"),width=150,height=50),
                    make_button("dashboard",lambda e:page.go("/"),width=150,height=50),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
               
        padding=20,
        bgcolor=theme["container_bg_colors"],
        border_radius=ft.border_radius.all(theme["container_border_radius"]),
        border=ft.border.all(width=1, color=theme["container_border_color"]),
    )

    # generate random data
    num_records = 1000
    data = [
        (
            random.randint(32110000, 32119999),  # ID عشوائي
            random.choice(["soker", "gold", "silver", "platinum", "bronze"]),  # اسم عشوائي
            random.randint(1, 20),  # الكمية السابقة
            random.randint(5, 50),  # الكمية الحالية
            random.randint(10, 100),  # السعر الإجمالي
            random.randint(5, 20),  # السعر لكل وحدة
        )
        for _ in range(num_records)
    ]

    batch_size = 20
    current_index = 0 
    list_selected = []
    
    def on_change(e, id, name, last_quantity, quantity, price, price_per_item):
        item = (id, name, last_quantity, quantity, price, price_per_item)
        if e.data == "true":
            list_selected.append(item)
        else:
            list_selected.remove(item)
        print("Selected Items:", list_selected)

    # for check and uncheck all rows
    def select_all_rows(e):
        nonlocal list_selected
        is_checked = e.control.value
        loaded_data = data[:current_index]
        
        if is_checked:
            for item in loaded_data:
                if item not in list_selected:
                    list_selected.append(item)
        else:
            list_selected = []
        print("Selected Items after select all:", list_selected)
        
        # تحديث حالة Checkbox لكل صف
        for row in table.rows:
            row.cells[0].content.value = is_checked
        page.update()

    # to laod more data
    def load_more_data(e):
        nonlocal current_index
        if current_index < len(data):
            next_batch = data[current_index:current_index + batch_size]
            current_index += batch_size

            for item in next_batch:
                table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Checkbox(
                                on_change=lambda e: on_change(e, item[0], item[1], item[2], item[3], item[4], item[5])
                            )),
                            ft.DataCell(ft.Text(str(item[0]),color="white")),
                            ft.DataCell(ft.Text(item[1],color="white")),
                            ft.DataCell(ft.Text(str(item[2]),color="white")),
                            ft.DataCell(ft.Text(str(item[3]),color="white")),
                            ft.DataCell(ft.Text(str(item[4]),color="white")),
                            ft.DataCell(ft.Text(str(item[5]),color="white")),
                        ],
                    )
                )
            page.update()

    def button(title, on_click):
        return ft.TextButton(
                title,
                on_click=on_click,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=0),
                    padding=ft.padding.all(5),
                    color="white"

                ))

    status = True
    
    def on_click_id_btn(e,y):
        nonlocal data
        nonlocal current_index
        nonlocal status
    
        if y == 0:
            data = sorted(data, key=lambda x: x[y], reverse=status)
        elif y == 1:
            data = sorted(data, key=lambda x: x[y], reverse=status)
        elif y == 2:
            data = sorted(data, key=lambda x: x[y], reverse=status)
        elif y == 3:
            data = sorted(data, key=lambda x: x[y], reverse=status)
        elif y == 4:
            data = sorted(data, key=lambda x: x[y], reverse=status)
        elif y == 5:
            data = sorted(data, key=lambda x: x[y], reverse=status)
        status = not status
        table.rows = []
        current_index = 0
        load_more_data(None)
        
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Checkbox(on_change=select_all_rows)),
            ft.DataColumn(button("ID",lambda e:on_click_id_btn(e,0))), 
            ft.DataColumn(button("Name",lambda e:on_click_id_btn(e,1))),
            ft.DataColumn(button("Last Quantity",lambda e:on_click_id_btn(e,2))),
            ft.DataColumn(button("Quantity",lambda e:on_click_id_btn(e,3))),
            ft.DataColumn(button("Price",lambda e:on_click_id_btn(e,4))),
            ft.DataColumn(button("Price Per Item",lambda e:on_click_id_btn(e,5))),
        ],
        rows=[],
    )
    
    def scroll(e):
        if e.pixels >= e.max_scroll_extent * 1:
            load_more_data(None)

    list_view = ft.ListView(
        controls=[table],
        expand=True,
        spacing=10,
        auto_scroll=False,
        on_scroll=scroll,
        
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

    load_more_data(None)

    return ft.View(
        route="/product_screen",
        controls=[  
            ft.Container(
                content=main_container,
                expand=True,
                alignment=ft.alignment.center
            )
        ],
    )