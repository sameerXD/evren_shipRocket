import razorpay
from utils.utils import send_respose
import os
# razorpay instance
razorpay_client = razorpay.Client(
    auth=(os.environ.get('RAZOR_KEY_ID'), os.environ.get('RAZOR_KEY_SECRET')))


def generate_order(amount):
    currency = 'INR'
    amount = amount  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = os.environ.get('RAZOR_KEY_ID')
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    return context


def verify_payment(request, amount):
        try:
           
            # get the required parameters from post request.
            payment_id = request['razorpay_payment_id']
            razorpay_order_id = request['razorpay_order_id']
            signature = request['razorpay_signature']
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            razorpay_client.utility.verify_payment_signature(
                params_dict)

            resp= razorpay_client.payment.fetch(payment_id)
            pay_det = {x: resp[x] for x in resp.keys()}
            
            # print("resp ",pay_det)
            # razorpay_client.payment.capture(payment_id, amount)
            
            return pay_det
        except Exception as e:
            # if we don't find the required parameters in POST data
            raise ValueError(str(e)) 
 