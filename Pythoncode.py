import random
from datetime import datetime, timedelta
import pandas as pd

# Configurations
num_customers = 15000
num_bookings = 25000
num_room_types = 6
num_branches = 10

# Base date range (5 years: 2021–2025)
start_date = datetime(2021, 1, 1)
end_date = datetime(2025, 12, 31)
date_range = (end_date - start_date).days + 1

# ============================
# 📅 Generate Date Dimension
# ============================
date_dim = []
for i in range(date_range):
    current_date = start_date + timedelta(days=i)
    date_id = f"D{i+1}"
    date_dim.append([
        date_id,
        current_date.strftime('%Y-%m-%d'),
        current_date.day,
        current_date.month,
        current_date.year,
        current_date.strftime('%A')
    ])
date_df = pd.DataFrame(date_dim, columns=['DateID', 'FullDate', 'Day', 'Month', 'Year', 'Weekday'])

# ============================
# 🏨 Generate Room Types
# ============================
room_types = []
for i in range(num_room_types):
    rid = f"RT{i+1}"
    room_types.append([
        rid,
        random.choice(["Single", "Double", "Suite"]),
        random.randint(2000, 10000),
        random.choice([1, 2, 4]),
        random.choice(["WiFi,TV", "WiFi,TV,MiniBar", "WiFi,TV,AC"]),
        random.choice([True, False]),
        random.choice([True, False])
    ])
room_df = pd.DataFrame(room_types, columns=['RoomTypeID', 'RoomType', 'Price', 'MaxOccupancy', 'Amenities', 'IsAC', 'IsSeaFacing'])

# ============================
# 🏢 Generate Branches (Total rooms ≤ 200)
# ============================
branches = []
cities_states = [
    ("Theni", "Tamil Nadu"), ("Delhi", "Delhi"), ("Mumbai", "Maharashtra"),
    ("Jaipur", "Rajasthan"), ("Chennai", "Tamil Nadu"), ("Kochi", "Kerala"),
    ("Goa", "Goa"), ("Ahmedabad", "Gujarat"), ("Pune", "Maharashtra"), ("Lucknow", "Uttar Pradesh")
]

total_rooms = 0
max_total_rooms = 200

for i in range(num_branches):
    cid, state = random.choice(cities_states)
    
    remaining_branches = num_branches - i
    remaining_capacity = max_total_rooms - total_rooms
    
    if remaining_branches > 1:
        room_count = random.randint(10, max(10, remaining_capacity // remaining_branches))
    else:
        room_count = remaining_capacity  # last branch gets remaining rooms
    
    total_rooms += room_count

    branches.append([
        f"B{i+1}",
        f"HotelRev {cid}",
        cid,
        state,
        f"Mr./Ms. {random.choice(['Rajan', 'Kavya', 'Mehta', 'Anita', 'Singh', 'Verma'])}",
        f"9{random.randint(100000000, 999999999)}",
        random.randint(3, 5),
        room_count,
        round(random.uniform(60, 95), 2),
        random.choice([True, False]),
        random.choice([True, False])
    ])

branch_df = pd.DataFrame(branches, columns=[
    'BranchID', 'BranchName', 'City', 'State', 'ManagerName', 'Phone',
    'StarRating', 'RoomCount', 'RevenueScore', 'HasPool', 'HasConferenceRoom'
])

print(f"✅ Total Rooms Across Branches: {total_rooms}")

# ============================
# 👥 Generate Customers
# ============================
customer_names = ["Aarav", "Kavya", "Rohan", "Simran", "Ishaan", "Tanya", "Aditya", "Neha", "Rajat", "Priya"]
loyalty_tiers = ['Bronze', 'Silver', 'Gold', 'Platinum']
age_groups = ['18-25', '26-35', '36-50', '51+']
genders = ['Male', 'Female', 'Other']

customers = []
for i in range(num_customers):
    name = random.choice(customer_names) + " " + random.choice(["Sharma", "Verma", "Kapoor", "Bhatia", "Sethi"])
    customers.append([
        f"C{i+1}",
        name,
        f"{name.replace(' ', '.').lower()}@example.com",
        f"9{random.randint(100000000, 999999999)}",
        random.choice(["Delhi", "Mumbai", "Chennai", "Jaipur", "Kolkata"]),
        random.choice(["Delhi", "Maharashtra", "Tamil Nadu", "Rajasthan", "West Bengal"]),
        "Indian",
        random.choice(loyalty_tiers),
        random.choice(age_groups),
        random.choice(genders)
    ])
customer_df = pd.DataFrame(customers, columns=[
    'CustomerID', 'Name', 'Email', 'Phone', 'City', 'State', 'Nationality',
    'LoyaltyTier', 'AgeGroup', 'Gender'
])

# ============================
# 📘 Generate Bookings
# ============================
booking_statuses = ['Cancelled', 'Checked-in', 'No-show']
payment_methods = ['Credit Card', 'UPI', 'Cash', 'Corporate Account']
booking_channels = ['Website', 'Mobile App', 'Travel Agent', 'Call Center']
purpose_booking = ['Business', 'Vacation', 'Conference', 'Holiday', '']

bookings = []
for i in range(num_bookings):
    bid = f"BK{i+1}"
    customer = customer_df.sample(1).iloc[0]
    room = room_df.sample(1).iloc[0]
    branch = branch_df.sample(1).iloc[0]

    check_in_index = random.randint(0, len(date_df) - 10)
    stay_length = random.randint(1, 7)
    check_out_index = check_in_index + stay_length

    check_in_date = date_df.iloc[check_in_index]['FullDate']
    check_out_date = date_df.iloc[check_out_index]['FullDate']

    revenue = int(room['Price']) * stay_length
    status = random.choice(booking_statuses)
    cancel_reason = random.choice(['Price', 'Change of plans', 'Weather', 'Other']) if status == 'Cancelled' else ''
    discount = random.choice([0, 5, 10, 15, 20])

    bookings.append([
        bid,
        customer['CustomerID'],
        room['RoomTypeID'],
        branch['BranchID'],
        check_in_date,
        check_out_date,
        stay_length,
        revenue,
        status,
        cancel_reason,
        random.randint(0, 60),
        random.choice(payment_methods),
        discount,
        random.choice(booking_channels),
        random.choice(purpose_booking)
    ])

booking_df = pd.DataFrame(bookings, columns=[
    'BookingID', 'CustomerID', 'RoomTypeID', 'BranchID',
    'CheckInDate', 'CheckOutDate', 'Duration', 'Revenue', 'BookingStatus',
    'CancellationReason', 'LeadTime', 'PaymentMethod', 'DiscountApplied', 'BookingChannel', 'Purpose'
])

# ============================
# 💾 Write all to Excel
# ============================
with pd.ExcelWriter("HotelData_AllSheets.xlsx", engine='openpyxl') as writer:
    customer_df.to_excel(writer, sheet_name='Customer', index=False)
    branch_df.to_excel(writer, sheet_name='Branch', index=False)
    room_df.to_excel(writer, sheet_name='RoomType', index=False)
    date_df.to_excel(writer, sheet_name='Date', index=False)
    booking_df.to_excel(writer, sheet_name='Booking', index=False)

print("✅ HotelData_AllSheets.xlsx created successfully with total rooms ≤ 200 and all dates in YYYY-MM-DD format!")
