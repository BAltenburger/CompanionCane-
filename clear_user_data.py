def clear(user_number):
    open(user_number + "service_order.txt", "w").write("")
    open(user_number + "user_age.txt", "w").write("")
    open(user_number + "user_number.txt", "w").write("")
    open(user_number + "user_gender.txt", "w").write("")
    open(user_number + "user_weight.txt", "w").write("")
    open(user_number + "emergency_contacts1.txt", "w").write("")
    open(user_number + "physician_contact.txt", "w").write("")
    open(user_number + "physician_email.txt", "w").write("")
    open(user_number + "user_preference.txt", "w").write("")
