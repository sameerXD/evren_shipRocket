from flask import jsonify
from cerberus import Validator
from models.orders import Orders
from models.buyers import Buyers
from models.products import Products_Details
from flask_bcrypt import bcrypt

from schema.orders import schema as orders_schema
from schema.product import schema as product_schema
from schema.buyer import schema as buyer_schema

from utils.utils import send_respose

def create_order(data):
    v1 = Validator(buyer_schema)
    v2 = Validator(orders_schema)
    v3 = Validator(product_schema)

    # FIRST VALIDATE THE SCHEMA AND ADD THE BUYER
    if v1.validate(data["buyer"]):
        buyer = Buyers(**data["buyer"])
        # TRY TO ADD THE BUYER IN DB, IF FAILED RETURN ERROR
        try:
            buyer.add_buyer()
        except:
            return send_respose(402, {},"","Error in adding buyer!!")

        if buyer:
            data["buyer_id"] = buyer.id

            # NOW VALIDATE ORDERS DATA, ADD IT, IF UNSUCESSFUL REMOVE THE BUYER DATA AND RETURN
            if v2.validate(data):
                new_order = Orders(**data)
                try:
                    new_order.save_order()
                except:
                    Buyers.delete(buyer.id)
                    return send_respose(402, {},"","Error in creating order!!")

                # ADD ALL THE PRODUCTS ONE BY ONE, BUT COMMIT AT THE LAST, IF UNSUCESSFUL IN ADDING ANY PRODUCT --> DELETE BUYER, ORDER, ROLLBACK THE ADDED PRODUCTS AND RETURN ERROR
                if new_order:
                    data["order_id"] = new_order.id

                    for i in range(1,data["number_of_products"]+1):
                        if v3.validate(data["products"][str(i)]):
                            product = Products_Details(data["order_id"], **data["products"][str(i)])
                            
                            if product:
                                product.add_product()

                            else:
                                Buyers.delete(buyer.id)
                                Orders.delete(new_order.id)
                                Products_Details.rollback()
                                return send_respose(401,{},"",f"Error in adding product{str(i)}")
                        
                        else:
                            Buyers.delete(buyer.id)
                            Orders.delete(new_order.id)
                            return send_respose(402,{},"",f"Product{str(i)} Validation Failed")
                        
                    resp = {
                        "order_id" : new_order.id,
                        "buyer_id" : new_order.buyer_id,
                        "created_at" : new_order.created_at
                    }
                    return send_respose(200,new_order.json(),"Order Created Successfully.","")


                else:
                    Buyers.delete(buyer.id)
                    return send_respose(401,{},"","Order creation failed")

            else:
                Buyers.delete(buyer.id)
                print(v2.errors)
                return send_respose(402,{},"","Order Schema Failed")
        
        else:
            return send_respose(401,{},"","Error in buyer data")

    else:
        print(v1.errors)
        return send_respose(402,{},"","Buyer Schema Failed")


def fetch_all_orders(id):
    return Orders.fetch_orders_by_user_id(id)



    