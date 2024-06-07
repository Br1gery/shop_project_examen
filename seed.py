from sqlalchemy.orm import Session
from database import engine
import models

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:
    # con1 = models.Country(name='Россия')
    # con2 = models.Country(name='Япония')

    # reg1 = models.Region(name='Свердловская область')
    # reg2 = models.Region(name='Хоккайдо')

    # mount1 = models.Mountain(name='parkur',height=10,countries=con1,regions = reg1)

    # mem1 = models.Member(FIO='parkuring',addres='xd xd xd')
    # mem2 = models.Member(FIO='parkuring2',addres='xd2 xd2 xd2')

    # cli1 = models.Climbing(name='climbing №1',date_start = datetime.now(), date_end = datetime(2025,1,1),mountain=mount1,members=[mem1,mem2])
    role1 = models.Role(name='user')
    role2 = models.Role(name='admin')
    role3 = models.Role(name='moderator')

    user1 = models.User(username = 'UserName', password = '$2b$12$8Xd0JDxaROG2eBg00Wo2zuw/nsCLCNyCphPrJaF0LabjBY/sBZHD2', role = role2)
    #UserName:UserName

    cat1 = models.Category(name='Мясо', description = 'Мясные продукты')
    cat2 = models.Category(name='Рыба', description = 'Рыбные продукты')
    cat3 = models.Category(name='Хлебобулочные изделия', description = 'Хлебобулочные изделия')
    cat4 = models.Category(name='Заморозка', description = 'Замороженные мясные/рыбные продукты')
    cat5 = models.Category(name='Полуфабрикаты', description = 'Полуфабрикаты')


    prod1 = models.Product(name='Говядина', description = 'desc_test1',avg_rating = 1, price = 1000,categories=[cat1,cat4])

    session.add_all([role1,role2,role3,user1,cat1,cat2,cat3,cat4,cat5,prod1])
    session.commit()