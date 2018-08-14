import sqlite3
import os

class BuyerReview:
    def __init__(self, rating, review, userId):
        if type(rating) is not int:
            raise Exception("Rating should be an int")
        if rating < 1 or rating > 5:
            raise Exception("Invalid Rating")
        if type(review) is not str:
            raise Exception("Review should be a string")
        if type(userId) is not str:
            raise Exception("User ID should be a string")

        self.rating = rating
        self.review = review
        self.userId = userId
        

    def getRating(self):
        return self.rating

    
    def getReview(self):
        return self.review

    def getUserId(self):
        return self.userId

class ShoppingItem:
    def __init__(self, name, price, sold, reviews, tags, buyers):
        
        if type(name) is not str:
            raise Exception("Name should be a string")

        self.name = name 
        self.price = price
        self.sold = sold
        self.reviews = reviews
        self.tags = tags
        self.buyers = buyers

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price
    
    def getNumberSold(self):
        return self.sold
    
    def getReviews(self):
        return self.reviews

    def getTags(self):
        return self.tags

    def getBuyers(self):
        return self.buyers 
    
    def getAverageRating(self):
        tally = 0
        for review in self.reviews:
            tally += review.getRating()
        return tally / len(self.reviews)
                                            #to test addPurchase:
    def addPurchase(self, userId):          #test numberSold make sure it adds one
        self.buyers.append(userId)          #test buyers make sure userId is appended in there
        self.sold +=1                       #test bad values make sure there's no weird symbols, userId should be a string

    def addReview(self, review):
        self.reviews.append(review)
    
    def setPrice(self, price):
        self.price = price
        if type(price) is not float:
            raise Exception("Must be a float")

class ShopperAccount:
    def __init__(self, userId, orderHistory):

        if type(userId) is not str:
            raise Exception("user ID should be a string")
        if not(userId):
            raise Exception("user ID is empty")

        self.userId = userId
        self.orderHistory = orderHistory

    
    def getUserId(self):
        return self.userId
    
    def getOrderHistory(self):
        return self.orderHistory

    def addPurchase(self, item):
        self.orderHistory.append(item)


class ClothingItem(ShoppingItem):
    def __init__(self, size):

        if type(size) is not str:
            raise Exception("size must be a string")
        if len(size) >= 5 or len(size) <= 0:
            raise Exception("Size must have 1 to 4 characters")

        self.size = size

        def getSize(self):
            return self.size
         

class ShoppingFactory:
    def __init__(self, dbpath):
        if not os.path.exists(dbpath):
            raise Exception("Bad DB path")
        self.dbconn = sqlite3.connect(dbpath)
        self.cursor = self.dbconn.cursor()
        self.cursor.execute("SELECT * FROM items")
        self.pageSize = 25
    
    def setPageSize(self, size):
        if size <= 0 or size > 100:
            raise Exception("Invalid page size")
        self.pageSize = size

    def getPageSize(self):
        return self.pageSize

    def getNextPage(self):
        data = self.cursor.fetchmany(self.pageSize)  #returns a list of tuples
        items = []
        for d in data:
            tags = str(d[4]).split(',')  #instead of passing in d4, we  gon' pass in tags
            reviews = self.constructReviews(d[0])
            items.append(ShoppingItem(d[1], float(d[2]), d[3], reviews, tags, []))          #name, price, numberSold, empty review, tags, empty buyers
        return items

    def constructReviews(self, itemId):
        c = self.dbconn.cursor()
        c.execute('SELECT * FROM reviews WHERE item_id is %d' % + itemId)
        data = c.fetchall()
        reviews = []
        for d in data:
            reviews.append(BuyerReview(d[1], str(d[2]), str(d[3])))
        return reviews
        

    def sortMostSold(self):
        self.cursor.execute("SELECT * FROM items ORDER BY sold DESC")

    def sortLowestSold(self):
        self.cursor.execute("SELECT * FROM items ORDER BY price ASC")

    def setSearchFilter(self, tags):
        query = 'SELECT * FROM items WHERE'
        addQ = ''
        for tag in tags:
            if addQ:
                addQ += ' OR'
            addQ += ' tags LIKE "%' + tag + '%"'
        query += addQ
        self.cursor.execute(query)
            

    #look at what objects are returned.
