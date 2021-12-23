import csv
import mysql.connector
import datetime
import json
from mysql.connector import Error
from datetime import date

hostname=''
db=''
username=''
pw=''

statusMap = {
    0 : "Checked Out",
    1: "Returned On Time",
    2: "Returned Over Due"
}

branchMap = {
    1:'cen',2:'qna',3:'lcy',4:'bea',5:'gwd',6:'nga',7:'wts',8:'mon',9:'rbe',10:'net',11:'glk',
    12:'bro',13:'swt',14:'cap',15:'mgm',16:'dlr',17:'uni',18:'bal', 19:'col',20:'spa',21:'dth',22:'hip',23:'mag',
    24:'fre',25:'nhy',26:'wal',27:'idc',28:'mob',29:'tcs',30:'GWD',31:'ill',32:'drp1',33:'out'
}

collectionMap = {
    1: 'cs6r', 2: 'camus', 3: 'canf', 4: 'nanf', 5: 'caln', 6: 'cs7r', 7: 'naaar', 8: 'ncpic', 9: 'nacd', 10: 'cs8r', 
    11: 'nafic', 12: 'cacd', 13: 'ccpic', 14: 'nadvdnf', 15: 'namys', 16: 'ncnf', 17: 'ncrdr', 18: 'caref', 19: 'nacdnf', 20: 'canew', 
    21: 'nacomic', 22: 'nanew', 23: 'cabocd', 24: 'nycomic', 25: 'nyfic', 26: 'ncenf', 27: 'natxtr', 28: 'ncef', 29: 'nynf', 30: 'caaero', 
    31: 'cab', 32: 'nadvd', 33: 'nabocd', 34: 'nasf', 35: 'ncln', 36: 'ncdvd', 37: 'ncbocd', 38: 'ncfft', 39: 'cs9g', 40: 'ccnf', 
    41: 'nchol', 42: 'nyser', 43: 'nccd', 44: 'camys', 45: 'cs9r', 46: 'ncnew', 47: 'cabr', 48: 'ccfic', 49: 'calibr', 50: 'ncfic', 
    51: 'nccomic', 52: 'cadvd', 53: 'ccser', 54: 'cs1malp', 55: 'cafic', 56: 'nybocd', 57: 'cccd', 58: 'naref', 59: 'ccln', 60: 'nab', 
    61: 'pknf', 62: 'capf', 63: 'najob', 64: 'cyb', 65: 'cacomic', 66: 'calpfic', 67: 'casf', 68: 'cs3fic', 69: 'ccb', 70: 'ccdvd', 
    71: 'naln', 72: 'cs1malf', 73: 'nalpfic', 74: 'ncref', 75: 'nalndvd', 76: 'cadesk3', 77: 'cycomic', 78: 'ncb', 79: 'cccomic', 80: 'ncdvdnf', 
    81: 'cacdnf', 82: 'cybocd', 83: 'naover', 84: 'cs7ro', 85: 'ncser', 86: 'ccfft', 87: 'casear', 88: 'cynf', 89: 'nynew', 90: 'naaanf', 
    91: 'naglc', 92: 'calndvd', 93: 'ccdvdnf', 94: 'cadvdnf', 95: 'caover', 96: 'naaab', 97: 'ncaafam', 98: 'cadesk8', 99: 'ccaward', 
    100: 'cs8ro', 101: 'caaeroc', 102: 'cadesk6', 103: 'cyfic', 104: 'nalpnf', 105: 'ccrdr', 106: 'cawest', 107: 'cadesk9', 108: 'cylp', 109: 'caatlas', 
    110: 'cass', 111: 'cchol', 112: 'carefo', 113: 'namar', 114: 'cash', 115: 'ncaward', 116: 'ccef', 117: 'calnr', 118: 'nclp', 119: 'naaafic', 120: 'ccbocd', 
    121: 'cs9go', 122: 'nawest', 123: 'nahol', 124: 'cckit', 125: 'ncpb', 126: 'caref8', 127: 'pkfic', 128: 'nalpnew', 129: 'calncd', 
    130: 'casbr', 131: 'caaerop', 132: 'calpnf', 133: 'cacdrr', 134: 'careadr', 135: 'caeslr', 136: 'naatlas', 137: 'najobr', 138: 'naatlr', 139: 'ccdesk', 140: 'cs9ro', 
    141: 'cs1lewr', 142: 'nass', 143: 'cs8rf', 144: 'nyb', 145: 'caref9f', 146: 'cs8rx', 147: 'naaanew', 148: 'cs9gf', 149: 'cadesk7', 150: 'caaeroo', 
    151: 'cs6ro', 152: 'napar', 153: 'cynew', 154: 'ncholsk', 155: 'caref9', 156: 'nylp', 157: 'nacon', 158: 'nadocr', 159: 'camapr', 
    160: 'namarr', 161: 'ccref', 162: 'cs6rf', 163: 'cs7rf', 164: 'nabr', 165: 'cclpfic', 166: 'napro', 167: 'nasbr', 168: 'narefsl', 169: 'nyref', 
    170: 'naconr', 171: 'nacdr', 172: 'calncas', 173: 'calnvid', 174: 'cacon', 175: 'naenvr', 176: 'nypb', 177: 'nahmwk', 178: 'nanar', 179: 'cadesk5', 180: 'nadesk', 
    181: 'nahmwkr', 182: 'navidg', 183: 'cyser', 184: 'nana', 185: 'navidgr', 186: 'ncaa', 187: 'cavidnf', 188: 'naaapb', 189: 'ncbb', 190: 'cs1lew', 
    191: 'napclbr', 192: 'cs1fic', 193: 'ccnew'
}

