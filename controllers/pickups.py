from flask import jsonify
from cerberus import Validator
from models.orders import Orders
from models.pickups import Pickups
from flask_bcrypt import bcrypt

from schema.pickups import schema as pickup_schema

from utils.utils import send_respose
from utils.config import db_code

def generate_pickup(user_id, order_id, courier_id):
    pass
    # GET THE REQUIRED SHIPPING CHARGES DETAILS FROM DELIVERY VENDOR
    
    # DEDUCT THE AMOUNT BY ENTERING A DEBIT ENTRY INTO WALLET MODEL GET THE TRANSACTION ID FROM WALLET

    # IF DEBIT WAS SUCCESSFUL, THEN CREATE AN ENTRY IN THE PICKUP TABLE USING THE TRANSACTION ID AND ORDER ID

    # IF CREATING A PICKUP ENTRY WAS UNSUCCESSFUL, THEN DELETE THE WALLET ENTRY


def cancel_order(order_id):
    pass
    # IF THE ORDER IS COMPLETED, RETURN "order can't be cancelled"

    # CHECK IF THE ORDER IS NEW ONE, SIMPLY UPDATE THE STATUS AS CANCELLED

    # IF THE ORDER IS "ready_for_shipment", THEN CHECK ITS PICKUP STATUS, IF ORDER IS PICKED UP, THEN SIMPLY UPDATE THE STATUS IN ORDER TABLE AND PICKUP TABLE AS CANCELLED

    # IF THE STATUS IN pickups IS NOT PICKED_UP, THEN CREATE A ENTRY IN CancellationRefunds TABLE, AND UPDATE THE STATUS AS CANCELLED


def generate_invoice(pickup_id):
    pass