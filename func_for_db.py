from connect import cursor, conn
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
    data = cursor.fetchall()[0]
    conn.commit()
    for element in data:
        print(f'Номер счета {element}')


def task_5():
    cursor.execute('''
        select pt.name,  avg(r.sum)  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where pt.name='КРЕДИТ' AND r.oper_date  = '2015-10-01' AND r.dt = 1
        GROUP BY  pt.name

         ''')
    data = cursor.fetchall()[0]
    conn.commit()
    pprint(data)



# 6 задача
def task_6():
    cursor.execute('''
        select c.name, r.oper_date, sum(r.sum)  from clients c
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        WHERE r.oper_date >= '2023-03-01' and r.oper_date <= '2023-03-31'
        group by c.name, r.oper_date 
         ''')
    data = cursor.fetchall()
    conn.commit()
    for element in data:
        print(f'Клиент: {element[0]}, дата: {element[1]}. Сумма операция на указанную дату: {element[2]}')


# 8 задача
def task_8():
    '''Если я правильно понимаю, чтобы погасить кредит, надо чтобы общая сумма по операциям с dt=1 и dt=0
    равнялась нулю. Здесь я сначал нахожу клиента с продуктом Кредит и с пустой датой закрытия, а затем в цикле
     получаю сумму по операциям. Сумма равняется 2000, получается что клиент снова взял кредит.'''
    cursor.execute('''
        select c.name,  pt.name, r.sum, r.dt  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where pt."name" = 'КРЕДИТ'  AND p.close_date  is NULL
         ''')
    data = cursor.fetchall()
    pprint(data)
    conn.commit()
    count = 0
    for element in data:
        if element[3] == 1:
            count+=element[2]
        else:
            count -= element[2]
    print(f'Cумма кредита: {count}')


def task_9():
    '''
    Сначала я выполняю Select запросы к БД и нахожу клиентов у которых открыт продукт - Кредит,
    проверяю чтобы он не был закрыт и считаю сумму по операциям при dt = 0 и dt = 1. Потом я суммирую эти значения
    и определяю клиента, у которого сумма = 0. Этого клинета нахожу в БД и делаю ему в табличке poducts дату
    закрытия продукта.
    '''
    cursor.execute('''
        select c.name,  pt.name, SUM(r.sum), r.dt  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where pt."name" = 'КРЕДИТ' AND r.dt =1 AND p.close_date  is NULL
        GROUP by c.name,  pt.name,  r.dt
         ''')
    data = cursor.fetchall()
    dict_client_dt_1 = {}
    for element in data:
        dict_client_dt_1[element[0]] = [int(element[2])]

    cursor.execute('''
        select c.name,  pt.name, SUM(r.sum), r.dt  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where pt."name" = 'КРЕДИТ' AND r.dt =0 AND p.close_date  is NULL
        GROUP by c.name,  pt.name,  r.dt
         ''')
    data = cursor.fetchall()
    dict_client_dt_0 = {}
    for element in data:
        dict_client_dt_0[element[0]] = [-int(element[2])]

    conn.commit()

    rezult= {}

    for key_1, val_1 in  dict_client_dt_0.items():
        if key_1 in dict_client_dt_1:
            dict_client_dt_1[key_1].extend(val_1)
        else:
            dict_client_dt_1[key_1] = val_1
    rezult.update(dict_client_dt_1)

    date = datetime.datetime.now()
    close_date = (str(date.year) + '-' + str(date.month) + '-' + str(date.day))

    for name,amount in rezult.items():
        if sum(amount) == 0:
            cursor.execute('''
                select p.id from products p
                inner join clients c on c.id =p.client_ref 
                where c.name = %s;''', (name,))

    name = cursor.fetchall()

    cursor.execute('''
        update products set close_date = %s WHERE id = %s;
        ''', (close_date, name[0][0]))

    conn.commit()

def task_10():
    '''
    Сначала я выполняю Select запросы к БД и нахожу клиентов у которых открыт продукт - Кредит,
    проверяю чтобы он не был закрыт и считаю сумму по операциям при dt = 0 и dt = 1. Потом я суммирую эти значения
    и определяю клиента, у которого сумма = 0. Этого клинета нахожу в БД и делаю ему в табличке poducts дату
    закрытия продукта.
    '''
    cursor.execute('''
        select c.name, r.oper_date  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where r.oper_date  < CURRENT_DATE - 30
             ''')
    data = cursor.fetchall()
    conn.commit()

    date = datetime.datetime.now()
    close_date = (str(date.year) + '-' + str(date.month) + '-' + str(date.day))

    dict_client={}
    for element in data:
        dict_client[element[0]] = close_date

    for name, close_date in dict_client.items():
        cursor.execute('''
                select p.id from products p
                inner join clients c on c.id =p.client_ref 
                where c.name = %s;''', (name,))

        name = cursor.fetchall()

        cursor.execute('''
                 update products set close_date = %s WHERE id = %s;
                ''', (close_date, name[0][0]))

    conn.commit()

if __name__ == '__main__':
    #task_4()
    task_5()
    #task_6()
    #task_8()
    #task_9()
    #task_10()