typeMap = {
    1: 'arbk', 2: 'acmus', 3: 'acbk', 4: 'arper', 5: 'jcbk', 6: 'accd', 7: 'acdvd', 8: 'jcdvd', 9: 'jccd', 
    10: 'pkbknh', 11: 'jrbk', 12: 'acmap', 13: 'acvhs', 14: 'armus', 15: 'drper', 16: 'bcbk', 17: 'arcdrom', 18: 'jcmus', 19: 'ucunkn', 
    20: 'arpost', 21: 'armap', 22: 'jrmus', 23: 'armfc', 24: 'jrcd', 25: 'dcillb', 26: 'arnp', 27: 'areq', 28: 'acper', 29: 'ackit', 
    30: 'atablet', 31: 'aceq', 32: 'accas', 33: 'bccd', 34: 'jckit', 35: 'acslide', 36: 'ardvd', 37: 'arpam', 38: 'accdrom', 39: 'alaptop', 
    40: 'arkit', 41: 'ardisk', 42: 'ucunknj', 43: 'xrbk', 44: 'drbk', 45: 'drord', 46: 'aceqnh', 47: 'drmfc', 48: 'acart', 49: 'ahbk', 
    50: 'arvhs', 51: 'arcd', 52: 'acpost', 53: 'bccas', 54: 'acpam', 55: 'acunkn', 56: 'arphoto', 57: 'jrper', 58: 'areqnh', 59: 'arcas', 
    60: 'jccas', 61: 'drcdrom', 62: 'bcdvd', 63: 'acphoto'
}

checkOutResponseTemplate = {
    "Library Card" : 0,
    "Bib Number" : 0,
    "Title" : "",
    "Checkout Date" : "",
    "CheckIn Date" : "",
    "Due Date" : "",
    "Status" : 0,
    "Branch" : 0
}

booksCountResponseTemplate = {
    "Library Card" : 0,
    "Number of Books Checked Out" : 0
}

checkInResponseTemplate = {
    "Library Card" : 0,
    "Bib Number" : 0,
    "Title" : "",
    "Checkout Date" : "",
    "CheckIn Date" : "",
    "Status" : 0,
    "Branch" : 0
}

failResponseTemplate = {
    "Error" : "Unable to execute query",
    "Status": False
}

readResponseTemplate = {
    "Status": False,
    "Response" : ""
}
def checkUserCount():
    query = f"select max(libraryCard) from User;"
    args = ()
    response = executReadQuery(query, args, True, False)
    if(response["Status"]):
        return int(str(response["Response"]).strip("(").strip(",)"))
    else:
        return failResponseTemplate

def checkUserEmpty():
    query = f"select count(libraryCard) from User;"
    args = ()
    response = executReadQuery(query, args, True, False)
    if(response["Status"]):
        return int(str(response["Response"]).strip("(").strip(",)"))
    else:
        return failResponseTemplate

def checkUserExist(libraryCard):
    query = f"select count(*) from User where libraryCard="+libraryCard+";"
    args = ()
    response = executReadQuery(query, args, True, False)
    if(response["Status"]):
        return int(str(response["Response"]).strip("(").strip(",)"))
    else:
        return failResponseTemplate

def checkUserPassword(libraryCard, password):
    query = f"select password from User where libraryCard=" + libraryCard
    args = ()
    response = executReadQuery(query, args, True, False)
    if(response["Status"]):
        if str(response["Response"]).strip("('").strip("',)") == str(password):
            return True
        else:
            return False 
    else:
        return failResponseTemplate

# returns book count for same bibnumber
def bookCount(BibNumber):
    query = f"select count(*) from Book where BibNumber=" + str(BibNumber) + ";"
    args = ()
    response = executReadQuery(query, args, True, False)
    if(response["Status"]):
        return int(str(response["Response"]).strip("(").strip(",)"))
    else:
        return failResponseTemplate

# returns book count for same exact book
def exactBookCount(BibNumber, ItemType, ItemCollection, branchId):
    query = f"select count(*) from Book where BibNumber="+ str(BibNumber) +" and ItemType="+ str(ItemType) +" and ItemCollection="+ str(ItemCollection) +" and branchId="+ str(branchId) +";"
    args = ()
    response = executReadQuery(query, args, True, False)
    if(response["Status"]):
        return int(str(response["Response"]).strip("(").strip(",)"))
    else:
        return failResponseTemplate

