import flet as ft

# Minimal mock data to replace utils.shared dependencies
mock_theme = {
    "border_color": "grey",
    "container_bg_colors": "white",
    "container_border_color": "grey",
    "container_border_radius": 10,
    "background_colors": "lightgrey",
    "button_bg_color": "blue",
    "button_text_color": "white",
}
mock_font_size = {"label": 16}
mock_language = {
    "statistics": {
        "left_container": {
            "search_label": "Search",
            "Add_Product": {"Add_Product": "Add Product"},
            "Edit_Product": {"Edit_Product": "Edit Product"},
            "Delete_Product": {"Delete_Product": "Delete Product"},
            "Out_of_stock_products": "Out of Stock",
        },
        "top_container": {
            "Product": "Products",
            "Orders": "Orders",
            "Customers": "Customers",
            "Dashboard": "Dashboard",
        },
    }
}

class StatisticsScreenView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/statistics_screen")
        self.page = page
        self.lng = mock_language["statistics"]
        self.controls = []
        self.ui_init()

    def make_button(self, text, on_click, width, height, icon=None):
        return ft.ElevatedButton(
            text=text,
            on_click=on_click,
            width=width,
            height=height,
            icon=icon,
            bgcolor=mock_theme["button_bg_color"],
            color=mock_theme["button_text_color"],
        )

    def open_dlg_add(self, e):
        self.page.add(ft.Text("Add Product Clicked"))
        self.page.update()

    def open_dlg_update(self, e):
        self.page.add(ft.Text("Edit Product Clicked"))
        self.page.update()

    def open_dlg_delete(self, e):
        self.page.add(ft.Text("Delete Product Clicked"))
        self.page.update()

    def Out_of_stock_products(self, e):
        self.page.add(ft.Text("Out of Stock Clicked"))
        self.page.update()

    def reset_table(self):
        self.page.add(ft.Text("Table Reset"))
        self.page.update()

    def handle_scroll(self, e):
        pass

    def ui_init(self):
        self.search_label = ft.Text(self.lng["left_container"]["search_label"], size=mock_font_size["label"])

        self.table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("Stat"))],
            rows=[ft.DataRow(cells=[ft.DataCell(ft.Text("Test Data"))])],
        )

        self.left_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Divider(height=1, color=mock_theme["border_color"]),
                    self.search_label,
                    ft.Divider(height=1, color=mock_theme["border_color"]),
                    self.make_button(
                        self.lng["left_container"]["Add_Product"]["Add_Product"],
                        lambda e: self.open_dlg_add(e),
                        width=250,
                        height=50,
                        icon=ft.Icons.ADD_CIRCLE_OUTLINED
                    ),
                    self.make_button(
                        self.lng["left_container"]["Edit_Product"]["Edit_Product"],
                        lambda e: self.open_dlg_update(e),
                        width=250,
                        height=50,
                        icon=ft.Icons.EDIT
                    ),
                    self.make_button(
                        self.lng["left_container"]["Delete_Product"]["Delete_Product"],
                        lambda e: self.open_dlg_delete(e),
                        width=250,
                        height=50,
                        icon=ft.Icons.DELETE
                    ),
                    ft.Divider(height=1, color=mock_theme["border_color"]),
                    self.make_button(
                        self.lng["left_container"]["Out_of_stock_products"],
                        lambda e: self.Out_of_stock_products(e),
                        width=250,
                        height=50,
                        icon=ft.Icons.SHOPPING_BASKET_OUTLINED
                    ),
                ],
                horizontal_alignment="center",
            ),
            width=300,
            padding=20,
            bgcolor=mock_theme["container_bg_colors"],
            border_radius=ft.border_radius.all(mock_theme["container_border_radius"]),
            border=ft.border.all(width=1, color=mock_theme["container_border_color"]),
        )

        self.top_container = ft.Container(
            content=ft.Row(
                controls=[
                    self.make_button(self.lng["top_container"]["Product"], lambda e: self.reset_table(), width=150, height=70),
                    self.make_button(self.lng["top_container"]["Orders"], lambda e: self.page.go("/orders_screen"), width=150, height=70),
                    self.make_button(self.lng["top_container"]["Customers"], lambda e: self.page.go("/customers_screen"), width=150, height=70),
                    self.make_button(self.lng["top_container"]["Dashboard"], lambda e: self.page.go("/"), width=150, height=70),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=10,
            bgcolor=mock_theme["container_bg_colors"],
            border_radius=ft.border_radius.all(mock_theme["container_border_radius"]),
            border=ft.border.all(width=1, color=mock_theme["container_border_color"]),
        )

        self.list_view = ft.ListView(
            controls=[self.table],
            expand=True,
            spacing=10,
            auto_scroll=False,
            on_scroll=lambda e: self.handle_scroll(e),
        )

        self.main_content_container = ft.Container(
            content=ft.Stack(
                [
                    ft.Container(
                        content=ft.Icon(name=ft.Icons.SHOPIFY_ROUNDED, size=600, opacity=0.3, color="grey"),
                        alignment=ft.alignment.center,
                    ),
                    self.list_view,
                ]
            ),
            padding=20,
            bgcolor=mock_theme["container_bg_colors"],
            border_radius=ft.border_radius.all(mock_theme["container_border_radius"]),
            border=ft.border.all(width=1, color=mock_theme["container_border_color"]),
            expand=True,
        )

        self.vertical_containers = ft.Column(
            controls=[
                self.top_container,
                self.main_content_container
            ],
            expand=True,
        )

        self.main_layout = ft.Row(
            controls=[
                self.left_container,
                self.vertical_containers
            ],
            expand=True,
            spacing=20,
        )

        self.main_container = ft.Container(
            content=self.main_layout,
            expand=True,
            padding=20,
            bgcolor=mock_theme["background_colors"],
        )

        self.controls.append(
            ft.Container(
                content=self.main_container,
                expand=True,
                alignment=ft.alignment.center
            )
        )

def main(page: ft.Page):
    page.title = "Test App"
    page.theme_mode = ft.ThemeMode.LIGHT

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.ElevatedButton(
                            "Go to Statistics",
                            on_click=lambda e: page.go("/statistics_screen"),
                            bgcolor="blue",
                            color="white",
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )
        elif page.route == "/statistics_screen":
            page.views.append(StatisticsScreenView(page))
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)