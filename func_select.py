from connect import cursor, conn


def select_1():
    """Студенты преподавателя Сидорова в группе 122"""
    cursor.execute('''
    select min(s.id), t.last_name, g.number, s.last_name, s.first_name from students s 
    inner join learner l on s.id = l.student_ref 
    inner join groups g on l.group_ref = g.id 
    inner join shedule s2 on g.id = s2.group_ref 
    inner join teacher t on s2.teacher_ref = t.id  
    where t.last_name = 'Сидоров' and g.number = 122
    group by t.last_name, s.last_name, s.first_name, g.number
         ''')

    data = cursor.fetchall()
    teacher = {}
    groups = {}
    students = []

    for element in data:
        teacher['teacher'] = element[1]
        groups['groups'] = element[2]
        personal_data = f'{element[3]} {element[4]}'
        students.append(personal_data)

    print(f'Преподаватель - {teacher["teacher"]}, группа - {groups["groups"]}, студенты - {", ".join(students)}.')

def select_2():
    """Кол-во уроков преподавателя Иванова в понедельник"""
    cursor.execute('''
    select t.last_name, t.first_name, count(l.id)  from teacher t
    inner join shedule s on s.teacher_ref = t.id 
    inner join lessons l on s.lessons_ref = l.id 
    inner join day_of_the_week dotw on s.day_of_the_week_ref = dotw.id 
    where t.last_name = 'Иванов' and dotw.reduction = 'Пн'
    group by t.last_name, t.first_name 
         ''')

    data = cursor.fetchall()
    print(f"Преподаватель - {data[0][0]} {data[0][1]}, кол-во уроков - {data[0][2]}.")


if __name__ == '__main__':
    # select_1() # Нужно закомментировать или раскомментировать необходимую функцию.
    select_2()