def checkCount(BibNumber,branchID, ItemCollection, ItemType):
    query = f"select ItemCount from Book where BibNumber = {BibNumber} and branchID = {branchID} and ItemCollection = {ItemCollection} and ItemType = {ItemType};"
    args = (BibNumber,branchID, ItemCollection, ItemType)
    response = executReadQuery(query, args, True, False)
    if(response["Status"]):
        #response["Response"] = int(str(response["Response"]).strip("(").strip(",)"))
        return response
    else:
        return failResponseTemplate

def updateCount(BibNumber,branchID, ItemCollection, ItemType):
    count = checkCount(BibNumber,branchID, ItemCollection, ItemType)["Response"][0]
    query = f" Update Book set ItemCount = {count+1} where BibNumber = {BibNumber} and branchID = {branchID} and ItemCollection = {ItemCollection} and ItemType = {ItemType};"
    args = (BibNumber,branchID, ItemCollection, ItemType)
    if executUpdateQuery(query, args, True):
        return True
    else:
        return failResponseTemplate

def getTitle(BibNumber,branchID, ItemCollection, ItemType):
    query = f"select Title from Book where BibNumber = {BibNumber} and branchID = {branchID} and ItemCollection = {ItemCollection} and ItemType = {ItemType};"
    args = (BibNumber,branchID, ItemCollection, ItemType)
    response = executReadQuery(query, args, True, False)
    if(response["Status"]):
        response["Response"] = response["Response"][0].strip("(").strip(",)").split("/")[0]
        return response["Response"]
    else:
        return failResponseTemplate

def numberOfBooksCheckedOut(libraryCard):
    query = f"select booksCheckedOut from User where libraryCard = {libraryCard};"
    response = executReadQuery(query, (), True, False)
    if response["Status"] :
        booksCountResponse = booksCountResponseTemplate
        booksCountResponse["Library Card"] = libraryCard
        booksCountResponse["Number of Books Checked Out"] = response["Response"][0]
        return booksCountResponse["Number of Books Checked Out"]
    return failResponseTemplate

def updateUserCount(libraryCard, count):
    query = f"Update User set booksCheckedOut = {count} where libraryCard = {libraryCard}"
    if executUpdateQuery(query, (), True):
        return True
    return failResponseTemplate

