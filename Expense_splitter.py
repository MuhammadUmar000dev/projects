# Hostel/Flat Expense Splitter

# Input Section
rent = int(input("Enter your hostel/flat rent: "))
food = int(input("Enter the total amount spent on food: "))
electricity_units = int(input("Enter total electricity units consumed: "))
charge_per_unit = int(input("Enter electricity charge per unit: "))
persons = int(input("Enter the number of persons living in the hostel/flat: "))

# Calculations
electricity_bill = electricity_units * charge_per_unit
total_expense = rent + food + electricity_bill
share_per_person = total_expense // persons

# Output
print("\n--- Expense Summary ---")
print(f"Total Rent: {rent}")
print(f"Total Food Expense: {food}")
print(f"Electricity Bill: {electricity_bill}")
print(f"Overall Expense: {total_expense}")
print(f"Each person will pay: {share_per_person}")
