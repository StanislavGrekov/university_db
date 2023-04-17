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


# 5 задание
def task_5():
    type_product = 'КРЕДИТ' # Устанавливаем тип продукта
    oper_date = '2015-10-01' # Устанавливаем дату проведения операций
    dt = 1 # Устанавливаем признак дебетования счета

    cursor.execute('''
        select pt.name,  avg(r.sum)  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where pt.name=%s AND r.oper_date  = %s AND r.dt = %s
        GROUP BY pt.name
         ''', (type_product, oper_date, dt))

    data = cursor.fetchall()
    conn.commit()
    for element in data:
        print(f'Тип продукта: {element[0]}, средняя сумма по операциям {int(element[1])}')



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

# 7 задача
def task_7():
    '''
    Не сталкивался с тем, чтобы данные в БД разъезжались, но мне кажется можно поступить как:
    -  найти r.acc_ref по операциям и сумму операций с  dt = 0 и отдельно c dt = 1 из таблицы records

        select r.acc_ref, sum(r.sum) from records r
        inner join accounts a on r.acc_ref = a.id
        where r.dt = 1
        group by r.acc_ref

        select r.acc_ref, sum(r.sum) from records r
        inner join accounts a on r.acc_ref = a.id
        where r.dt = 0
        group by r.acc_ref

    - далее найти a.id и a.saldo из таблички accounts

        select a.id, a.saldo  from accounts a

    - и, если я правильно понимаю что saldo это разница между суммами операций при  dt = 0 и dt = 1, нам нужно вписать значения
    a.id в r.acc_ref, где sum(r.sum, при dt = 0) - sum(r.sum при dt = 1) = a.saldo
       '''
    pass

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
    и определяю клиента, у которого сумма = 0. Этого клинета нахожу в БД и делаю ему в табличке products дату
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

    id = cursor.fetchall()

    cursor.execute('''
        update products set close_date = %s WHERE id = %s;
        ''', (close_date, id[0][0]))
    print(f'Для клиента {name} установлена дата закрытия {close_date}')
    conn.commit()

def task_10():
    '''
    Сначала я нахожу клиентов, у которых были последнии операции 30 и больше дней назад.
     Затем в цикле я нахожу id продукта клиента и ставлю ему в дату закрытия сегодняшний день.
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

        id = cursor.fetchall()

        cursor.execute('''
                 update products set close_date = %s WHERE id = %s;
                ''', (close_date, id[0][0]))
        print(f'Для клиента {name} установлена дата закрытия {close_date}')
    conn.commit()


def task_11():
    '''
    Добавляю в табличку accounts столбец sum_dogovor.
    Не понимаю, что такое "сумма максимальной дебетовой операции" поэтому я заполню поле sum_dogovor суммой дебетовых
    операций по продукту Кредит и суммой кредитовых операций по продукту Карта, Депозит
    '''

    # Запрос по продукту Кедит, дебетовая операция
    cursor.execute('''
        select pt.name, SUM(r.sum)  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where pt."name" = 'КРЕДИТ' AND r.dt =1 
        GROUP by pt.name, r.dt
             ''')
    data = cursor.fetchall()

    pprint(int(data[0][1]))

    cursor.execute('''
            update accounts set sum_dogovor = %s WHERE product_ref = %s; 
            ''', (int(data[0][1]), 1)) # Здесь, конечно, сначала нужно вытаскивать product_ref через табличку products_type
    conn.commit()

    # Запрос по продукту Карта, кредитовая операция
    cursor.execute('''
        select pt.name, SUM(r.sum)  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where pt."name" = 'КАРТА' AND r.dt =0 
        GROUP by pt.name, r.dt
             ''')
    data = cursor.fetchall()

    pprint(int(data[0][1]))

    cursor.execute('''
            update accounts set sum_dogovor = %s WHERE product_ref = %s;
            ''', (int(data[0][1]), 3))
    conn.commit()

    # Запрос по продукту депозит, кредитовая операция
    cursor.execute('''
        select pt.name, SUM(r.sum)  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where pt."name" = 'ДЕПОЗИТ' AND r.dt =0 
        GROUP by pt.name, r.dt
             ''')
    data = cursor.fetchall()

    pprint(int(data[0][1]))

    cursor.execute('''
            update accounts set sum_dogovor = %s WHERE product_ref = %s;
            ''', (int(data[0][1]), 2))
    conn.commit()


if __name__ == '__main__':
    #task_4() # Нужно закомментировать или раскомментировать необходимую функцию.
    #task_5()
    #task_6()
    #task_7()
    #task_8()
    #task_9()
    #task_10()
    task_11()