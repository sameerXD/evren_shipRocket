schema = {
    # 'order_id':{'type':'integer','required':True},
    'product_name':{'type':'string','required':True},
    'hsn_code':{'type':'string'},
    'unit_price':{'type':'float', 'required':True},
    'units_ordered':{'type':'float', 'required':True},
    'unit_used':{'type':'string'},
    'tax_rate':{'type':'float', 'required':True},
}