import pandas as pd

# Load CSVs once at module level for reuse
customer_df = pd.read_csv("crm_data.csv")
otp_df = pd.read_csv("dummy_users_otps.csv")


def validate_chassis(chassis_number: str) -> dict:
    """
    Validates the given chassis number in the system using the CSV data.
    """
    # customer_df = pd.read_csv("dummy_users_otps.csv")
    match = customer_df[customer_df['chassis_number'] == chassis_number]
    if not match.empty:
        row = match.iloc[0]
        return {
            'found': True,
            'firstName': row['first_name'],
            'lastName': row['last_name'],
            'rcNumber': row['reg_number']
        }
    else:
        return {'found': False}


def validate_chassis_details_with_crm(firstName: str, lastName: str, chassis_number: str) -> str:
    """
    Validates chassis details with the CRM system using the CSV data.
    """
    match = customer_df[
        (customer_df['first_name'] == firstName) &
        (customer_df['last_name'] == lastName) &
        (customer_df['chassis_number'] == chassis_number)
    ]
    return "VALID" if not match.empty else "INVALID"


def validate_rc_copy(image: bytes, chassis_number: str) -> str:
    """
    RC copy validation function remains unchanged.
    """
    return "VALID"


def send_otp(mobile_number: str) -> bool:
    """
    Sends OTP to the given mobile number (mock).
    """
    print(f"Sending OTP to {mobile_number}")
    return True


def validate_otp(otp: str, mobile_number: str) -> str:
    """
    Validates the OTP for the given mobile number using the OTP CSV data.
    """
    match = otp_df[
        (otp_df['mobile_number'] == int(mobile_number)) &
        (otp_df['otp'] == int(otp))
    ]
    return "VALID" if not match.empty else "INVALID"


def update_and_sync_new_mobile_number(old_mobile_number: str, new_mobile_number: str) -> str:
    """
    Updates the old mobile number with the new one in both the customer CSV and OTP CSV.

    Args:
        old_mobile_number (str): The current mobile number.
        new_mobile_number (str): The new mobile number to update.

    Returns:
        str: Confirmation message after update.
    """
    # --- Update dummy_users.csv ---
    customer_df = pd.read_csv("crm_data.csv")
    customer_df.columns = customer_df.columns.str.strip()
    
    updated = False
    if 'mob_number' in customer_df.columns:
        match_idx = customer_df[customer_df['mob_number'] == int(old_mobile_number)].index
        if not match_idx.empty:
            customer_df.loc[match_idx, 'mob_number'] = int(new_mobile_number)
            updated = True

    if updated:
        customer_df.to_csv("dummy_users.csv", index=False)
    else:
        return f"No match found for old mobile number {old_mobile_number} in dummy_users.csv."

    # --- Update dummy_users_otps.csv ---
    otp_df = pd.read_csv("dummy_users_otps.csv")
    otp_df.columns = otp_df.columns.str.strip()

    match_idx_otp = otp_df[otp_df['mobile_number'] == int(old_mobile_number)].index
    if not match_idx_otp.empty:
        otp_df.loc[match_idx_otp, 'mobile_number'] = int(new_mobile_number)
        otp_df.to_csv("dummy_users_otps.csv", index=False)
    else:
        return f"Updated in dummy_users.csv, but no match found for old mobile number {old_mobile_number} in dummy_users_otps.csv."

    return f"Mobile number updated from {old_mobile_number} to {new_mobile_number} and synced successfully all the systems."