def checkoutBook(LibraryCard, BibNumber, branchID, ItemCollection, ItemType):
    for obj in (BibNumber,branchID, ItemCollection, ItemType, LibraryCard):
        if obj == None:
            print("Incorrect/misssing information. Please ensure the data type is accurate.")
            return
        if not obj.isdigit():
            print("Incorrect/misssing information. Please ensure the data type is accurate.")
            return

    if checkUserExist(LibraryCard) < 1:
        print("This user does not exist.")
        return

    if exactBookCount(BibNumber, ItemType, ItemCollection, branchID) < 1:
        print("This book does not exist or has already been deleted.")
        return

    count = checkCount(BibNumber,branchID, ItemCollection, ItemType)["Response"][0]
    if count == 0:
        response = failResponseTemplate
        response["Response"] = "There are currently no copies available of this book. Try again with a different type or location"
        print("This book is already checked out.")
        return response
    today = date.today()
    #print(str(date.today()).replace("-", "/"))
    checkoutDate = datetime.datetime.strptime(str(date.today()).replace("-", "/"), "%Y/%m/%d")
    dueDate = checkoutDate + datetime.timedelta(days=14)
    query = """
            INSERT INTO CheckOuts(libraryCard, BibNumber, checkoutDate, checkInDate, dueDate, branchID, status, itemType, itemCollection)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
    args = (LibraryCard, BibNumber, checkoutDate, None, dueDate, branchID, 0, ItemType, ItemCollection)
    #print(checkoutDate)
    if (executUpdateQuery (query, args, False)):
        query = f" Update Book set ItemCount = {count-1} where BibNumber = {BibNumber} and branchID = {branchID} and ItemCollection = {ItemCollection} and ItemType = {ItemType};"
        args = (count-1, BibNumber,branchID, ItemCollection, ItemType)
        if executUpdateQuery(query, args, True):
            # response = checkOutResponseTemplate
            # response["Library Card"] = LibraryCard
            # response["Bib Number"] = BibNumber
            title = getTitle(BibNumber, branchID, ItemCollection, ItemType)
            # response["Title"] = title
            # response["Checkout Date"] = checkoutDate.strftime("%Y/%m/%d")
            # response["CheckIn Date"] = ""
            # response["Status"] = 0
            # response["Due Date"] = dueDate.strftime("%Y/%m/%d")
            # response["Branch"] = branchID
            print(title  + " checked out.")
            numberOfBooks = numberOfBooksCheckedOut(LibraryCard)
            updateUserCount(LibraryCard, numberOfBooks+1)
            return 
    else: 
        print("Cannot check out the book more than once a day.")
        return failResponseTemplate
#gets the most recent checkout date of a book 
def getCheckOutDate(LibraryCard, BibNumber,branchID, ItemCollection, ItemType):
    query = f"select checkoutDate from CheckOuts where libraryCard = {LibraryCard} and BibNumber = {BibNumber} and branchID = {branchID} and status = 0;"
    args = ()
    response = executReadQuery(query, args, True, False)
    if(response["Status"]):
        return response
    else:
        return failResponseTemplate

def checkInBook(LibraryCard, BibNumber, branchID, ItemCollection, ItemType):
    for obj in (LibraryCard, BibNumber, branchID, ItemCollection, ItemType):
        assert obj != None
        assert obj.isdigit()
    
    checkInDate = datetime.datetime.strptime(str(date.today()).replace("-", "/"), "%Y/%m/%d")
    checkoutDateResponse = getCheckOutDate(LibraryCard, BibNumber,branchID, ItemCollection, ItemType)
    if not checkoutDateResponse["Status"] or not checkoutDateResponse["Response"]:
        print("This book is not checked out currently.")
        return failResponseTemplate
    checkoutDate = checkoutDateResponse["Response"][0]
    overDue = ((checkInDate - checkoutDate).days > 14)
    status = {
        False: 1,
        True: 2
    }
    value = status[overDue]
    query = f"Update CheckOuts SET checkInDate = '{checkInDate}', status = {value} where libraryCard = {LibraryCard} and BibNumber = {BibNumber} and branchID = {branchID} and itemType = {ItemType} and itemCollection = {ItemCollection} and status = 0;"
    args = ()
    if(executUpdateQuery(query, args, True)):
        if not updateCount(BibNumber,branchID, ItemCollection, ItemType):
            return failResponseTemplate
        response = checkInResponseTemplate
        response["Library Card"] = LibraryCard
        response["Bib Number"] = BibNumber
        response["Title"] = getTitle(BibNumber, branchID, ItemCollection, ItemType)
        response["Checkout Date"] = checkoutDate.strftime("%Y/%m/%d")
        response["CheckIn Date"] = checkInDate.strftime("%Y/%m/%d")
        response["Status"] = status[overDue]
        response["Branch"] = branchID
        numberOfBooks = numberOfBooksCheckedOut(LibraryCard)
        updateUserCount(LibraryCard, numberOfBooks-1)
        print("The book was checked in.")
        return  response
    else: 
        return failResponseTemplate

def findBooksByCategory(categories, limit):
    query = "select BibNumber, Title, ItemType, ItemCollection, branchID, itemCount from Book "
    ItemType = ""
    CollectionType = ""
        
    if len(categories) == 2:
        # if not categories[0] in typeMap or not categories[1] in collectionMap:
        #     print("Categories are incorrect.")
        #     return
        for itemType in typeMap.keys():
            if typeMap[itemType] == categories[0]:
                ItemType = itemType
        for collectionType in collectionMap.keys():
            if collectionMap[collectionType] == categories[1]:
                CollectionType = collectionType
        query  = query + f"where ItemType = {ItemType} and ItemCollection = {CollectionType} limit {limit}"
    if len(categories) == 1:
        # if not categories[0] in typeMap and not categories[0] in collectionMap:
        #     print("Category is incorrect.")
        #     return
        for itemType in typeMap.keys():
            if typeMap[itemType] == categories[0]:
                ItemType = itemType
                query  = query + f"where ItemType = {ItemType} limit {limit}"
        for collectionType in collectionMap.keys():
            if collectionMap[collectionType] == categories[0]:
                CollectionType = collectionType
                query  = query + f"where ItemCollection = {CollectionType} limit {limit}"            

    books = executReadQuery(query, (), True, True)

    if books["Status"]:
        with open('result.csv', 'w') as filtered_books:
            results = csv.writer(filtered_books, delimiter = ",")
            results.writerow(["BibNumber","Title","ItemType","ItemCollection","branchID","itemCount"])
            for book in books["Response"]:
                results.writerow([book[0], book[1].split("/")[0], book[2], book[3], book[4], book[5]])
            filtered_books.close()
            return True
    else:
        return failResponseTemplate
def searchByBib(BibNumber):
    if BibNumber == None:
        print("Incorrect/misssing information. Please ensure the data type is accurate.")
        return
    if not BibNumber.isdigit():
        print("Incorrect/misssing information. Please ensure the data type is accurate.")
        return

    query = f"select Title, ISBN, Author, Publisher, PublishYear, Subject, ItemCollection, ItemType, branchID, ItemCount from Book where BibNumber = {BibNumber}"
    args = (BibNumber)
    response = executReadQuery(query, args, True, True)
    # print(response)
    if(response["Status"]):
        with open('result.csv', 'w', encoding="utf-8") as filtered_books:
            results = csv.writer(filtered_books, delimiter = ",")
            results.writerow(["Title", "ISBN", "Author", "Publisher", "PublishYear", "Subject", "ItemCollection", "ItemType", "branchID", "ItemCount"])
            for book in response["Response"]:
                results.writerow([book[0], book[1].split("/")[0], book[2], book[3], book[4], book[5], book[6], book[7], book[8], book[9]])
            filtered_books.close()
            return True
    else:
        return failResponseTemplate

def searchBook(searchString):
    query = f"select BibNumber, Title, ISBN, Author, Publisher, PublishYear, Subject, ItemType, ItemCollection, branchID from Book where Title regexp '{searchString}'"
    args = (searchString)
    response = executReadQuery(query, args, True, True)
    # print(response)
    if(response["Status"]):
        with open('result.csv', 'w', encoding="utf-8") as filtered_books:
            results = csv.writer(filtered_books, delimiter = ",")
            results.writerow(["BibNumber","Title","ISBN","Author","Publisher","PublishYear","Subject","ItemType","ItemCollection","branchID"])
            for book in response["Response"]:
                results.writerow([book[0], book[1].split("/")[0], book[2], book[3], book[4], book[5], book[6], book[7], book[8], book[9]])
            filtered_books.close()
            return True
    else:
        print("No books were found.")
        return failResponseTemplate

def getGoodReads(BibNumber):
    args = ("dummy")
    query = f"select distinct ISBN from ISBNs where BibNumber={BibNumber};"
    response = executReadQuery(query, args, True, True)
    print(response)
    if(response["Status"]):
        for isbn in response["Response"]:
            print(isbn[0])
            query = f"select * from GoodReads where ISBN='{isbn[0]}'"
            response = executReadQuery(query, args, True, False)
            if(response["Status"]):
                if(response["Response"]):
                    with open('result.csv', 'w') as filtered_books:
                        book = response["Response"]
                        print(book)
                        res = []
                        for entry in book:
                            if entry == None:
                                res.append('')
                            else:
                                res.append(entry)
                        results = csv.writer(filtered_books, delimiter = ",")
                        results.writerow(res)
                        filtered_books.close()
                        return True
            else:
                return failResponseTemplate
        return {"Error": "Could not find item in GoodReads database"}
    return failResponseTemplate

def getReviews(BibNumber):
    if BibNumber == None:
        print("Incorrect/misssing information. Please ensure the data type is accurate.")
        return
    if not BibNumber.isdigit():
        print("Incorrect/misssing information. Please ensure the data type is accurate.")
        return

    args = ("dummy")
    query = f"select userName, libraryCard, rating, reviewText from LibraryReview inner join User using (libraryCard) where BibNumber = {BibNumber}"
    response = executReadQuery(query, args, True, 1)
    if(response["Status"]):
        return response
    else:
        return failResponseTemplate

def BooksCheckedOut(libraryCard):
    if libraryCard == None:
        print("Incorrect/misssing information. Please ensure the data type is accurate.")
        return
    if not libraryCard.isdigit():
        print("Incorrect/misssing information. Please ensure the data type is accurate.")
        return
        
    query = f"select BibNumber, checkoutDate, checkInDate, Status, itemType, itemCollection, branchID from CheckOuts where libraryCard = {libraryCard};"
    response = executReadQuery(query, (), True, True)
    if response["Status"]:
        bibs = []
        with open("result.csv", "w") as records_csv:
            records = csv.writer(records_csv, delimiter = ",")
            records.writerow(["BibNumber", "CheckOutDate", "CheckInDate", "Status", "Type", "Collection", "Branch"])
            for record in response["Response"]:
                records.writerow([record[0], record[1], record[2], statusMap[record[3]], record[4], record[5], record[6]])
            records_csv.close()
        return True
    else:
        return failResponseTemplate


#this function takes care of all NON - MODIFYING queries (reading)
#the flag "ignore" is used if you do not want to pass in an args array
def executReadQuery(query, args, ignore, all):
    try:
        connection = mysql.connector.connect(
            host=hostname,
            database=db,
            user=username,
            password=pw
        )
        if connection.is_connected():
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")
            ReadResponse = readResponseTemplate
            if ignore:
                cursor.execute(query)
                connection.commit()
            else:
                cursor.execute(query, args)
                connection.commit()
            if all:
                ReadResponse["Response"] = cursor.fetchall()
            else :
                ReadResponse["Response"] = cursor.fetchone()
            ReadResponse["Status"] = True
            return ReadResponse
        else:
            print("Please check your database connection and try again")            
            return readResponseTemplate
    except Error as e:
        return failResponseTemplate 

#this function takes care of all MODIFYING queries (writing, altering, dropping etc)
#the flag "ignore" is used if you do not want to pass in an args array
def executUpdateQuery(query, args, ignore):
    #print(query)
    try:
        connection = mysql.connector.connect(
            host=hostname,
            database=db,
            user=username,
            password=pw
        )
        if connection.is_connected():
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")
            #record = cursor.fetchone()
            if ignore:
                cursor.execute(query)
            else:
                cursor.execute(query, args)
            connection.commit()
            return True
        else:
            print("Please check your database connection and try again")
            return False
    except Error as e:
        return False

# Adding a user
def userAdd(userName, password, email):
    #Checking if values are correct
    
    #Calculating library card number
    if checkUserEmpty() == 0:
        libraryCard = 1000000000
    else:
        libraryCard = 1 + checkUserCount()

    #Executing Insert query
    query = """
    INSERT INTO User(userName, password, email, libraryCard, booksCheckedOut)
    VALUES(%s,%s, %s, %s, %s);"""
    args = (userName, password, email, libraryCard, 0)
    if (executUpdateQuery(query, args, False)):
        print("User has been added. Your library card number is: "+str(libraryCard))
        return
    else:
        return failResponseTemplate

# Removing a user
# def userDrop(libraryCard, password):
#     print("you are here!")
#     if libraryCard == None:
#             print("Incorrect/misssing information. Please ensure the data type is accurate.")
#             return
#     if not libraryCard.isdigit():
#         print("Incorrect/misssing information. Please ensure the data type is accurate.")
#         return

#     if checkUserPassword(libraryCard, password):
#         query = "DELETE FROM LibraryReview WHERE libraryCard=" + libraryCard
#         print(query)
#         args = ()
#         if (executUpdateQuery(query, args, True)):
#             print("Library reviews have been deleted.")
#             query = "DELETE FROM User WHERE libraryCard=" + libraryCard
#             print(query)
#             args = ()
#             if (executUpdateQuery(query, args, True)):
#                 print("User has been deleted.")
#                 return
#             else:
                
#                 return failResponseTemplate
#         else:
#             return failResponseTemplate
#     else:
#         print("Password or User is incorrect")

# Adding a book
def bookAdd(BibNumber, Title, Author, ISBN, Publisher, PublishYear, ItemType, Subject, ItemCollection, branchId, ItemCount):
    #Checking if values are correct
    for obj in (BibNumber, ItemType, ItemCollection, branchId, ItemCount):
        if obj == None:
            print("Incorrect/misssing information. Please ensure the data type is accurate.")
            return
        if not obj.isdigit():
            print("Incorrect/misssing information. Please ensure the data type is accurate.")
            return

    if exactBookCount(BibNumber, ItemType, ItemCollection, branchId) != 0:
        print("This book already exists. Please delete the record if you wish to add a new one.")
        return

    #Executing Insert query
    query = """
    INSERT INTO Book
    (BibNumber, Title, Author, ISBN,Publisher, PublishYear, ItemType, Subject, ItemCollection, branchID, ItemCount)
    VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    args = (BibNumber, Title, Author, ISBN, Publisher, PublishYear, ItemType, Subject, ItemCollection, branchId, ItemCount)
    if (executUpdateQuery(query, args, False)):
        print("Book has been added.")
        return
    else:
        return failResponseTemplate

