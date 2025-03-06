import flet as ft
from utils.shared import theme, font_size


def navigate_to_page(route,page):
        page.go(route)

def create_button(text, route,page):
        return ft.ElevatedButton(
            text,
            width=250,
            height=200,
            on_click=lambda e: navigate_to_page(route,page),
            bgcolor=theme["button_bg_color"],
            color=theme["button_text_color"],
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=theme["button_border_radius"]),
                side=ft.BorderSide(width=theme["button_border_width"], color=theme["button_text_color"]),
                text_style=ft.TextStyle(size=font_size["subtitle"]),
                overlay_color=theme["button_overlay_color"]
            )
        )