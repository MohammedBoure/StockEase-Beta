import flet as ft
from datetime import datetime, timedelta
from database.orders import   OrderDatabase

class StatisticsScreenView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/statistics_screen")
        self.db=OrderDatabase()
       
        self.page = page
        self.page.bgcolor = "#0D0D0D"
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self.start_time = "2025-02-15 13:43:24"
        self.end_time = "2025-03-15 13:43:24"
        self.period_type = "firstperiod"
        self.s_time_text = ft.Text(f"Start Time: {self.start_time}", size=20, color="#E0E0E0", weight=ft.FontWeight.W_500)
        self.e_time_text = ft.Text(f"End Time: {self.end_time}", size=20, color="#E0E0E0", weight=ft.FontWeight.W_500)
        self.p_type_text = ft.Text(f"Period Type: {self.period_type}", size=20, color="#E0E0E0", weight=ft.FontWeight.W_500)
        
        self.orders =  [self.db.get_order_details(i[0]) for i in self.db.get_all_orders() ]
        for i in self.orders:
            print(i)
        self.sum_of_all_prices = sum([order["order_info"][2] for order in self.orders])
        self.max_order = max(self.orders, key=lambda order: order["order_info"][2], default=None)
        self.max_price = self.max_order["order_info"][2]
        self.max_customer = self.max_order["order_info"][3] if self.max_order else "not specified"
        self.main_price_bar_len = (self.page.width // 2) if self.page.width else 500
        
        self.controls = []
        self.ui_init()

    def make_button(self, text, on_click, width, height, icon=None):
        return ft.ElevatedButton(
            text=text,
            on_click=on_click,
            width=width,
            height=height,
            icon=icon,
            bgcolor="#212121",  # Dark gray for buttons
            color="#FFFFFF",    # White text
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=4,    # Subtle shadow
                overlay_color=ft.colors.with_opacity(0.1, "#FFFFFF"),
            ),
        )

    def segment_prices_by_period(self, start_time, end_time):
        try:
            start_dt = datetime.strptime(start_time, self.time_format)
            end_dt = datetime.strptime(end_time, self.time_format)
            time_range = end_dt - start_dt
            total_days = time_range.total_seconds() / (60 * 60 * 24)
            segmented_data = []

            if self.period_type and total_days>0:
                if total_days <= 1:
                    self.period_type = "hour"
                elif total_days <= 31:
                    self.period_type = "day"
                elif total_days <= 365:
                    self.period_type = "week"
                elif total_days <= 365 * 5:
                    self.period_type = "month"
                else:
                    self.period_type = "year"

                print(f"Automatically selected self.period_type: {self.period_type} for {total_days:.2f} days")
            else:
                print("the time range is negative")    

            if self.period_type == "hour":
                hour_duration = timedelta(hours=1)
                current_start = start_dt
                hour_index = 1
                while current_start < end_dt:
                    hour_end = min(current_start + hour_duration, end_dt)
                    hour_prices = []
                    for order in self.orders:
                        order_time = datetime.strptime(order["order_info"][1], self.time_format)
                        if current_start <= order_time < hour_end:
                            hour_prices.append(order["order_info"][2])
                    hour_sum = sum(hour_prices) if hour_prices else 0
                    segmented_data.append({
                        "hour": hour_index,
                        "start": current_start.strftime(self.time_format),
                        "end": hour_end.strftime(self.time_format),
                        "sum_prices": hour_sum,
                        "count": len(hour_prices)
                    })
                    current_start = hour_end
                    hour_index += 1

            elif self.period_type == "day":
                day_duration = timedelta(days=1)
                current_start = start_dt
                day_index = 1
                while current_start < end_dt:
                    day_end = min(current_start + day_duration, end_dt)
                    day_prices = []
                    for order in self.orders:
                        order_time = datetime.strptime(order["order_info"][1], self.time_format)
                        if current_start <= order_time < day_end:
                            day_prices.append(order["order_info"][2])
                    day_sum = sum(day_prices) if day_prices else 0
                    segmented_data.append({
                        "day": day_index,
                        "start": current_start.strftime(self.time_format),
                        "end": day_end.strftime(self.time_format),
                        "sum_prices": day_sum,
                        "count": len(day_prices)
                    })
                    current_start = day_end
                    day_index += 1

            elif self.period_type == "week":
                week_duration = timedelta(days=7)
                current_start = start_dt
                week_index = 1
                while current_start < end_dt:
                    week_end = min(current_start + week_duration, end_dt)
                    week_prices = []
                    for order in self.orders:
                        order_time = datetime.strptime(order["order_info"][1], self.time_format)
                        if current_start <= order_time < week_end:
                            week_prices.append(order["order_info"][2])
                    week_sum = sum(week_prices) if week_prices else 0
                    segmented_data.append({
                        "week": week_index,
                        "start": current_start.strftime(self.time_format),
                        "end": week_end.strftime(self.time_format),
                        "sum_prices": week_sum,
                        "count": len(week_prices)
                    })
                    current_start = week_end
                    week_index += 1

            elif self.period_type == "month":
                current_start = start_dt
                month_index = 1
                while current_start < end_dt:
                    next_month = current_start.month % 12 + 1
                    next_year = current_start.year + (current_start.month // 12)
                    month_end = min(datetime(next_year, next_month, 1, 0, 0, 0), end_dt)
                    month_prices = []
                    for order in self.orders:
                        order_time = datetime.strptime(order["order_info"][1], self.time_format)
                        if current_start <= order_time < month_end:
                            month_prices.append(order["order_info"][2])
                    month_sum = sum(month_prices) if month_prices else 0
                    segmented_data.append({
                        "month": f"{current_start.strftime('%B')} {current_start.year}",
                        "start": current_start.strftime(self.time_format),
                        "end": month_end.strftime(self.time_format),
                        "sum_prices": month_sum,
                        "count": len(month_prices)
                    })
                    current_start = month_end
                    month_index += 1

            elif self.period_type == "year":
                current_start = start_dt
                year_index = 1
                while current_start < end_dt:
                    next_year_start = datetime(current_start.year + 1, 1, 1, 0, 0, 0)
                    year_end = min(next_year_start, end_dt)
                    year_prices = []
                    for order in self.orders:
                        order_time = datetime.strptime(order["order_info"][1], self.time_format)
                        if current_start <= order_time < year_end:
                            year_prices.append(order["order_info"][2])
                    year_sum = sum(year_prices) if year_prices else 0
                    segmented_data.append({
                        "year": current_start.year,
                        "start": current_start.strftime(self.time_format),
                        "end": year_end.strftime(self.time_format),
                        "sum_prices": year_sum,
                        "count": len(year_prices)
                    })
                    current_start = year_end
                    year_index += 1

            print(f"Segmented data for {self.period_type}: {segmented_data}")
            return segmented_data
        except Exception as e:
            print(f"Error in segment_prices_by_period: {e}")
            return []

    def multiple_make_barrconnt(self):
        def make_barrcont(price_data):
            price = price_data["sum_prices"]
            price_bar_len = int(price / self.max_price * self.main_price_bar_len) + 3

            bar = ft.Container(
                width=price_bar_len,
                height=20,
                bgcolor="#42A5F5",  # Soft blue for bars
                border_radius=5,
                shadow=ft.BoxShadow(blur_radius=4, color="#00000040"),  # Subtle shadow
            )
            

            info_text = ft.Text(
                f"Price: {price_data['sum_prices']} | Begin: {price_data['start']} | End: {price_data['end']} | Units: {price_data['count']}",
                size=16,
                color="#E0E0E0",  # Light gray text
                weight=ft.FontWeight.W_400,
            )

            bar_unit = ft.Container(
                content=ft.Column(
                    controls=[
                        bar,
                        ft.Row(controls=[info_text,self.make_button(text="customer details",width=120,height=50,on_click= lambda e: print("customers button is clicked"))], alignment=ft.MainAxisAlignment.CENTER),
                    ],
                    spacing=8,
                ),
                padding=12,
                border=ft.border.all(1, "#424242"),  # Dark gray border
                border_radius=10,
                bgcolor="#212121",  # Dark gray background
                width=self.main_price_bar_len + 120,
                height=80,
                shadow=ft.BoxShadow(blur_radius=6, color="#00000040"),  # Subtle shadow
            )

            return bar_unit

        self.list_view.controls.clear()
        

        for i in self.segment_prices_by_period(start_time=self.start_time, end_time=self.end_time):
            full_bar_unit = make_barrcont(i)
            self.list_view.controls.append(full_bar_unit)
        self.s_time_text.value = f"Start Time: {self.start_time}"
        self.e_time_text.value = f"End Time: {self.end_time}"
        self.p_type_text.value = f"Period Type: {self.period_type}"    

        self.page.update()

    def calender_maker(self):
        start_datepicker = ft.DatePicker(first_date=datetime(2023, 10, 1), last_date=datetime(2025, 12, 31))
        start_timepicker = ft.TimePicker()
        end_datepicker = ft.DatePicker(first_date=datetime(2023, 10, 1), last_date=datetime(2025, 12, 31))
        end_timepicker = ft.TimePicker()
        
        self.page.overlay.extend([start_datepicker, start_timepicker, end_datepicker, end_timepicker])

        def change_start_date_time(e):
            try:
                date_str = (start_datepicker.value.strftime("%Y-%m-%d") if start_datepicker.value 
                            else datetime.now().strftime("%Y-%m-%d"))
                time_str = (start_timepicker.value.strftime("%H:%M:%S") if start_timepicker.value 
                            else "00:00:00")
                combined_str = f"{date_str} {time_str}"
                print(f"Start DateTime set: {combined_str}")
                
                self.start_time = combined_str
                
            except AttributeError as ae:
                print(f"Error accessing start picker value: {ae}")
            except Exception as ex:
                print(f"Unexpected error in change_start_date_time: {ex}")

        def change_end_date_time(e):
            try:
                date_str = (end_datepicker.value.strftime("%Y-%m-%d") if end_datepicker.value 
                            else datetime.now().strftime("%Y-%m-%d"))
                time_str = (end_timepicker.value.strftime("%H:%M:%S") if end_timepicker.value 
                            else "00:00:00")
                combined_str = f"{date_str} {time_str}"
                print(f"End DateTime set: {combined_str}")
                
                self.end_time = combined_str
                
            except AttributeError as ae:
                print(f"Error accessing end picker value: {ae}")
            except Exception as ex:
                print(f"Unexpected error in change_end_date_time: {ex}")

       
        calender_cont = ft.Container(
            content=ft.Column(
                controls=[
                    ft.ElevatedButton(
                        "Pick Start Date & Time",
                        icon=ft.Icons.CALENDAR_TODAY,
                        on_click=lambda e: [self.page.open(start_datepicker), self.page.open(start_timepicker)],
                        bgcolor="#424242",  # Darker gray
                        color="#FFFFFF",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            elevation=4,
                        ),
                    ),
                    ft.ElevatedButton(
                        "Pick End Date & Time",
                        icon=ft.Icons.CALENDAR_TODAY,
                        on_click=lambda e: [self.page.open(end_datepicker), self.page.open(end_timepicker)],
                        bgcolor="#424242",
                        color="#FFFFFF",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            elevation=4,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            width=260,
            border=ft.border.all(2, "#424242"),  # Dark gray border
            padding=20,
            border_radius=12,
            bgcolor="#1E1E1E",  # Very dark gray
            shadow=ft.BoxShadow(blur_radius=10, color="#00000080"),  # Soft shadow
        )

        start_datepicker.on_change = change_start_date_time
        start_timepicker.on_change = change_start_date_time
        end_datepicker.on_change = change_end_date_time
        end_timepicker.on_change = change_end_date_time

        return calender_cont

    def ui_init(self):
        a=ft.Divider()
        self.left_container_controls = ft.Column(
            controls=[
                
                ft.Text("jjjjjjjjjjjjjjjj"),
               

                self.make_button(
                    "Show Bars",
                    lambda e: self.multiple_make_barrconnt(),
                    width=250,
                    height=50,
                    icon=ft.Icons.BAR_CHART,
                ),
                self.calender_maker(),

                ft.Container(content=ft.Column(
                    controls=[
                self.s_time_text,
                ft.Divider(),
                
                self.e_time_text,
                ft.Divider(),
                self.p_type_text,
                
                ]
            
                ),
                border_radius=12,
            border=ft.border.all(2, "#424242"),
            shadow=ft.BoxShadow(blur_radius=10, color="#00000080"),
            padding=20
                
                ),
                
                
            ft.Text(f"ttttt{self.sum_of_all_prices}"),
           
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )
        self.left_container = ft.Container(
            content=self.left_container_controls,
            width=300,
            padding=20,
            bgcolor="#1E1E1E",  # Very dark gray
            border_radius=12,
            border=ft.border.all(1, "#424242"),
            shadow=ft.BoxShadow(blur_radius=10, color="#00000080"),
        )

        self.top_container = ft.Container(
            content=ft.Row(
                controls=[
                   
                    self.make_button("Dashboard", lambda e: self.page.go("/"), width=150, height=70),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=15,
            bgcolor="#1E1E1E",
            border_radius=12,
            border=ft.border.all(1, "#424242"),
            shadow=ft.BoxShadow(blur_radius=10, color="#00000080"),
        )

        self.list_view = ft.Column(
            controls=[],
            expand=True,
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
        )

        self.main_content_container = ft.Container(
            content=ft.Stack(
                [
                    ft.Container(
                        content=ft.Icon(name=ft.Icons.SHOPIFY_ROUNDED, size=600, opacity=0.05, color="#B0BEC5"),
                        alignment=ft.alignment.center,
                    ),
                    self.list_view,
                ]
            ),
            padding=20,
            bgcolor="#121212",  # Almost black
            border_radius=12,
            border=ft.border.all(1, "#424242"),
            shadow=ft.BoxShadow(blur_radius=10, color="#00000080"),
            expand=True,
        )

        self.vertical_containers = ft.Column(
            controls=[
                self.top_container,
                self.main_content_container,
            ],
            expand=True,
            spacing=15,
        )

        self.main_layout = ft.Row(
            controls=[
                self.left_container,
                self.vertical_containers,
            ],
            expand=True,
            spacing=20,
        )

        self.main_container = ft.Container(
            content=self.main_layout,
            expand=True,
            padding=20,
            bgcolor="#0D0D0D",  # Pure black background
        )

        self.controls.append(
            ft.Container(
                content=self.main_container,
                expand=True,
                alignment=ft.alignment.center,
            )
        )
        self.page.update()

  

if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "Statistics Dashboard"
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = "#0D0D0D"  # Match the black theme
        page.views.append(StatisticsScreenView(page))
        page.update()

    ft.app(target=main)