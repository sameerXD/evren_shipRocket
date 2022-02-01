class db_code:
    class kyc_status:
        rejected = 0
        under_review = 1
        verified = 2

    class user:
        inactive = 0
        active = 1
        email_not_verified= 0
        email_verified= 1
        otp_validity = 300

    class order_status:
        cancelled = 0
        deleted = 0
        new = 1
        ready_for_pickup = 2
        pickep_up = 3
        completed = 4
    
    class wallet:
        credit= 0
        debit = 1
        clear = 1
        unclear =0
        order_place=0
        deposit_bank=1
        refund=2
        wallet_init_amount= 1200*100
