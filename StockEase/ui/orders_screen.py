import flet as ft
from utils.file_utils import theme,font_size

def orders_screen(page: ft.Page):
    # Left Container (Price)
    left_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Price", size=font_size["title"], weight="bold", color=theme["text_color0"]),
                ft.Text("$99.99", size=font_size["subtitle"], color=theme["text_color0"]),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=200,  # Fixed width for the left container
        padding=20,
        bgcolor=theme["container_bg_colors"],
        border_radius=ft.border_radius.all(theme["container_border_radius"]),
        border=ft.border.all(width=1, color=theme["container_border_color"]),
    )

    # Top Container (Buttons)
    top_container = ft.Container(
        content=ft.Row(
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
            spacing=20,
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=20,
        bgcolor=theme["container_bg_colors"],
        border_radius=ft.border_radius.all(theme["container_border_radius"]),
        border=ft.border.all(width=1, color=theme["container_border_color"]),
    )

    # Main Content Container (Empty for now)
    main_content_container = ft.Container(
        content=ft.Container(width=200,
                             height=300,
                             bgcolor="blue",),  # Empty for now
        expand=True,
        padding=20,
        bgcolor=theme["container_bg_colors"],
        border_radius=ft.border_radius.all(theme["container_border_radius"]),
        border=ft.border.all(width=1, color=theme["container_border_color"]),
    )

    # Main Layout
    main_layout = ft.Row(
        controls=[
            left_container,  # Left side (Price)
            ft.Column(
                controls=[
                    top_container,  # Top (Buttons)
                    main_content_container,  # Main Content (Empty)
                ],
                expand=True,
                spacing=20,
            ),
        ],
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
        route="/orders_screen",
        controls=[  
            ft.Container(
                content=main_container,
                expand=True,
                alignment=ft.alignment.center
            )
        ],
       
    )