import win32print
import win32ui

def list_printers():
    """عرض قائمة الطابعات المتاحة"""
    printers = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)]
    if not printers:
        print("❌ لا توجد طابعات متصلة!")
        return None

    print("\n🔹 قائمة الطابعات المتاحة:")
    for i, printer in enumerate(printers):
        print(f"{i + 1}. {printer}")
    
    return printers

def choose_printer(printers):
    """يطلب من المستخدم اختيار طابعة عبر الـ Terminal"""
    while True:
        try:
            choice = int(input("\n🔷 اختر رقم الطابعة المطلوبة: ")) - 1
            if 0 <= choice < len(printers):
                return printers[choice]
            else:
                print("❌ اختيار غير صالح، حاول مجددًا.")
        except ValueError:
            print("❌ الرجاء إدخال رقم صحيح.")

def print_blank_page(printer_name):
    """طباعة صفحة بيضاء باستخدام الطابعة المختارة"""
    hprinter = win32print.OpenPrinter(printer_name)
    printer_info = win32print.GetPrinter(hprinter, 2)
    pdc = win32ui.CreateDC()
    pdc.CreatePrinterDC(printer_name)
    pdc.StartDoc("Blank Page")
    pdc.StartPage()

    pdc.Rectangle((0, 0, 800, 1100))  

    pdc.EndPage()
    pdc.EndDoc()
    pdc.DeleteDC()
    win32print.ClosePrinter(hprinter)
    print(f"\n✅ تم إرسال أمر الطباعة إلى الطابعة: {printer_name}")

printers = list_printers()
if printers:
    selected_printer = choose_printer(printers)
    print_blank_page(selected_printer)
