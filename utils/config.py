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

