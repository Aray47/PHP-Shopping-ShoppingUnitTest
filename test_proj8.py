import unittest
import shopping
import sqlite3

DBNAME = 'test8.db'
DBCONN = sqlite3.connect(DBNAME)

def clearDatabase():
    c = DBCONN.cursor()

    c.execute('DELETE FROM accounts')
    c.execute('DELETE FROM items')
    c.execute('DELETE FROM purchases')
    c.execute('DELETE FROM reviews')
    DBCONN.commit()

class testInitialize(unittest.TestCase):
    def test_initialize(self):
        factory = shopping.ShoppingFactory(DBNAME)  #testing our db
        with self.assertRaises(Exception):
            factory = shopping.ShoppingFactory("test_foo.db")   #file that doesn't exist


class testPageSize(unittest.TestCase):
    def test_setPageSize(self):         # testing good values here
        factory = shopping.ShoppingFactory(DBNAME)
        factory.setPageSize(11)
        self.assertEqual(factory.getPageSize(), 11)
        factory.setPageSize(1)
        self.assertEqual(factory.getPageSize(), 1)
        factory.setPageSize(100)
        self.assertEqual(factory.getPageSize(), 100)

    def test_badValues(self):           # testing bad values here
        factory = shopping.ShoppingFactory(DBNAME)
        with self.assertRaises(Exception):
            factory.setPageSize("Hello")
        with self.assertRaises(Exception):
            factory.setPageSize(-1)
        with self.assertRaises(Exception):
            factory.setPageSize(101)
        with self.assertRaises(Exception):
            factory.setPageSize(0)

        

