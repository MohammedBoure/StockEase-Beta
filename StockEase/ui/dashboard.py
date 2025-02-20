import flet as ft
from utils.file_utils import theme,font_size

def dashboard(page):
    return ft.View(
        route="/login",
        controls=[  
            ft.Container(
                content=ft.Text("Dashboard", size=font_size["title"]),
                expand=True,
                alignment=ft.alignment.center
            )
        ],
        bgcolor=theme["background_colors"][0]
    )


def dashboard_login(page):
    return ft.View(
        route="/login",
        controls=[  
            ft.Container(
                content=ft.Text("Login", size=font_size["title"]),
                expand=True,
                alignment=ft.alignment.center
            )
        ],
        bgcolor=theme["background_colors"][0]
    )