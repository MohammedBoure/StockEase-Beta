import flet as ft
from utils.file_utils import theme,font_size

def product_screen(page):


    
    return ft.View(
        route="/product_screen",
        controls=[  
            ft.Container(
                content=ft.Text("product screen is empty", size=font_size["title"]),
                expand=True,
                alignment=ft.alignment.center
            )
        ],
        bgcolor=theme["background_colors"][0]
    )