class TestGetPage(unittest.TestCase):
    def test_NumberOfItems(self):
        clearDatabase()
        c = DBCONN.cursor()
        c.execute('INSERT INTO items VALUES (1, "Macbook", 1.99, 3, "laptop,mac")')
        c.execute('INSERT INTO items VALUES (2, "Macbook", 1.99, 3, "laptop,mac")')
        c.execute('INSERT INTO items VALUES (3, "Macbook", 1.99, 3, "laptop,mac")')
        c.execute('INSERT INTO items VALUES (4, "Macbook", 1.99, 3, "laptop,mac")')
        c.execute('INSERT INTO items VALUES (5, "Macbook", 1.99, 3, "laptop,mac")')
        c.execute('INSERT INTO items VALUES (6, "Macbook", 1.99, 3, "laptop,mac")')
        c.execute('INSERT INTO items VALUES (7, "Macbook", 1.99, 3, "laptop,mac")')
        
        DBCONN.commit()

        factory = shopping.ShoppingFactory(DBNAME)
        factory.setPageSize(3)

        self.assertEqual(len(factory.getNextPage()), 3)
        self.assertEqual(len(factory.getNextPage()), 3)
        self.assertEqual(len(factory.getNextPage()), 1)
        self.assertEqual(len(factory.getNextPage()), 0)


    def test_getItems(self):
        clearDatabase()  #re-clear the database as to not have a bunch of random shit
        c = DBCONN.cursor()
        c.execute('INSERT INTO items VALUES (1, "Macbook", 3000.00, 300, "laptop,mac")')  #insert new data
        c.execute('INSERT INTO items VALUES (2, "Dell", 1.99, 3, "laptop,pc")')
        DBCONN.commit()       

        factory = shopping.ShoppingFactory(DBNAME)
        items = factory.getNextPage()
        self.assertEqual(len(items), 2)

        self.assertTrue(isinstance(items[0], shopping.ShoppingItem))
        self.assertTrue(isinstance(items[1], shopping.ShoppingItem))

    def test_ItemValues(self):
        clearDatabase()
        c = DBCONN.cursor()
        c.execute('INSERT INTO items VALUES (1, "Macbook", 3000.00, 300, "laptop,mac")') 
        DBCONN.commit()

        factory = shopping.ShoppingFactory(DBNAME)
        items = factory.getNextPage()

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].getName(), "Macbook")
        self.assertEqual(items[0].getPrice(), 3000.00)
        self.assertEqual(items[0].getNumberSold(), 300)
        
        tags = items[0].getTags() #putting tags in a variable
        self.assertEqual(len(tags), 2)  #length of this tag = 2
        self.assertTrue("laptop" in tags and "mac" in tags)
    
    def test_sortMostSold(self):
        clearDatabase()
        c = DBCONN.cursor()
        c.execute('INSERT INTO items VALUES (1, "Macbook", 3000.00, 2, "laptop,mac")') 
        c.execute('INSERT INTO items VALUES (2, "PC", 3000.00, 5, "laptop,mac")')
        c.execute('INSERT INTO items VALUES (3, "Phone", 3000.00, 3, "laptop,mac")')
        DBCONN.commit()

        factory = shopping.ShoppingFactory(DBNAME)
        factory.sortMostSold()

        items = factory.getNextPage()

        self.assertEqual(len(items), 3)
        self.assertEqual(items[0].getName(), "PC")
        self.assertEqual(items[1].getName(), "Phone")
        self.assertEqual(items[2].getName(), "Macbook")
    

    def test_setSearch(self):
        clearDatabase()
        c = DBCONN.cursor()
        c.execute('INSERT INTO items VALUES (1, "Macbook", 3000.00, 2, "laptop,mac")') 
        c.execute('INSERT INTO items VALUES (2, "PC", 3000.00, 5, "dog,cat")')
        c.execute('INSERT INTO items VALUES (3, "Phone", 3000.00, 3, "phone,cell")')
        DBCONN.commit()

        factory = shopping.ShoppingFactory(DBNAME)
        factory.setSearchFilter(["laptop", "lollipop"])
        items = factory.getNextPage()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].getName(), "Macbook")


    def test_sortLowestPrice(self):
        clearDatabase()
        c = DBCONN.cursor()
        c.execute('INSERT INTO items VALUES (1, "Macbook", 100.00, 2, "laptop,mac")') 
        c.execute('INSERT INTO items VALUES (2, "PC", 300.00, 5, "laptop,mac")')
        c.execute('INSERT INTO items VALUES (3, "Phone", 433.00, 3, "laptop,mac")')
        DBCONN.commit()

        factory = shopping.ShoppingFactory(DBNAME)
        factory.sortLowestSold()

        items = factory.getNextPage()
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0].getName(), "Macbook")
        self.assertEqual(items[1].getName(), "PC")
        self.assertEqual(items[2].getName(), "Phone")
    
    def test_Reviews(self):
        clearDatabase()
        c = DBCONN.cursor()
        c.execute('INSERT INTO items VALUES (1, "Macbook", 100.00, 2, "laptop,mac")')
        c.execute('INSERT INTO reviews VALUES (1, 2, "This is sucks", "mike")')
        c.execute('INSERT INTO reviews VALUES (1, 5, "This is awesome", "mike")')
        c.execute('INSERT INTO reviews VALUES (1, 4, "This is ok", "mike")')
        DBCONN.commit()

        factory = shopping.ShoppingFactory(DBNAME)
        items = factory.getNextPage()
        self.assertEqual(len(items), 1)

        reviews = items[0].getReviews()
        self.assertEqual(len(reviews), 3)


        #attempting to test get buyers and make sure the first buyer is mike however we have some issues following this:
    # def test_getBuyers(self):
    #     clearDatabase()
    #     c = DBCONN.cursor()
    #     c.execute('INSERT INTO reviews VALUES (1, 2, "This is sucks", "mike")')
    #     c.execute('INSERT INTO reviews VALUES (2, 5, "This is awesome", "tony")')
    #     c.execute('INSERT INTO reviews VALUES (3, 4, "This is ok", "Jeffrey Dahmer")')
    #     DBCONN.commit()

    #     factory = shopping.ShoppingFactory(DBNAME)
    #     items = factory.getNextPage()
        
    #     self.assertEqual(items[1].getBuyers(), "tony")
        


        



unittest.main()

