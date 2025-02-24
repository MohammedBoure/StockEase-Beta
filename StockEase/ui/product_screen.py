import flet as ft
from utils.file_utils import theme, font_size


def product_screen(page: ft.Page):
    # Left Container (Price)





    print(theme["check_box_text_color"])

    hide_show_checkbox = ft.Checkbox(
        label="hide top",
        on_change=lambda e: hide_show(),
        label_style=ft.TextStyle(color=theme["check_box_text_color"]),  # Set text color to white
    )
     
    left_container = ft.Container(
        content=ft.Column(
            controls=[
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
                ft.ElevatedButton(
                    width=150,
                    height=50,
                    text="hide top",
                    on_click=lambda e: print("kk"),
                    bgcolor=theme["button_bg_color"],
                    color=theme["button_text_color"],
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        overlay_color=theme["button_overlay_color"],)
                    ),
                    hide_show_checkbox,
                    ]
                    ),
  
           
        
        
        
        width=200,  # Fixed width for the left container
        padding=20,
        bgcolor=theme["container_bg_colors"],
        border_radius=ft.border_radius.all(theme["container_border_radius"]),
        border=ft.border.all(width=1, color=theme["container_border_color"]),
    )


    def hide_show():
        if hide_show_checkbox.value==True:
            vertical_containers.controls.remove(top_container)
        elif hide_show_checkbox.value==False:
            vertical_containers.controls.insert(0,top_container)    
        page.update()



   

    # Top Container (Buttons)
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
                
                
                    ]),
               
        
      
        padding=20,
        bgcolor=theme["container_bg_colors"],
        border_radius=ft.border_radius.all(theme["container_border_radius"]),
        border=ft.border.all(width=1, color=theme["container_border_color"]),
    )

    # Main Content Container (Empty for now)
    main_content_container = ft.Container(
        content=ft.Text("the table will be here",color="white"),
        expand=True,
        padding=20,
        bgcolor=theme["container_bg_colors"],
        border_radius=ft.border_radius.all(theme["container_border_radius"]),
        border=ft.border.all(width=1, color=theme["container_border_color"]),
    )

 
    vertical_containers=ft.Column(
                controls=[
                    top_container,  # Top (Buttons)
                    main_content_container  # Main Content (Empty)
                ],)
    
   # Main Layout
    main_layout = ft.Row(
        controls=[
            left_container,  # Left side (Price)
            vertical_containers],
            expand=True,
            spacing=20,
           
   
    )

    # Main Container
    main_container = ft.Container(
        content=main_layout,
        expand=True,
        padding=20,
        bgcolor=theme["background_colors"],
    )



    
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