# Removing a book
def bookDrop(BibNumber, ItemType, ItemCollection, branchId, password):
    #Checking if values are correct
    for obj in (BibNumber, ItemType, ItemCollection, branchId):
        if obj == None:
            print("Incorrect/misssing information. Please ensure the data type is accurate.")
            return
        if not obj.isdigit():
            print("Incorrect/misssing information. Please ensure the data type is accurate.")
            return

    if bookCount(BibNumber) < 1:
        print("This book does not exist or has already been deleted.")
        return

    #Executing Insert query
    if password == "12321":
        query = "DELETE FROM CheckOuts WHERE BibNumber="+ BibNumber +" AND ItemType="+ ItemType +" AND ItemCollection="+ ItemCollection + " AND branchID="+ branchId +";"
        args = ()
        if (executUpdateQuery(query, args, True)):
            query = "DELETE FROM Book WHERE BibNumber="+ BibNumber +" AND ItemType="+ ItemType +" AND ItemCollection="+ ItemCollection + " AND branchID="+ branchId +";"
            args = ()
            if (executUpdateQuery(query, args, True)):
                print("Book has been deleted.")
                return
            else:
                return failResponseTemplate
        else:
            return failResponseTemplate
    else:
        print("Password is incorrect please try again later.") 

# Adding a review
def reviewAdd(BibNumber, Rating, Review, libraryCard, password):
    #Checking if values are correct
    for obj in (BibNumber, libraryCard, Rating):
        if obj == None:
            print("Incorrect/misssing information. Please ensure the data type is accurate.")
            return
        if not obj.isdigit():
            print("Incorrect/misssing information. Please ensure the data type is accurate.")
            return

    if checkUserPassword(libraryCard, password):

        if (int(Rating) > 5 or int(Rating) < 0):
            print("Incorrect Rating score. Please try again later.")
            return

        if bookCount(BibNumber) < 1:
            print("This book does not exist.")
            return
        
        if reviewCount(BibNumber, libraryCard ) > 0:
            print("You already have a review. Please edit that review instead.")
            return

        #Executing Insert query
        query = """
        INSERT INTO LibraryReview
        (BibNumber, rating, reviewText, libraryCard)
        VALUES(%s,%s, %s, %s);"""
        args = (BibNumber, Rating, Review, libraryCard)
        if (executUpdateQuery(query, args, False)):
            print("Review has been added.")
            return
        else:
            print("Review was not added. Ensure you have entered the correct book information or do not already have a review for this book.")
            return
    else:
        print("Password or User is incorrect")

