from connect import cursor, conn

def add_data():
    '''
    Функция, заполняющая базу данных информацией
    '''
    cursor.execute('''

        insert into groups
        values (1, 122, 'Ремонт радиоаппаратуры', 25);
        insert into groups
        values (2, 125, 'Информационная безопасность', 12);
    
        insert into students
        values(1, 'Лойе', 'Александр', 'Витальевич');
        insert into students
        values(2, 'Фомкин', 'Алексей', 'Леонидович');
        insert into students
        values(3, 'Гусева', 'Наталья', 'Евгеньевна');
    
        insert into teacher
        values (1, 'Иванов', 'Иван', 'Иванович');
        insert into teacher
        values (2, 'Сидоров', 'Петр', 'Александрович');

        insert into day_of_the_week
        values (1, 'Понедельник', 'Пн');
        insert into day_of_the_week
        values (2, 'Вторник', 'Вт');
        insert into day_of_the_week
        values (3, 'Среда', 'Ср');
        insert into day_of_the_week
        values (4, 'Четверг', 'Чт');
        insert into day_of_the_week
        values (5, 'Пятница', 'Пт');
        insert into day_of_the_week
        values (6, 'Суббота', 'Суб');
        insert into day_of_the_week
        values (7, 'Воскресенье', 'Вс');

        insert into discipline
        values (1, 'Радиотехника');
        insert into discipline
        values (2, 'Усилительные устройства');
        insert into discipline
        values (3, 'Кибернетике');

        insert into auditorium
        values (1, 236, 'Класс технических наработок', 60);
        insert into auditorium
        values (2, 300, 'Лаборатория боевых ракетных и рактно-космических комплексов', 70);

        insert into lessons
        values (1, '08:00:00', '09:30:00');
        insert into lessons
        values (2,  '09:40:00', '11:10:00');
        insert into lessons
        values (3,'11:20:00', '12:50:00');
        insert into lessons
        values (4,'14:00:00', '15:30:00');
        insert into lessons
        values (5,'15:40:00', '17:10:00');
      
        insert into month
        values (9, 'Сентябрь');
        insert into month
        values (10, 'Октябрь');
        insert into month
        values (11, 'Ноябрь');
       
        insert into academic_year
        values (1, to_date('01.01.2023','DD.MM.YYYY'));
        insert into academic_year
        values (2, to_date('01.01.2024','DD.MM.YYYY'));

        insert into day_of_month
        values(1, 1);
        insert into day_of_month
        values(2, 2);
        insert into day_of_month
        values(3, 3);
        insert into day_of_month
        values(4, 4);
        insert into day_of_month
        values(5, 5);
        insert into day_of_month
        values(6, 6);
    
        insert into department
        values(1, 1, 'Кафедра конструирования и производства радиоаппаратуры');
        
        insert into learner
        values(1, 1, 1);
        insert into learner
        values(2, 1, 2);
        insert into learner
        values(3, 2, 3);
  
  
        insert into shedule
        values(1, 1, 1, 1, 1, 1, 1, 1, 9, 1);
        insert into shedule
        values(2, 1, 2, 2, 2, 2, 1, 1, 9, 1);
        insert into shedule
        values(3, 1, 1, 1, 1, 3, 1, 1, 9, 1);
        insert into shedule
        values(4, 1, 2, 2, 2, 4, 1, 1, 9, 1);
        
        ''')
    conn.commit()


    print('Данные добавлены.')


if __name__ == '__main__':
    add_data()