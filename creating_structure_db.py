from connect import cursor, conn

def create_table():
    '''
    Функция, создающая структуру БД
    '''
    cursor.execute('''
    
            CREATE TABLE IF NOT EXISTS groups (
            id INTEGER primary key,
            number INTEGER NOT NULL,
            name VARCHAR(1000) NOT NULL,
            size VARCHAR(100) NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS teacher (
            id INTEGER primary key,
            last_name VARCHAR(100) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            patronymic VARCHAR(100) NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS day_of_the_week (
            id INTEGER primary key,
            day_week VARCHAR(100) NOT NULL,
            reduction VARCHAR(100) NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS discipline (
            id INTEGER primary key,
            subject VARCHAR(100) NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS auditorium (
            id INTEGER primary key,
            number INTEGER NOT NULL,
            name VARCHAR(100) NOT NULL,
            capacity INTEGER NOT NULL
            );
      
            CREATE TABLE IF NOT EXISTS lessons(
            id INTEGER primary key,
            time_begin TIME,
            time_end TIME
            );
            
            CREATE TABLE IF NOT EXISTS academic_year(
            id INTEGER primary key,
            year DATE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS students(
            id INTEGER primary key,
            last_name VARCHAR(100) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            patronymic VARCHAR(100) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS learner(
            id INTEGER primary key,
            group_ref INTEGER NOT NULL REFERENCES groups(id),
            student_ref INTEGER NOT NULL REFERENCES students(id)
            );
            
            CREATE TABLE IF NOT EXISTS department(
            id INTEGER primary key,
            group_ref INTEGER NOT NULL REFERENCES groups(id),
            name VARCHAR(1000) NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS month (
            id INTEGER primary key,
            name VARCHAR(100) NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS day_of_month (
            id INTEGER primary key,
            number INTEGER NOT NULL
            );
                        
            CREATE TABLE IF NOT EXISTS shedule(
            id INTEGER primary key,
            group_ref INTEGER NOT NULL REFERENCES groups(id),
            teacher_ref INTEGER NOT NULL REFERENCES teacher(id),
            discipline_ref INTEGER NOT NULL REFERENCES discipline(id),
            auditorium_ref INTEGER NOT NULL REFERENCES auditorium(id),
            lessons_ref INTEGER NOT NULL REFERENCES lessons(id),
            day_of_the_week_ref INTEGER NOT NULL REFERENCES day_of_the_week(id),
            day_of_month_ref INTEGER NOT NULL REFERENCES day_of_month(id),
            month_ref INTEGER NOT NULL REFERENCES month(id),
            academic_year_ref INTEGER NOT NULL REFERENCES academic_year(id)
            );


                ''')
    conn.commit()
    print('Структура успешно создана.')


def drop():
    '''
    Функция, удаляющая структуру в БД
    '''
    cursor.execute('''
            DROP TABLE teacher CASCADE;
            DROP TABLE day_of_the_week CASCADE;
            DROP TABLE discipline CASCADE;
            DROP TABLE auditorium CASCADE;
            DROP TABLE lessons CASCADE;
            DROP TABLE academic_year CASCADE;
            DROP TABLE students CASCADE;
            DROP TABLE learner CASCADE;
            DROP TABLE groups CASCADE;
            DROP TABLE department CASCADE;
            DROP TABLE month CASCADE;
            DROP TABLE day_of_month CASCADE;
            DROP TABLE shedule CASCADE;
        ''')
    conn.commit()
    print('Структура успешно удалена.')


if __name__ == '__main__':
    # drop() # Нужно закомментировать или раскомментировать необходимую функцию.
    create_table()
