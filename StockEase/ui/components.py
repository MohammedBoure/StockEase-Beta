import flet as ft
from utils.shared import theme, font_size

def make_button(text, on_click, width, height):
    """
    Creates a styled button with specified text, on_click handler, width, and height.
        
    Args:
        text (str): Button text.
        on_click (callable): Function to call on button click.
        width (int): Button width.
        height (int): Button height.
            
    Returns:
        ft.ElevatedButton: Styled button.
    """
    return ft.ElevatedButton(
        width=width,
        height=height,
        text=text,
        on_click=on_click,
        bgcolor=theme["button_bg_color"],
        color=theme["button_text_color"],
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=theme["button_border_radius"]),
            overlay_color=theme["button_overlay_color"],
        )
    )
        
def button(title, on_click):
    """
    Creates and returns a text button with the specified title and click handler.
    Used for column headers in the product table.
    """
    return ft.TextButton(
        title,
        on_click=on_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0),
            padding=ft.padding.all(5),
            color=theme["button_text_color"]
        )
    )
