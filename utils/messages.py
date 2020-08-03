"""
contains all constant messages
which can be used in views
"""
METHOD_NOT_ALLOWED = "Method Not Allowed!"
BAD_REQUEST = "Bad Request!"
JWT_REQUIRED = "JWT Token required!"
INVALID_TOKEN = "Invalid JWT Token!"
TOKEN_EXPIRED = "Token Expired!"
EMAIL_ALREADY_EXISTS = "Email already Registered!"
MEC_CODE_ALREADY_EXISTS = "Mechanic Code already exists!"
MEC_CREATED = "Mechanic created with email: {}"
NO_OF_REPEATS_EXCEEDED = "Number of repeats should not exceed 100!"
ERROR_UPLOADING_FILE = "Error Uploading File!"
PRODUCT_SAVED = "Product saved with id {}"
INSUFFICIENT_BALANCE = "Insufficient Balance. Please apply coupons to get more balance!"
ORDER_CREATED = "Order sent successfully."
ORDER_ALREADY_RETURNED = "This order is already requested for returning!"
ORDER_RETURNING = "Please use the following QR code to return your order to a UPS store!"
COUPON_ALREADY_APPLIED = "This coupon code is already claimed by you!! Please try with another coupon code"
COUPON_APPLIED = "Coupon successfully applied!"
RESTRICTED = "You are not allowed to access this resource!"
INVALID_STATUS = "the value of 'status' has to be 'delivered','return pending' or 'returned'"

QR_CODE_URL = "https://storage.cloud.google.com/traceable/qr_code/return-qr-code.png"
