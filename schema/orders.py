schema = {
    'user_id' : {'type':'integer','required':True},
    'buyer' : {
        'type':'dict',
        'allow_unknown' : True,
        'required':True
        },
    'buyer_id' : {'type':'integer','required':True},
    'store_id' : {'type':'integer', 'required':True},
    'products' : {
        'type':'dict',
        'allow_unknown' : True,
        'required':True
        },
    'total_order_amount' : {'type':'float'},
    'other_charges' : {'type':'float'},
    'discount' : {'type':'float'},
    'tax' : {'type':'float', 'required':True},
    'payment_mode' : {'type':'string', 'required':True},
    'item_length' : {'type':'float', 'required':True},
    'item_width' : {'type':'float', 'required':True},
    'item_height' : {'type':'float', 'required':True},
    'order_weight' : {'type':'float', 'required':True},
    'number_of_products' : {'type':'integer', 'required':True},
    'order_type' : {'type':'integer'},
    'parent_order_id' : {'type':'integer','dependencies':['order_type']},
}