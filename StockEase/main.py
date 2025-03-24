import flet as ft
from ui.dashboard.dashboard import  dashboard
from ui.product.product_screen import ProductScreenView
from ui.orders.orders_screen import OrdersScreen
from ui.settings.settings_screen import SettingsScreenView
from ui.statistics.statistics_screen import StatisticsScreenView
from utils.shared import settings


theme = settings["theme"]

def main(page: ft.Page):
    page.title = "STOCKEASE-BETA"
    page.window.width = 1000
    page.window.height = 800
    page.window.top = 3
    page.window.left = 600
    
    page.window.full_screen = True
    
    page.theme_mode = ft.ThemeMode.LIGHT if theme == "dark" else ft.ThemeMode.DARK


    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(dashboard(page))
        elif page.route=="/product_screen":
            page.views.append(ProductScreenView(page))
        elif page.route=="/customers_screen":
            page.views.append(ProductScreenView(page))
        elif page.route=="/orders_screen":
            page.views.append(OrdersScreen(page))     
        elif page.route=="/settings_screen":
            page.views.append(SettingsScreenView(page))     
        elif page.route=="/statistics_screen":
            page.views.append(StatisticsScreenView(page))           
        page.update()

    page.on_route_change = route_change
    
    page.go("/")

ft.app(target=main)