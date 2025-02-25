def calculate_ean13_check_digit(barcode: str) -> int:
    if len(barcode) != 12 or not barcode.isdigit():
        raise ValueError("يجب أن يكون الباركود 12 رقمًا")

    total = sum((3 if i % 2 else 1) * int(digit) for i, digit in enumerate(barcode))
    check_digit = (10 - (total % 10)) % 10 
    return check_digit

barcode = "569745801145" 
check_digit = calculate_ean13_check_digit(barcode)
print(f"رقم التحقق: {check_digit}")
