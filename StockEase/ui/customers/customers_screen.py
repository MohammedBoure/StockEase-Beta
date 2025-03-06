import flet as ft
from utils.shared import theme, font_size, language 

def product_screen(page):

    return ft.View(
        route="/customers_screen",
        controls=[  
            ft.Container(
                content=ft.Text("customers screen is empty", size=font_size["title"]),
                expand=True,
                alignment=ft.alignment.center
            )
        ],
        bgcolor=theme["background_colors"][0]
    )