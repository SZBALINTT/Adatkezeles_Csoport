from pymongo import MongoClient, collection
import pymongo

client = pymongo.MongoClient("mongodb+srv://adat:jelszo1234@cluster.svqzgsc.mongodb.net/")

db = client.drink_companies


# --- Függvények ---
def lekerdezes1():
    print("Az egyes lekérdezés: 500 forintnál olcsóbb italok")
    query01 = db.drinks.find({ "price": { "$lt": 500 } }, {"name": 1, "price":1, "_id": 0})
    for i in query01:
        nev = i["name"]
        ar = i["price"]
        print(f"Az üdítő neve: {nev}, ára: {ar}")

def lekerdezes2():
    print("A kettes lekérdezés: az Aloe Vera Drink üdítőre érkezett értékelések")
    query02 = db.reviews.find({ "drink_name": "Aloe Vera Drink" }, {"rating": 1, "review":1})
    for i in query02:
        ertekeles = i["review"]
        pontszam = i["rating"]
        print(f"Szöveges értékelés: {ertekeles} \nPontszám: {pontszam} \n")

def lekerdezes3():
    print("A hármas lekérdezés: A budapesti automaták melyik helyeken találhatók meg")
    query03 = db.vending_machines.find({ "city": "Budapest" }, {"city": 1,"street": 1, "_id": 0})
    for i in query03:
        varos = i["city"]
        utca = i["street"]
        print(f"{varos}, {utca}")


def lekerdezes4():
    print("A négyes lekérdezés: kategóriák átlagára")
    query4 = db.drinks.aggregate([
        {"$group": {"_id": "$category", "AVG_Price": {"$avg": "$price"}}}
    ])
    for i in query4:
        nev = i["_id"]
        atlag_ar = i["AVG_Price"]
        print(f"{nev}: {atlag_ar}")

def lekerdezes5():
    print("Az ötös lekérdezés: mennyi ital van az egyes kategóriákban.")
    query5 = db.drinks.aggregate([
        {"$group": {"_id": "$category", "Count": {"$sum": 1}}}
    ])
    for i in query5:
        kategoria = i["_id"]
        mennyiseg = i["Count"]
        print(f"{kategoria}: {mennyiseg}")

def lekerdezes6():
    print("A hatos lekérdezés: Mekkora méretű automatákból mennyi van")
    query6 = db.vending_machines.aggregate([
        {"$group": {"_id": "$size", "Count": {"$sum": 1}}}
    ])
    for i in query6:
        meret = i["_id"]
        mennyiseg = i["Count"]
        print(f"{meret}: {mennyiseg}")

# CRUD függvények
def letrehozas():
    user_minta = {
                  "firstname":"Minta",
                  "lastname" : "Adat",
                  "username" : "mintaAdat",
                  "email" : "mintaadat@domain.com",
                  "age" : 22,
                }

    db.users.insert_one(user_minta)
    print("A \"mintaAdat\" felhasználónevű felhasználó létre lett hozva a user gyüjteményben")

def letrehozas2():
    spar_udito = {
        "name" : "Spar S-Budget Energy Drink",
        "price" : 199,
        "category" : "Energy Drinks",
        "volume":"200ml",
        }
    db.drinks.insert_one(spar_udito)
    print("A \"Spar S-Budget Energy Drink\" nevű ital létre lett hozva a drinks gyüjteményben")

def torles():
    db.users.delete_many({"username": "mintaAdat"})
    print("Az összes \"mintaAdat\" felhaszálónevű felhasználó törölve lett a user gyüjteményből")

def torles2():
    db.drinks.delete_many({"name":"7UP"})
    print("Az összes \"7UP\" nevű ital törölve lett a drinks gyüjteményből")

def frissites():
    update = {
         "$set":{"comment":"Pineapple-menta Pepsi is the ABSOLUTE BEST. I LOVE IT. Too bad they don't sell it anymore . :C","rating": 5},
    }
    db.reviews.update_one({"drink_name": "Pepsi"}, update)
    print("A Pepsi italhoz tartozó vélemény a review gyüjteményben frissítve lett")

def kereses():
    kereses_lekerdezes = db.reviews.find({"drink_name":"Pepsi"})
    for i in kereses_lekerdezes:
        nev = i["drink_name"]
        pontszam = i["rating"]
        velemeny = i["comment"]
        print(f"A {nev} italhoz tartozó vélemény:\nPontszám: {pontszam}\nVélemény: {velemeny}")

