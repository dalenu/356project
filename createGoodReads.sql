drop table if exists GoodReads;
create table GoodReads (
    Id TEXT NOT NULL,
    title VARCHAR(500),
    ISBN VARCHAR(20),
    Authors TEXT NOT NULL,
    Rating TEXT NOT NULL,
    PublishYear TEXT,
    PublishMonth TEXT,
    PublishDay TEXT,
    Publisher TEXT,
    RatingDist5 TEXT NOT NULL,
    RatingDist4 TEXT NOT NULL,
    RatingDist3 TEXT NOT NULL,
    RatingDist2 TEXT NOT NULL,
    RatingDist1 TEXT NOT NULL,
    RatingDistTotal TEXT NOT NULL,
    CountsOfReview TEXT NOT NULL, 
    Language TEXT NOT NULL,
    pagesNumber TEXT,
    Description TEXT,
    NumOfTextReviews TEXT,
    primary key (ISBN)
);

CREATE INDEX indexTitle
ON GoodReads (title, ISBN);

LOAD DATA INFILE '/var/lib/mysql-files/20-Books/goodreads1.csv' INTO TABLE GoodReads
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/20-Books/goodreads2.csv' INTO TABLE GoodReads
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/20-Books/goodreads3.csv' INTO TABLE GoodReads
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/20-Books/goodreads4.csv' INTO TABLE GoodReads
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/20-Books/records.csv' INTO TABLE Records
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(BibNumber, @dummy, ItemType, ItemCollection, CallNumber, CheckoutDateTime);

LOAD DATA INFILE '/var/lib/mysql-files/20-Books/seattle.csv' INTO TABLE Book
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(BibNumber, Title, Author, ISBN, PublishYear, Publisher, Subject, ItemType, ItemCollection, @dummy, branchID, @dummy, ItemCount);

create table preISBNs (
    BibNumber INTEGER NOT NULL,
    ISBN VARCHAR(20) NOT NULL,
    FOREIGN KEY (BibNumber) references Book(BibNumber)
);

insert ignore into preISBNs (BibNumber, ISBN)
select distinct t.BibNumber, replace(j.ISBN, ' ', '')
from book t
join json_table(
    replace(json_array(t.ISBN), ',', '","'),
    '$[*]' columns (ISBN varchar(20) path '$')
) j;

create table ISBNs (
    BibNumber INTEGER NOT NULL,
    ISBN VARCHAR(20) NOT NULL,
    PRIMARY KEY (BibNumber, ISBN),
    FOREIGN KEY (BibNumber) references Book(BibNumber),
    FOREIGN KEY (ISBN) references GoodReads(ISBN)
);

insert into ISBNs (BibNumber, ISBN) select BibNumber, ISBN from preISBNs inner join goodreads using(isbn);

drop table preISBNs;