def reviewCount(BibNumber, libraryCard ):
    query = f"select count(*) from LibraryReview where BibNumber=" + BibNumber + " and libraryCard=" + libraryCard +";"
    args = ()
    response = executReadQuery(query, args, True, False)
    if(response["Status"]):
        return int(str(response["Response"]).strip("(").strip(",)"))
    else:
        return failResponseTemplate

# Removing a review
def reviewDrop(BibNumber,libraryCard, password):
    #Checking if values are correct
    for obj in (BibNumber, libraryCard):
        if obj == None:
            print("Incorrect/misssing information. Please ensure the data type is accurate.")
            return
        if not obj.isdigit():
            print("Incorrect/misssing information. Please ensure the data type is accurate.")
            return

    if checkUserPassword(libraryCard, password):

        if bookCount(BibNumber) < 1:
            print("This book does not exist.")
            return

        if reviewCount(BibNumber, libraryCard ) < 1:
            print("You have no review to delete.")
            return
            

        #Executing Insert query
        query = "delete from LibraryReview where BibNumber=" + BibNumber + " and libraryCard="+ libraryCard +";"
        args = ()
        if (executUpdateQuery(query, args, True)):
            print("Review has been deleted.")
            return
        else:
            print("Review was not deleted. Ensure you have entered the correct book information or that you do have a review for this book.")
            return 
    else:
        print("Password or User is incorrect")

