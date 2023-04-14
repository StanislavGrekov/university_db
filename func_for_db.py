from connect import cursor,conn
from pprint import pprint
import datetime

# 4 задание
def task_4():
    cursor.execute('''
        select a.acc_num  from accounts a 
        inner join products p on a.product_ref = p.id 
        inner join products_type pt on p.product_type_id = pt.id 
        where pt.name = 'ДЕПОЗИТ' and not pt.name = 'КРЕДИТ'
         ''')
    date = cursor.fetchall()[0]
    conn.commit()
    for element in date:
        print(f'Номер счета {element}')

# 6 задача
def task_6():
    cursor.execute('''
        select c.name, r.oper_date, sum(r.sum)  from clients c
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        WHERE r.oper_date >= '2023-03-01' and r.oper_date <= '2023-03-31'
        group by c.name, r.oper_date 
         ''')
    date = cursor.fetchall()
    conn.commit()
    for element in date:
        print(f'Клиент: {element[0]}, дата: {element[1]}. Сумма операция на указанную дату: {element[2]}')

# 8 задача
select c.name, p."name", pt.name  from clients c
inner join products p on c.id = p.client_ref
inner join products_type pt on pt.id = p.product_type_id

if __name__ == '__main__':
    # task_4()
    task_6()