def reset():
    #Létrehozott adatok törlése
    db.users.delete_many({"username": "mintaAdat"})
    db.drinks.delete_many({"name":"Spar S-Budget Energy Drink"}) 

    #Vélemény visszaállítása az eredetire
    resetter={
    "$set":{"comment":"Coca Cola is better.","rating":3} 
    }
    result=db.reviews.update_one({"drink_name": "Pepsi"},resetter)

    #Kitörölt ital visszaállítása
    innivalo={
        "name" : "7UP",
        "price" : 510,
        "category" : "Soft Drinks",
        "volume":"330ml",
    }
    db.drinks.insert_one(innivalo)

    print("Az adatbázis vissza lett álíítva eredeti helyzetébe")


# --- Kiválasztó Program ---
while True:
    menu = input("\nVálassza ki, mit szeretne tenni. \n 1 - Lekérdezések | 2 - CRUD műveletek | k - Kilépés   \n")

    if (menu == "1"):
        #Lekérdezések
        while True:
            lekerdezesek_menu = input("\nMelyik lekérdezést szeretné megtekinteni? \n 1-5 - Lekérdezések | k - Vissza   \n")
            if (lekerdezesek_menu == "k"):
                break

            elif (lekerdezesek_menu == "1"):
                lekerdezes1()
                
            elif (lekerdezesek_menu == "2"):
                lekerdezes2()

            elif (lekerdezesek_menu == "3"):
                lekerdezes3()

            elif (lekerdezesek_menu == "4"):
                lekerdezes4()

            elif (lekerdezesek_menu == "5"):
                lekerdezes5()
                    
            elif (lekerdezesek_menu == "6"):
                lekerdezes6()

    elif (menu == "2"):
        #CRUD műveletek
        while True:
            muveletek_menu = input("\nMelyik CRUD műveletet szeretné végrehajtani? \n l - létrehozás | l2 - létrehozás 2 | t - törlés | t2 - törlés 2 | f - frissités | k - keresés | r - adatbázis alaphelyzetbe állítása | v - Vissza   \n")
            if (muveletek_menu == "v"):
                break

            elif (muveletek_menu == "l"):
                letrehozas()
            
            elif (muveletek_menu == "l2"):
                letrehozas2()

            elif (muveletek_menu == "t"):
                torles()

            elif (muveletek_menu == "t2"):
                torles2()

            elif (muveletek_menu == "f"):
                frissites()

            elif (muveletek_menu == "k"):
                kereses()
            
            elif (muveletek_menu == "r"):
                reset()

    elif (menu == "k"):
        break


""""
   --- Lekérdezések magukban ---

query01 = db.drinks.find({ "price": { "$lt": 500 } }, {"name": 1, "price":1, "_id": 0})
for i in query01:
   print(i)


query02 = db.reviews.find({ "drink_name": "Aloe Vera Drink" }, {"rating": 1, "review":1})
for i in query02:
   print(i)

query03 = db.vending_machines.find({ "city": "Budapest" }, {"city": 1,"street": 1, "_id": 0})
for i in query03:
   print(i)

query4 = db.drinks.aggregate([
    {"$group": {"_id": "$category", "AVG_Price": {"$avg": "$price"}}}
])
for i in query04:
   print(i)

query5 = db.drinks.aggregate([
        {"$group": {"_id": "$category", "Count": {"$sum": 1}}}
    ])
for i in query05:
   print(i)

query6 = db.vending_machines.aggregate([
        {"$group": {"_id": "$size", "Count": {"$sum": 1}}}
    ])
for i in query06:
   print(i)

 --- CRUD műveletek magukban ---


-Létrehozás-
1.
user_minta = {
                  "firstname":"Minta",
                  "lastname" : "Adat",
                  "username" : "mintaAdat",
                  "email" : "mintaadat@domain.com",
                  "age" : 22,
              }
db.users.insert_one(user_minta)
 
2.
spar_udito = {
    "name" : "Spar S-Budget Energy Drink",
    "price" : 199,
    "category" : "Energy Drinks",
    "volume":"200ml",
}
db.drinks.insert_one(spar_udito)


-Törlés-
1.
db.users.delete_many({"username": "mintaAdat"})
2.
db.drinks.delete_many({"name":"7UP"})

-Frissítés-

update = {
         "$set":{"comment":"Pineapple-menta Pepsi is the ABSOLUTE BEST. I LOVE IT. Too bad they don't sell it anymore . :C","rating": 5},
    }
db.reviews.update_one({"drink_name": "Pepsi"}, update)


-Keresés-
kereses_lekerdezes = db.reviews.find({"drink_name":"Pepsi"})
    for i in kereses_lekerdezes:
        print(i)

"""