# Editing a review
def reviewEdit(BibNumber, Rating, Review, libraryCard, password):
    #Checking if values are correct
    for obj in (BibNumber, libraryCard, Rating):
        if obj == None:
            print("Incorrect/misssing information. Please ensure the data type is accurate.")
            return
        if not obj.isdigit():
            print("Incorrect/misssing information. Please ensure the data type is accurate.")
            return

    if checkUserPassword(libraryCard, password):
        
        if (int(Rating) > 5 or int(Rating) < 0):
            print("Incorrect Rating score. Please try again later.")
            return

        if bookCount(BibNumber) < 1:
            print("This book does not exist.")
            return

        if reviewCount(BibNumber, libraryCard ) < 1:
            print("You have no review to edit.")
            return

        #Executing Insert query
        query = "update LibraryReview set rating="+ Rating +", reviewText=\'"+ Review +"\' where BibNumber=" + BibNumber + " and libraryCard="+ libraryCard+ ";"
        args = ()
        if (executUpdateQuery(query, args, False)):
            print("Review has been updated.")
            return
        else:
            print("Review was not updated. Ensure you have entered the correct book information or do not already have a review for this book.")
            return failResponseTemplate
    else:
        print("Password or User is incorrect")

#Searching prev records
def searchRecords(BibNumber):
   
    if BibNumber == None:
        print("Incorrect/misssing information. Please ensure the data type is accurate.")
        return
    if not BibNumber.isdigit():
        print("Incorrect/misssing information. Please ensure the data type is accurate.")
        return

    query = f"select * from Records where BibNumber={BibNumber};"
    #query = f"select * from CheckOuts;"
    response = executReadQuery(query, (), True, True)
    if response["Status"]:
        with open ("records.csv", "w") as records_csv:
            records = csv.writer(records_csv, delimiter=',')
            records.writerow(["BibNumber", "ItemType", "ItemCollection", "CallNumber", "CheckoutDateTime"])
            for record in response["Response"]:
                records.writerow([record[0], record[1], record[2], record[3], record[4]])
            records_csv.close
        return True
    else:
        return failResponseTemplate



def main():
    command = ""
    print("Welcome to the 356 Books:")
    while command != "exit":
        print("------------------------------------------------------------")
        print("Please enter one for the following commands:")
        print("user - allows you to either add a user or see checkout books.")
        print("book - allows you to either add or delete a book.")
        print("review - allows you to either add, delete, view, or edit a review.")
        print("checkout - allows you to checkout a book.")
        print("checkin - allows you to checkin a book.")
        print("checkouts - returns the checkout records for a user.")
        print("search - helps a user find the book they are looking for.")
        print("------------------------------------------------------------")
        print("")
        command = input("option: ")
        # print(bookCount(123123))
        # print(exactBookCount(123123, 1, 1, 2))
        if command == 'user':
            print("Please enter \"add\", \"check\": ")
            command = input("option: ")
        
            if command == 'add':
                userName = input("username: ")
                password = input("password: ")
                email = input("email: ")
                print("")
                userAdd(userName, password, email)
            # elif command == 'delete':
            #     libraryCard = input("librarycard: ")
            #     password = input("password: ")
            #     print("")
            #     userDrop(libraryCard, password)
            elif command == 'check':
                libraryCard = input("librarycard: ")
                numBooks = numberOfBooksCheckedOut(libraryCard)
                print("")
                print("You have "+str(numBooks)+" book(s) checkedout currently.")
            else:
                print("Incorrect command.")
        elif command == 'book':
            print("Please enter \"add\" or \"delete\": ")
            command = input("option: ")
        
            if command == 'add':
                BibNumber = input("Bibnumber(int): ")
                Title = input("Title(text): ")
                Author = input("Author(text): ")
                ISBN = input("ISBN(text): ")
                Publisher = input("Publisher(text): ")
                PublishYear = input("Publish Year(text): ")
                ItemType = input("Item Type(int): ")
                Subject = input("Subject(text): ")
                ItemCollection = input("Item Collection(int): ")
                branchId = input("branchId(int): ")
                ItemCount = input("Item Count(int): ")
                print("")
                bookAdd(BibNumber, Title, Author, ISBN, Publisher, PublishYear, ItemType, Subject, ItemCollection, branchId, ItemCount)
            elif command == 'delete':
                BibNumber = input("Bibnumber(int): ")
                ItemType = input("Item Type(int): ")
                ItemCollection = input("Item Collection(int): ")
                branchId = input("branchId(int): ")
                password = input("admin password(12321): ")
                print("")
                bookDrop(BibNumber, ItemType, ItemCollection, branchId, password)
            else:
                print("Incorrect command.")
        elif command == 'review':
            print("Please enter \"add\", \"edit\", \"view\", or \"delete\": ")
            command = input("option: ")
        
            if command == 'add':
                BibNumber = input("Bibnumber(int): ")
                Rating = input("Rating(int 0-5): ")
                Review = input("Review(text): ")
                libraryCard = input("librarycard: ")
                password = input("password: ")
                print("")
                reviewAdd(BibNumber, Rating, Review, libraryCard, password)
            elif command == 'edit':
                BibNumber = input("Bibnumber(int): ")
                Rating = input("Rating(int 0-5): ")
                Review = input("Review(text): ")
                libraryCard = input("librarycard: ")
                password = input("password: ")
                print("")
                reviewEdit(BibNumber, Rating, Review, libraryCard, password)
            elif command == 'delete':
                BibNumber = input("Bibnumber(int): ")
                libraryCard = input("librarycard: ")
                password = input("password: ")
                print("")
                reviewDrop(BibNumber,libraryCard, password)
            elif command == 'view':
                BibNumber = input("Bibnumber(int): ")
                count = 0
                rating = 0
                print("")
                print("Reviews:")
                for i in getReviews(BibNumber)['Response']:
                    print(i)
                    rating += i[2]
                    count += 1
                if(count > 0): 
                    print(f"Average rating: {rating/count} out of {count} reviews")
            else:
                print("Incorrect command.")
        elif command == 'checkout':
            LibraryCard = input("LibraryCard(int): ")
            BibNumber = input("Bibnumber(int): ")
            ItemType = input("Item Type(int): ")
            ItemCollection = input("Item Collection(int): ")
            branchId = input("branchId(int): ")
            print("")
            checkoutBook(LibraryCard, BibNumber,branchId, ItemCollection, ItemType)
        elif command == 'checkin':
            LibraryCard = input("LibraryCard(int): ")
            BibNumber = input("Bibnumber(int): ")
            ItemType = input("Item Type(int): ")
            ItemCollection = input("Item Collection(int): ")
            branchId = input("branchId(int): ")
            print("")
            checkInBook(LibraryCard, BibNumber,branchId, ItemCollection, ItemType)
        elif command == 'checkouts':
            LibraryCard = input("LibraryCard(int): ")
            print("")
            print("The results are in the result.csv file.")
            BooksCheckedOut(LibraryCard)
        elif command == 'search':
            print("Please enter \"category\", \"goodreads\", \"bibnumber\", \"records\" or \"title\": ")
            command = input("option: ")
            if command == 'category':
                command = input("How many categories would you like to use: 1 or 2: ")
                if (command == "1"):
                    Category = input("Item/CollectionType(text): ")
                    Limit = input("Limit(int): ")
                    findBooksByCategory([Category], Limit)
                    print("")
                    print("The results are in the result.csv file.")
                elif (command == "2"):
                    Category1 = input("ItemType(text): ")
                    Category2 = input("ItemCollection(text): ")
                    Limit = input("Limit(int): ")
                    findBooksByCategory([Category1, Category2], Limit)
                    print("")
                    print("The results are in the result.csv file.")
                else:
                    print("")
                    print("Incorrect command.")

            elif command == 'title':
                Title = input("Title(text): ")
                print("")
                if searchBook(Title) != failResponseTemplate:
                    print("The results are in the result.csv file.")
            elif command == 'goodreads':
                command = input("BibNumber: ")
                print("")
                getGoodReads(command)
            elif command == "bibnumber":
                BibNumber = input("BibNumber: ")
                print("")
                if searchByBib(BibNumber) != failResponseTemplate:
                    print("The results are in the result.csv file.")
            elif command == "records":
                BibNumber = input("BibNumber: ")
                print("")
                if searchRecords(BibNumber) != failResponseTemplate:
                    print("The results are in the records.csv file.")
            else:
                print("Incorrect command.")
        elif command == "exit":
            break
        else:
            print("Incorrect command.")
    

    #PARSE USER INPUT HERE AND ADD FUNCTIONS

if __name__ == "__main__":
    main()
