from escpos.printer import Usb
from escpos import printer

def find_connected_printers():
    """Find all connected USB printers"""
    printers = []
    try:
        # Search for USB devices
        devices = Usb.find_usb_devices()
        for device in devices:
            vendor_id = device['vendor_id']
            product_id = device['product_id']
            printers.append({
                'vendor_id': vendor_id,
                'product_id': product_id,
                'device': device
            })
            print(f"Found printer: Vendor ID={hex(vendor_id)}, Product ID={hex(product_id)}")
    except Exception as e:
        print("Error finding printers:", e)
    return printers

def select_printer(printers, vendor_id, product_id):
    """Select a specific printer from the list"""
    for printer in printers:
        if printer['vendor_id'] == vendor_id and printer['product_id'] == product_id:
            return printer
    return None

def print_receipt(printer, items, tax_rate=0.10):
    """Print a receipt on the selected printer"""
    try:
        # Initialize the printer
        p = Usb(printer['vendor_id'], printer['product_id'], in_ep=0x81, out_ep=0x03)

        # Header
        p.set(align='center', text_type='B')
        p.text("\nMy Shop Name\n")
        p.text("123 Business Street\n")
        p.text("Tax ID: 123-456-789\n\n")
        p.set(align='left', text_type='normal')

        # Items header
        p.text("-" * 32 + "\n")
        p.text(f"{'Item':<20}{'Qty':>5}{'Price':>7}\n")
        p.text("-" * 32 + "\n")

        # Items list
        subtotal = 0
        for item in items:
            name = item['name'][:20]  # Truncate long names
            qty = item['qty']
            price = item['price']
            total = qty * price
            subtotal += total
            p.text(f"{name:<20}{qty:>5}{price:>7.2f}\n")

        # Totals
        p.text("-" * 32 + "\n")
        tax = subtotal * tax_rate
        grand_total = subtotal + tax
        p.set(align='right')
        p.text(f"Subtotal: {subtotal:.2f}\n")
        p.text(f"Tax ({tax_rate*100}%): {tax:.2f}\n")
        p.text(f"Total: {grand_total:.2f}\n")
        p.set(align='left')

        # Footer
        p.text("\n" * 2)
        p.set(align='center')
        p.text("Thank you for shopping!\n")
        p.text("www.myshop.com\n")

        # Cut paper
        p.cut()

    except Exception as e:
        print("Printer Error:", e)

# Example usage
if __name__ == "__main__":
    # Find all connected printers
    printers = find_connected_printers()

    if not printers:
        print("No printers found.")
    else:
        # Print details of connected printers
        for i, printer in enumerate(printers):
            print(f"Printer {i + 1}: Vendor ID={hex(printer['vendor_id'])}, Product ID={hex(printer['product_id'])}")

        # Select a printer (e.g., the first one)
        selected_printer = printers[0]  # Change this to select a different printer
        print(f"Selected printer: Vendor ID={hex(selected_printer['vendor_id'])}, Product ID={hex(selected_printer['product_id'])}")

        # Define items for the receipt
        items = [
            {'name': 'Product 1', 'qty': 2, 'price': 15.50},
            {'name': 'Another Item', 'qty': 1, 'price': 30.00},
            {'name': 'Long Product Name Example', 'qty': 3, 'price': 5.25}
        ]

        # Print the receipt on the selected printer
        print_receipt(selected_printer, items)