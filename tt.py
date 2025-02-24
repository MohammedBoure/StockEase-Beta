def calculate_ean13_check_digit(barcode: str) -> int:
    if len(barcode) != 12 or not barcode.isdigit():
        raise ValueError("يجب أن يكون الباركود 12 رقمًا")

    total = sum((3 if i % 2 else 1) * int(digit) for i, digit in enumerate(barcode))
    check_digit = (10 - (total % 10)) % 10  # للحصول على رقم بين 0 و 9
    return check_digit

# تجربة الحساب
barcode = "613250154553"  # 12 رقمًا بدون رقم التحقق
check_digit = calculate_ean13_check_digit(barcode)
print(f"رقم التحقق: {check_digit}")  # يجب أن يكون 1