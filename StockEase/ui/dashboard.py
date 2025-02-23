import flet as ft
from utils.file_utils import theme, font_size

def dashboard(page: ft.Page):
    # Interface buttons
    interface_buttons = ft.Row(
        controls=[
            ft.ElevatedButton(
                "📦 Product",
                width=250,
                height=200,
                on_click=lambda e: page.go("/product_screen"),

                bgcolor=theme["button_bg_color"],

                color=theme["button_text_color"],
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=theme["button_border_radius"]),
                    side=ft.BorderSide(width=theme["button_border_width"], color=theme["button_text_color"]),
                    text_style=ft.TextStyle(size=font_size["subtitle"]),
                    overlay_color=theme["button_overlay_color"]
                )
            ),
            ft.ElevatedButton(
                "📑 Orders",
                width=250,
                height=200,
                on_click=lambda e: page.go("/orders_screen"),
                bgcolor=theme["button_bg_color"],
                color=theme["button_text_color"],
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=theme["button_border_radius"]),
                    side=ft.BorderSide(width=theme["button_border_width"], color=theme["button_text_color"]),
                    text_style=ft.TextStyle(size=font_size["subtitle"]),
                    overlay_color=theme["button_overlay_color"]
                )
            ),
            ft.ElevatedButton(
                "👨🏼‍🤝‍👨🏼 Customers",
                width=250,
                height=200,
                on_click=lambda e: page.go("/customers_screen"),
                bgcolor=theme["button_bg_color"],
                color=theme["button_text_color"],
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=theme["button_border_radius"]),
                    side=ft.BorderSide(width=theme["button_border_width"], color=theme["button_text_color"]),
                    text_style=ft.TextStyle(size=font_size["subtitle"]),
                    overlay_color=theme["button_overlay_color"]
                )
            ),
        ],
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Main content container
    main_content = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                content=ft.Text("📊 Dashboard", 
                             size=font_size["title"], 
                             weight="bold", 
                             color=theme["text_color0"]),
                padding=20
            ),
            ft.Divider(height=10, color=theme["text_color0"]),
            ft.Container(
                content=interface_buttons,
                expand=True,
                alignment=ft.alignment.center,
                padding=20
            )
        ],
        expand=True
    )

    # Main container with styling
    main_container = ft.Container(
        content=main_content,
        expand=True,
        bgcolor=theme["background_colors"],
        padding=theme["container_padding"],
        border=ft.border.all(
            width=theme["container_border_radius"],
            color=theme["container_border_color"]
        ),
        border_radius=ft.border_radius.all(theme["container_border_radius"])
    )

    return ft.View(
        route="/",
        controls=[main_container],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )