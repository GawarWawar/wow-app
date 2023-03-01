import utils.static_db_creation.generate_static_item_database as st_db_generator
import utils.dn_db_helper as dn_db_helper

def receive_answer():
    try:
        answer = int(input("Input here: "))
        return answer
    except ValueError:
        print("""
              Program exept only numbers as an input :*
              """)
        answer = receive_answer()
        return answer
        
def check_element(element, check_group):
    if element in check_group:
        return element

print(
"""
Select next options what you want to do:
    0: Generate static database (if yes input 0)
    1: Transform dynamic database into parquet (if yes input 2)
    2: Transform dynamic database into csv (if yes input 1)
    3: Should we do logging (if yes input 3)

If you want all options, input 0123
*Transformation dynamic database into parquet will be done first
""",
)

answer = input("Input here: ")
answer = list(answer)

check_group = [
    "0", "1", "2", "3"
]

active_options = []
for i in answer:
    if check_element(i, check_group):
        active_options.append(i)

if "3" in active_options:
    log_on = True
else:
    log_on = False

if "0" in active_options:
    st_db_generator.main(
        log_on=log_on
    )

if "1" in active_options:
    dn_db_helper.csv_to_parquet(
        log_on=log_on
    )

if "2" in active_options:
    dn_db_helper.parquet_to_csv(
        log_on=log_on
    )
    
active_options.sort()
print(f"Options from this list was done {active_options} sucsessfully")