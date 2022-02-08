
import json

c={}

messages={
    "d1": 'd1 (мм)-диаметр поршня ',
    "d2": 'd2 (мм)-диаметр штока ',
    "t1":'t1 (сек)-время выдвижения штока',
    "t2":'t2 (сек)-время втягивания штока',
    "v1": "v1 (м/сек)скорость при выдвижении штока ",
    "v2": "v2 (м/сек)скорость при втягивании штока ",
    "Q1": 0,
    "Q2": 0,
    "P1": 'P1 (кН) - усилие при выдвижении штока',
    "P2": 'P1 (кН) - усилие при втягивании штока',
    "m": 'm (тн) - масса груза',
    "p1": 'p1 (Bar) - давление в поршневой полости',
    "p2": 'p2 (Bar) - давление в штоковой полости',
    "L1": 'L 1(мм)- ход поршня при выдвижении штока ',
    "L2": 'L 2(мм)- ход поршня при втягивании штока ',
}
# файлы для записи и чтения

#file_name = "E:/ГИДРООБОРУДОВАНИЕ/7535  Кран  'PRESTEL'/УСКОРЯЮ PRESTEL/7535_PRESTEL.json"
file_name='cylinder.json'
#file_name ="C:/Python34/MyLessons/Hydraulics/JsonFiles/7535_PRESTEL.json"


#  запись
def w_file():
    with open( file_name, 'w')as file:
        json.dump(c, file,sort_keys=True, indent=4)


# чтение   
def r_file():   
    with open(file_name, 'r') as file:
        c_read=json.load(file)
    for key, val in c_read.items():
        c[key]=val
        if  c[key] != 0:
            print('    {}:{:>2}'.format(key,val))

# получаю словарь из внешнего фаила или записываю
def get_par():
    try:
        r_file()
    except :
        print("запись введённых значений")
        w_file()
        


# перезаписываю внешний файл после ввода запрашиваемых значений
def parameter_input(key):
    if len(c) == 0:
        r_file()
    par = c.get(key, 0)
    print('параметр {} определён значением {}'.format(messages.get(key), par))
    try:
        par = float(input('введи новое значение или \
        жми клавишу "ввод" , чтобы оставить прежним\n'))
        c[key]=par
        w_file() #перезаписываю файл
    except:
        pass
    return par
    
  


'''
#запись
def w_file(file='cilinder.txt'):
    with open(file, 'w')as file:
        for key,val in cil.items():
            file.write('{}:{} \n'.format(key, str(val)))
    pass

#чтение
def r_file(file='cilinder.txt'):
    new={}
    with open(file, 'r')as file:
        for i in file.readlines():
            key,val = i.strip().split(':')
            new[key]=val
    print (new) 
'''


