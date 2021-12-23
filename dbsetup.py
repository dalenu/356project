import csv
import mysql.connector
from mysql.connector import Error
import pandas as pd

hostname=''
db=''
username=''
pw=''

branchMap = {1:'cen',2:'qna',3:'lcy',4:'bea',5:'gwd',6:'nga',7:'wts',8:'mon',9:'rbe',10:'net',11:'glk',
            12:'bro',13:'swt',14:'cap',15:'mgm',16:'dlr',17:'uni',18:'bal', 19:'col',20:'spa',21:'dth',22:'hip',23:'mag',
            24:'fre',25:'nhy',26:'wal',27:'idc',28:'mob',29:'tcs',30:'GWD',31:'ill',32:'drp1',33:'out'}
collectionMap = {1: 'cs6r', 2: 'camus', 3: 'canf', 4: 'nanf', 5: 'caln', 6: 'cs7r', 7: 'naaar', 8: 'ncpic', 9: 'nacd', 10: 'cs8r', 
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
                191: 'napclbr', 192: 'cs1fic', 193: 'ccnew'}
typeMap = {
    1: 'arbk', 2: 'acmus', 3: 'acbk', 4: 'arper', 5: 'jcbk', 6: 'accd', 7: 'acdvd', 8: 'jcdvd', 9: 'jccd', 
    10: 'pkbknh', 11: 'jrbk', 12: 'acmap', 13: 'acvhs', 14: 'armus', 15: 'drper', 16: 'bcbk', 17: 'arcdrom', 18: 'jcmus', 19: 'ucunkn', 
    20: 'arpost', 21: 'armap', 22: 'jrmus', 23: 'armfc', 24: 'jrcd', 25: 'dcillb', 26: 'arnp', 27: 'areq', 28: 'acper', 29: 'ackit', 
    30: 'atablet', 31: 'aceq', 32: 'accas', 33: 'bccd', 34: 'jckit', 35: 'acslide', 36: 'ardvd', 37: 'arpam', 38: 'accdrom', 39: 'alaptop', 
    40: 'arkit', 41: 'ardisk', 42: 'ucunknj', 43: 'xrbk', 44: 'drbk', 45: 'drord', 46: 'aceqnh', 47: 'drmfc', 48: 'acart', 49: 'ahbk', 
    50: 'arvhs', 51: 'arcd', 52: 'acpost', 53: 'bccas', 54: 'acpam', 55: 'acunkn', 56: 'arphoto', 57: 'jrper', 58: 'areqnh', 59: 'arcas', 
    60: 'jccas', 61: 'drcdrom', 62: 'bcdvd', 63: 'acphoto'}
try:
    connection = mysql.connector.connect(host=hostname,
                                    database=db,
                                    user=username,
                                    password=pw)
    if connection.is_connected():
        cursor = connection.cursor(buffered=True)
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        fd = open('356Project.sql', 'r')
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(';')
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        for command in sqlCommands:
            try:
                if command.strip() != '':
                    cursor.execute(command)
            except Error as e:
                print("Error while connecting to MySQL", e)
        for row in branchMap:
                #print(row)
                query = """
                        INSERT INTO Branches
                        (branchID, branch)
                        VALUES(%s,%s)
                        """
                args = (row, branchMap[row])
                cursor.execute(query, args)
                connection.commit()
        for row in collectionMap:
                #print(row)
                query = """
                        INSERT INTO ItemCollection
                        (collectionID, collection)
                        VALUES(%s,%s)
                        """
                args = (row, collectionMap[row])
                cursor.execute(query, args)
                connection.commit()
        for row in branchMap:
                #print(row)
                query = """
                        INSERT INTO ItemType
                        (typeID, type)
                        VALUES(%s,%s)
                        """
                args = (row, collectionMap[row])
                cursor.execute(query, args)
                connection.commit()
                #cursor.execute("select Title from Book;")
                #connection.commit()
        connection.commit()
except Error as e:
    print("Error while connecting to MySQL", e)
# file = pd.read_pickle('collection (1).pkl').to_csv("./seattle.csv", sep=',',index=False)
# file = pd.read_csv('seattle.csv', sep =',', encoding='utf-8', engine='python')
# try:
#         connection = mysql.connector.connect(host='localhost',
#                                         database='356project',
#                                         user='root',
#                                         password='12345')
#         if connection.is_connected():
#                 cursor = connection.cursor(buffered=True)
#                 cursor.execute("select database();")
#                 record = cursor.fetchone()
#                 print("You're connected to database: ", record)
#                 cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
#                 fd = open('356Project.sql', 'r')
#                 sqlFile = fd.read()
#                 fd.close()
#                 sqlCommands = sqlFile.split(';')
#                 db_Info = connection.get_server_info()
#                 print("Connected to MySQL Server version ", db_Info)
#                 cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
#                 for command in sqlCommands:
#                         try:
#                                 if command.strip() != '':
#                                         cursor.execute(command)
#                         except Error as e:
#                                 print("Error while connecting to MySQL", e)
#                 query = """LOAD DATA LOCAL INFILE 'seattle.csv' INTO TABLE Book
#                 FIELDS TERMINATED BY ',' 
#                 ENCLOSED BY '"' 
#                 LINES TERMINATED BY '\r\n'
#                 IGNORE 1 LINES
#                 (BibNumber, Title, Author, ISBN, PublishYear, Publisher, Subject, ItemType, ItemCollection, @dummy, branchID, @dummy, ItemCount)
#                 SET LibraryUserRating = NULL
#                 SET PublishMonth = NULL
#                 SET PublishDay = NULL
#                 SET PageCount = NULL
#                 SET Status = 'availabe';"""
#                 cursor.execute(query, args)
#                 connection.commit()
#         #cursor.execute("select Title from Book;")
#         #connection.commit()            
#         connection.commit()

#                 #         books = csv.reader(csv_file, delimiter=',')
#                 # next(books)
#                 # for row in books:
#                 #         #print(row)
#                 #         query = """
#                 #                 INSERT INTO Book
#                 #                 (BibNumber, Title, Author, ISBN, LibraryUserRating, Publisher, PublishYear, PublishMonth, PublishDay, PageCount, Status, ItemType, Subject, ItemCollection, branchID, ItemCount)
#                 #                 VALUES(%s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)"""
#                 #         args = (row[0], row[1], row[2], row[3], None, row[5], row[4], None, None, None, 'available', row[7], row[6], row[8], row[10], row[12])
#                 #         cursor.execute(query, args)
#                 #         connection.commit()
#                 #         #cursor.execute("select Title from Book;")
#                 #         #connection.commit()
# except Error as e:
#         print("Error while connecting to MySQL", e)