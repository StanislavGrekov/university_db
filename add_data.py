from connect import cursor, conn


def create_table():
    '''
    Функция, создающая структуру БД
    '''
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
            id INTEGER primary key,
            name VARCHAR(1000) NOT NULL,
            place_of_birth VARCHAR(1000) NOT NULL,
            date_of_birth DATE,
            address VARCHAR(1000) NOT NULL,
            passport VARCHAR(100) NOT NULL UNIQUE
            );
            
            CREATE TABLE IF NOT EXISTS tarifs (
            id INTEGER primary key,
            name VARCHAR(100) NOT NULL,
            cost NUMERIC(10,2)
            );
            
            CREATE TABLE IF NOT EXISTS products_type (
            id INTEGER primary key,
            name VARCHAR(100) NOT NULL,
            begin_date DATE,
            end_date DATE,
            tarif_ref INTEGER NOT NULL REFERENCES tarifs(id)
            );
            
            CREATE TABLE IF NOT EXISTS products (
            id INTEGER primary key,
            product_type_id INTEGER NOT NULL REFERENCES products_type(id),
            name VARCHAR(100) NOT NULL,
            client_ref INTEGER NOT NULL REFERENCES clients(id),
            open_date DATE,
            close_date DATE
            );
            
            CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER primary key,
            name VARCHAR(100) NOT NULL,
            saldo NUMERIC(10,2),
            client_ref INTEGER NOT NULL REFERENCES clients(id),
            open_date DATE,
            close_date DATE,
            product_ref INTEGER NOT NULL REFERENCES products(id),
            acc_num VARCHAR(100) NOT NULL UNIQUE
            );
            
            CREATE TABLE IF NOT EXISTS records (
            id INTEGER primary key,
            dt NUMERIC(1),
            sum NUMERIC(10,2),
            acc_ref INTEGER NOT NULL REFERENCES accounts(id),
            oper_date DATE
            );
                ''')
    conn.commit()
    print('Структура успешно создана.')


def drop():
    '''
    Функция, удаляющая структуру в БД
    '''
    cursor.execute('''
            DROP TABLE clients CASCADE;
            DROP TABLE records CASCADE;
            DROP TABLE accounts CASCADE;
            DROP TABLE products CASCADE;
            DROP TABLE products_type CASCADE;
            DROP TABLE tarifs CASCADE;
        ''')
    conn.commit()
    print('Структура успешно удалена.')


def add_data():
    '''
    Функция, заполняющая базу данных информацией
    '''
    cursor.execute('''
        insert into tarifs
        values (1,'Тариф за выдачу кредита', 10);
        insert into tarifs
        values (2,'Тариф за открытие счета', 10);
        insert into tarifs
        values (3,'Тариф за обслуживание карты', 10);
        
        
        insert into products_type 
        values (1, 'КРЕДИТ', to_date('01.01.2018','DD.MM.YYYY'), null, 1);
        insert into products_type
        values (2, 'ДЕПОЗИТ', to_date('01.01.2018','DD.MM.YYYY'), null, 2);
        insert into products_type 
        values (3, 'КАРТА', to_date('01.01.2018','DD.MM.YYYY'), null, 3);
        
        
        insert into clients 
        values (1, 'Сидоров Иван Петрович', 'Россия, Московская облать, г. Пушкин', to_date('01.01.2001','DD.MM.YYYY'), 'Россия, Московская облать, г. Пушкин, ул. Грибоедова, д. 5', '2222 555555, выдан ОВД г. Пушкин, 10.01.2015');
        insert into clients 
        values (2, 'Иванов Петр Сидорович', 'Россия, Московская облать, г. Клин', to_date('01.01.2001','DD.MM.YYYY'), 'Россия, Московская облать, г. Клин, ул. Мясникова, д. 3', '4444 666666, выдан ОВД г. Клин, 10.01.2015');
        insert into clients 
        values (3, 'Петров Сиодр Иванович', 'Россия, Московская облать, г. Балашиха', to_date('01.01.2001','DD.MM.YYYY'), 'Россия, Московская облать, г. Балашиха, ул. Пушкина, д. 7', '4444 666666, выдан ОВД г. Клин, 10.01.2016');
        
        insert into products
        values (1, 1, 'Кредитный договор с Сидоровым И.П.', 1, to_date('01.06.2015','DD.MM.YYYY'), null);
        insert into products 
        values (2, 2, 'Депозитный договор с Ивановым П.С.', 2, to_date('01.08.2017','DD.MM.YYYY'), null);
        insert into products 
        values (3, 3, 'Карточный договор с Петровым С.И.', 3, to_date('01.08.2017','DD.MM.YYYY'), null);
        
        
        insert into accounts 
        values (1, 'Кредитный счет для Сидоровым И.П.', -2000, 1, to_date('01.06.2015','DD.MM.YYYY'), null, 1, '45502810401020000022');
        insert into accounts 
        values (2, 'Депозитный счет для Ивановым П.С.', 6000, 2, to_date('01.08.2017','DD.MM.YYYY'), null, 2, '42301810400000000001');
        insert into accounts 
        values (3, 'Карточный счет для Петровым С.И.', 8000, 3, to_date('01.08.2017','DD.MM.YYYY'), null, 3, '40817810700000000001');
        
        insert into records 
        values (1, 1, 5000, 1, to_date('01.06.2015','DD.MM.YYYY'));
        insert into records 
        values (2, 0, 1000, 1, to_date('01.07.2015','DD.MM.YYYY'));
        insert into records 
        values (3, 0, 2000, 1, to_date('01.08.2015','DD.MM.YYYY'));
        insert into records 
        values (4, 0, 3000, 1, to_date('01.09.2015','DD.MM.YYYY'));
        insert into records
        values (5, 1, 5000, 1, to_date('01.10.2015','DD.MM.YYYY'));
        insert into records 
        values (6, 0, 3000, 1, to_date('01.10.2015','DD.MM.YYYY'));
        
        insert into records 
        values (7, 0, 10000, 2, to_date('01.08.2017','DD.MM.YYYY'));
        insert into records
        values (8, 1, 1000, 2, to_date('05.08.2017','DD.MM.YYYY'));
        insert into records
        values (9, 1, 2000, 2, to_date('21.09.2017','DD.MM.YYYY'));
        insert into records
        values (10, 1, 5000, 2, to_date('24.10.2017','DD.MM.YYYY'));
        insert into records 
        values (11, 0, 6000, 2, to_date('26.11.2017','DD.MM.YYYY'));
        
        insert into records 
        values (12, 0, 120000, 3, to_date('08.09.2017','DD.MM.YYYY'));
        insert into records
        values (13, 1, 1000, 3, to_date('05.10.2017','DD.MM.YYYY'));
        insert into records 
        values (14, 1, 2000, 3, to_date('21.10.2017','DD.MM.YYYY'));
        insert into records 
        values (15, 1, 5000, 3, to_date('24.10.2017','DD.MM.YYYY'));
        
        insert into records 
        values (16, 1, 2500, 3, to_date('20.03.2023','DD.MM.YYYY'));
        insert into records 
        values (17, 0, 3500, 3, to_date('20.03.2023','DD.MM.YYYY'));
        
        insert into records 
        values (18, 1, 2500, 1, to_date('20.03.2023','DD.MM.YYYY'));
        insert into records 
        values (19, 0, 3500, 1, to_date('20.03.2023','DD.MM.YYYY'));
        
        insert into records 
        values (20, 1, 2500, 2, to_date('20.03.2023','DD.MM.YYYY'));
        insert into records 
        values (21, 0, 3500, 2, to_date('20.03.2023','DD.MM.YYYY'));

        ''')
    conn.commit()
    print('Данные добавлены.')

if __name__ == '__main__':
    #drop() # Нужно закомментировать или раскомментировать необходимую функцию.
    #create_table()
    add_data()