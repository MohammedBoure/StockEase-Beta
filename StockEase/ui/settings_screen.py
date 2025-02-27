import flet as ft
from utils.file_utils import theme, font_size, language, settings, write_json
import os
import sys


class SettingsScreenView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/settings_screen")
        self.page = page
        self.lng = language["settings"]
        
        # Create header buttons
        header_controls = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda e: self.page.go("/"),
                    icon_size=30,
                    tooltip="رجوع",
                    bgcolor=theme["icon_button_bg_color"],
                    icon_color=theme["icon_button_icon_color"],
                    style=ft.ButtonStyle(
                        overlay_color=theme["icon_button_overlay_color"],
                        shape=ft.RoundedRectangleBorder(radius=theme["icon_button_border_radius"]),
                    ),
                ),
                ft.IconButton(
                    icon=ft.Icons.SAVE,
                    on_click=lambda e: self.save_settings(),
                    icon_size=30,
                    tooltip="حفظ الإعدادات",
                    bgcolor=theme["icon_button_bg_color"],
                    icon_color=theme["icon_button_icon_color"],
                    style=ft.ButtonStyle(
                        overlay_color=theme["icon_button_overlay_color"],
                        shape=ft.RoundedRectangleBorder(radius=theme["icon_button_border_radius"]),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=40
        )

        general_settings = self.create_settings_container(
            title=self.lng["generals_settings"]["title"],
            
            controls=[
                self.create_setting_item(self.lng["generals_settings"]["language"], self.create_language_dropdown()),
                self.create_setting_item(self.lng["generals_settings"]["theme"], self.create_theme_dropdown()),
            ]
        )

        printing_settings = self.create_settings_container(
            title=self.lng["printing_settings"]["title"],
            controls=[
                self.create_setting_item(self.lng["printing_settings"]["Font_size"], ft.Slider(min=10, max=24, divisions=14, label="{value}pt")),
                self.create_setting_item(self.lng["printing_settings"]["Paper_type"], ft.Dropdown(options=[
                    ft.dropdown.Option("A4"),
                    ft.dropdown.Option("A5"),
                    ft.dropdown.Option("Letter"),
                ])),
            ]
        )

        database_settings = self.create_settings_container(
            title=self.lng["database_settings"]["title"],
            controls=[
                self.create_setting_item(self.lng["database_settings"]["User_name"], ft.TextField(
                    border_color=theme["input_border_color"],
                    bgcolor=theme["input_fill_color"],
                    cursor_color=theme["input_cursor_color"],
                    selection_color=theme["input_selection_color"],
                    focused_border_color=theme["input_focused_border_color"],
                )),
                self.create_setting_item(self.lng["database_settings"]["Password"], ft.TextField(
                    password=True,
                    border_color=theme["input_border_color"],
                    bgcolor=theme["input_fill_color"],
                    cursor_color=theme["input_cursor_color"],
                    selection_color=theme["input_selection_color"],
                    focused_border_color=theme["input_focused_border_color"],
                )),
            ]
        )

        backup_settings = self.create_settings_container(
            title=self.lng["backup_settings"]["title"],
            controls=[
                self.create_setting_item(self.lng["backup_settings"]["save_path"], ft.TextField(
                    border_color=theme["input_border_color"],
                    bgcolor=theme["input_fill_color"],
                    cursor_color=theme["input_cursor_color"],
                    selection_color=theme["input_selection_color"],
                    focused_border_color=theme["input_focused_border_color"],
                )),
                ft.ElevatedButton(
                    self.lng["backup_settings"]["create_a_version_now"],
                    icon=ft.Icons.BACKUP,
                    bgcolor=theme["button_bg_color"],
                    color=theme["button_text_color"],
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=theme["button_border_radius"]),
                        overlay_color=theme["button_overlay_color"],
                    ),
                ),
            ]
        )

        # Main layout
        main_column = ft.Column(
            controls=[
                header_controls,
                general_settings,
                printing_settings,
                database_settings,
                backup_settings
            ],
            spacing=25,
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE
        )

        self.controls.append(
            ft.Container(
                content=main_column,
                padding=theme["container_padding"],
                expand=True,
                bgcolor=theme["background_colors"],
            )
        )

    def create_settings_container(self, title: str, controls: list):
        """Creates a uniform settings container"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=theme["text_color"]),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=10, color=theme["container_border_color"]),
                    *controls
                ],
                spacing=15
            ),
            padding=theme["container_padding"],
            bgcolor=theme["container_bg_colors"],
            border_radius=theme["container_border_radius"],
            border=ft.border.all(theme["container_border"], theme["container_border_color"]),
            shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.BLACK12)
        )

    def create_setting_item(self, label: str, control: ft.Control):
        """Creates a uniform setting row"""
        return ft.Row(
            controls=[
                ft.Text(label, width=150, size=16, color=theme["text_color"]),
                control
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

    def create_language_dropdown(self):
        """Creates language dropdown with current selection"""
        return ft.Dropdown(
            options=[
                ft.dropdown.Option("ar"),
                ft.dropdown.Option("en"),
                ft.dropdown.Option("fr"),
            ],
            value=settings["language"],
            width=200,
            content_padding=10,
            border_color=theme["input_border_color"],
            bgcolor=theme["input_fill_color"],
            focused_border_color=theme["input_focused_border_color"],
            on_change=self.change_language
        )

    def create_theme_dropdown(self):
        if settings["theme"] == "dark":
            tm = self.lng["generals_settings"]["dark"]
        elif settings["theme"] == "light":
            tm = self.lng["generals_settings"]["light"]
        """Creates theme dropdown with current selection"""
        return ft.Dropdown(
            options=[
                ft.dropdown.Option(self.lng["generals_settings"]["light"]),
                ft.dropdown.Option(self.lng["generals_settings"]["dark"]),
            ],
            value=tm,
            width=200,
            content_padding=10,
            border_color=theme["input_border_color"],
            bgcolor=theme["input_fill_color"],
            focused_border_color=theme["input_focused_border_color"],
            on_change=self.change_theme
        )

    def save_settings(self):
        try:
            if self.page.route:
                pass
        except:
            return        
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def change_language(self, e):
        settings["language"] = e.control.value
        write_json(settings,"config/settings.json")

    def change_theme(self, e):
        if e.control.value == self.lng["generals_settings"]["light"]:
            settings["theme"] = "light"
        elif e.control.value == self.lng["generals_settings"]["dark"]:
            settings["theme"] = "dark"
            
        write_json(settings,"config/settings.json")
        