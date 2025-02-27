import flet as ft
from utils.file_utils import theme, font_size, language

def dashboard(page: ft.Page):
    lng = language["dashboard"]

    def end_window(e):
        page.window.minimized = True
        page.window.skip_task_bar = True
        page.window.destroy()

    def create_button(text, route):
        return ft.ElevatedButton(
            text,
            width=250,
            height=200,
            on_click=lambda e: navigate_to_page(route),
            bgcolor=theme["button_bg_color"],
            color=theme["button_text_color"],
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=theme["button_border_radius"]),
                side=ft.BorderSide(width=theme["button_border_width"], color=theme["button_text_color"]),
                text_style=ft.TextStyle(size=font_size["subtitle"]),
                overlay_color=theme["button_overlay_color"]
            )
        )

    def navigate_to_page(route):
        print(f"تم النقر على {route}")
        page.go(route)

    buttons = [
        create_button(lng["buttons"]["Product"], "/product_screen"),
        create_button(lng["buttons"]["Orders"], "/orders_screen"),
        create_button(lng["buttons"]["Customers"], "/customers_screen"),
        create_button(lng["buttons"]["Statistics"], "/statistics_screen"),
    ]

    interface_buttons = ft.ResponsiveRow(
        controls=[ft.Container(b, col={"sm": 6, "md": 4, "lg": 3}) for b in buttons],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        run_spacing=20,
        expand=True
    )

    main_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text(lng["head"]["Dashboard"], 
                             size=font_size["title"], 
                             weight="bold", 
                             color=theme["text_color"]),
                padding=20,
                alignment=ft.alignment.center
            ),
            
            ft.Divider(height=10, color=theme["text_color"]),
            
            ft.Container(
                content=interface_buttons,
                expand=True,
                alignment=ft.alignment.center,
                padding=20
            )
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    control_icons = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.SETTINGS,
                    icon_size=30,
                    tooltip=lng["buttons"]["Settings"],
                    icon_color=theme["button_text_color"],
                    on_click=lambda e:page.go("/settings_screen")
                ),
                ft.IconButton(
                    icon=ft.Icons.EXIT_TO_APP,
                    icon_size=30,
                    tooltip=lng["buttons"]["exit"],
                    icon_color=theme["button_text_color"],
                    on_click=end_window
                ),
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=20
        ),
        padding=ft.padding.all(20)
    )

    main_container = ft.Column(
        controls=[
            main_content,
            control_icons
        ],
        expand=True,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.View(
        route="/",
        controls=[
            ft.Container(
                content=main_container,
                expand=True,
                bgcolor=theme["background_colors"],
                padding=theme["container_padding"],
                border=ft.border.all(
                    width=theme["container_border_radius"],
                    color=theme["container_border_color"]
                ),
                border_radius=ft.border_radius.all(theme["container_border_radius"])
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )