from flask import render_template
from utils.utils import send_respose


from razorpay_third_party import razorpay

 
 
 
def homepage():
    order = razorpay.generate_order(9000)
    return render_template('index.html', content=order)


# POST request will be made by Razorpay
# and it won't have the csrf token.
def paymenthandler(request):
    try:
        user_details = razorpay.verify_payment(request)
        return send_respose(200, {"user_details":user_details}, "payment successful", '')
    except Exception as e:
        return  send_respose(400, {}, "payment failed", str(e))   
  

