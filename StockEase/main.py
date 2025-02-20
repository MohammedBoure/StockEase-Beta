import flet as ft
from ui.dashboard import  dashboard,dashboard_login


theme = "light" #مؤقتا

def main(page: ft.Page):
    page.title = "STOCKEASE-BETA"
    page.window.width = 1000
    page.window.height = 800
    page.window.top = 3
    page.window.left = 600
    
    page.theme_mode = ft.ThemeMode.LIGHT if theme == "light" else ft.ThemeMode.DARK


    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(dashboard(page))
        page.update()

    page.on_route_change = route_change
    
    page.go("/")

ft.app(target=main)