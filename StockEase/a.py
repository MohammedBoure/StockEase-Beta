import flet as ft

def main(page: ft.Page):
    def create_editable_text(initial_text):
        text_field = ft.TextField(
            value=initial_text,
            visible=False,
            autofocus=True,
            on_submit=lambda e: save_changes(e, text_field, text_display)
        )
        text_display = ft.Text(initial_text)
        
        gesture = ft.GestureDetector(
            content=text_display,
            on_long_press=lambda e: toggle_edit(text_field, text_display)
        )

        return ft.Row(
            controls=[
                ft.Container(
                    content=gesture,
                    visible=True,
                    padding=5,
                    border=ft.border.all(1, "blue"),
                    border_radius=5
                ),
                ft.Container(
                    content=text_field,
                    visible=False,
                    padding=5,
                    border=ft.border.all(1, "green"),
                    border_radius=5
                )
            ]
        )

    def toggle_edit(text_field, text_display):
        text_field.value = text_display.value
        text_display.container.visible = False
        text_field.container.visible = True
        text_field.focus()
        page.update()

    def save_changes(e, text_field, text_display):
        text_display.value = text_field.value
        text_field.container.visible = False
        text_display.container.visible = True
        page.update()

    # إضافة العناصر للصفحة
    page.add(
        create_editable_text("اضغط مطولاً لتعديل النص"),
        create_editable_text("نص آخر قابل للتعديل")
    )

ft.app(target=main)