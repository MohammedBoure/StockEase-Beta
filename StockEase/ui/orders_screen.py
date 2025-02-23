import flet as ft
from utils.file_utils import theme,font_size

def orders_screen(page:ft.Page):

    def order_information_table():  
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Price")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{i}")),
                        ft.DataCell(ft.Text(f"Product {i}")),
                        ft.DataCell(ft.Text(f"$10{i}")),
                    ]
                ) for i in range (30)
            ]
        )

        return table

        """
            rows=[
    ft.DataRow(
        cells=[
            ft.DataCell(ft.Text(f"{i}")),
            ft.DataCell(ft.Text(f"Product {i}")),
            ft.DataCell(ft.Text(f"$10{i}")),
        ]
    ) for i in range(30)
]  # ✅ No extra parenthesis
"""
       
     
    
    def delete_sub_side_container_top(e):
        container_buttom.content.controls.pop(len(container_buttom.content.controls)-1)
        page.update()
        

    


    def show_navigation_buttons(e):
        container_buttom.content.controls.append(sub_side_container_top)
        page.update()
        pass



    sub_side_container_top=ft.Container(
        width=200,
        height=500,
        bgcolor="yellow",
        content=ft.Column(controls=[ft.ElevatedButton(text="go back",on_click=delete_sub_side_container_top),
                                    ft.ElevatedButton(text="Order Information Section"),
                                    ft.ElevatedButton(text="Order Items List"),
                                    ft.ElevatedButton(text="Order Summary"),
                                    ft.ElevatedButton(text="Payment Details"),
                                    ft.ElevatedButton(text="Order Actions"),
                                    ft.ElevatedButton(text="Delivery & Shipping Details "),
                                    ft.ElevatedButton(text="Order History "),])
    )

    sub_side_container_top_button1=ft.IconButton(icon=ft.icons.MENU,on_click=show_navigation_buttons)
    sub_side_container_top_button2=ft.IconButton(icon=ft.icons.CANCEL)
    sub_side_container_top_button3=ft.IconButton(icon=ft.icons.CANCEL)

    
    


    side_icons_container=ft.Container(
        width=40,
        height=150,
        bgcolor="red",
        content=ft.Container(content=ft.Column(controls=[sub_side_container_top_button1,
                                    sub_side_container_top_button2,
                                    sub_side_container_top_button3,]),)
    )
    bellow_side_icons_container=ft.Container(bgcolor="black",
                                             width=100,
                                             height=150,)
    #side container                        ////                         content_container
       #side_icons_container                                                nothing yet            
       #bellow_side_icons_container     
    side_container=ft.Container(content=ft.Column(controls=[side_icons_container,bellow_side_icons_container]))


    table=order_information_table()
    content_container=ft.Container(width=500,
                                   height=500,                                   
                                   bgcolor="brown",
                                   content=ft.Column(controls=[table],
                                   scroll=ft.ScrollMode.AUTO)

                                   

    )

    content_container_column=ft.Column(controls=[content_container])
    main_structure=ft.Row(controls=[side_container, content_container_column])


    container_buttom=ft.Container(
        width=800,
        height=800,
        bgcolor="green",
        content=ft.Stack(controls=[main_structure])
        )




    return ft.View(
        route="/orders_screen",
        controls=[container_buttom,],
        #bgcolor=theme["background_colors"][0]
    )