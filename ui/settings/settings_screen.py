import flet as ft
import os
import sys
from utils.shared import theme, font_size, language, settings
from utils.file_utils import write_json


class SettingsCategory:
    def __init__(self, title: str, icon: str, controls: list):
        self.title = title
        self.icon = icon
        self.controls = controls

class SettingsScreenView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/settings_screen")
        self.page = page
        self.lng = language["settings"]

        self.header_controls = ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="رجوع",
                    icon=ft.Icon(name=ft.Icons.ARROW_BACK, size=20),
                    on_click=lambda e: self.page.go("/"),
                    tooltip="رجوع إلى الشاشة الرئيسية",
                    bgcolor=theme.get("icon_button_bg_color", "#424242"),
                    color=theme.get("icon_button_icon_color", "#FFFFFF"),
                    elevation=5,
                    style=ft.ButtonStyle(
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    ),
                    on_hover=self.on_hover,
                ),
                ft.ElevatedButton(
                    text="حفظ",
                    icon=ft.Icon(name=ft.Icons.SAVE, size=20),
                    on_click=lambda e: self.save_settings(),  # استدعاء الدالة الجديدة
                    tooltip="حفظ الإعدادات",
                    bgcolor=theme.get("icon_button_bg_color", "#424242"),
                    color=theme.get("icon_button_icon_color", "#FFFFFF"),
                    elevation=5,
                    style=ft.ButtonStyle(
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    ),
                    on_hover=self.on_hover,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=0
        )

        self.language_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option(key="ar", text="العربية"),
                ft.dropdown.Option(key="en", text="English"),
                ft.dropdown.Option(key="fr", text="Français"),
            ],
            value=settings.get("language", "ar"),
            width=200,
            tooltip="اختر اللغة المفضلة",
            on_change=self.on_language_change
        )
        self.theme_color_picker = ft.Dropdown(
            options=[
                ft.dropdown.Option(key="dark", text="dark"),
                ft.dropdown.Option(key="light", text="light"),
            ],
            value=settings.get("theme", "light"),
            width=200,
            tooltip="اختر لون الثيم",
            on_change=self.on_theme_change
        )
        self.font_size_slider = ft.Slider(
            min=10,
            max=24,
            value=settings.get("font_size", 12),
            label="{value}pt",
            tooltip="اضبط حجم الخط"
        )


        # فئات الإعدادات مع أيقونات صحيحة
        self.categories = [
            SettingsCategory("الإعدادات العامة", ft.Icons.SETTINGS, [
                self.create_setting_item("اللغة", self.language_dropdown),
                self.create_setting_item("لون الثيم", self.theme_color_picker),
                self.create_setting_item("حجم الخط", self.font_size_slider),
            ])
        ]

        # التبويبات
        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text=category.title,
                    icon=category.icon,
                    content=ft.Container(
                        content=ft.Column(controls=category.controls, spacing=15),
                        padding=10
                    )
                ) for category in self.categories
            ],
            expand=1
        )

        # التخطيط الرئيسي
        main_column = ft.Column(
            controls=[self.header_controls, self.tabs],
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE
        )
        self.controls = [ft.Container(content=main_column, padding=10, expand=True)]
        
        
    def on_language_change(self,e):
        settings["language"] = self.language_dropdown.value
        write_json(settings,"config/settings.json")
    def on_theme_change(self,e):
        settings["theme"] = self.theme_color_picker.value
        write_json(settings,"config/settings.json")
    
    def create_setting_item(self, label: str, control: ft.Control):
        """إنشاء عنصر إعداد موحد"""
        return ft.Row(
            controls=[
                ft.Text(label, width=150, size=16),
                control
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def on_hover(self, e):
        """تأثير التمرير فوق الزر"""
        e.control.bgcolor = theme.get("hover_color", "#D3D3D3") if e.data == "true" else theme.get("icon_button_bg_color", "#424242")
        e.control.update()

    def save_settings(self):
        """حفظ الإعدادات وإعادة تشغيل التطبيق"""
        try:
            if self.page.route:
                pass
        except:
            return
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def create_backup(self, e):
        """إنشاء نسخة احتياطية (افتراضي)"""
        self.page.snack_bar = ft.SnackBar(ft.Text("تم بدء النسخ الاحتياطي!"), open=True)
        self.page.update()


if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "إعدادات"
        page.add(SettingsScreenView(page))
    ft.app(target=main)