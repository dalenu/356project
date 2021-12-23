drop table if exists LibraryReview;
drop table if exists CheckOuts;
drop table if exists Records;
drop table if exists Book;
drop table if exists User;
drop table if exists Branches;
drop table if exists ItemCollection;
drop table if exists ItemType;

create table Branches (
    branchID INTEGER PRIMARY KEY,
    branch VARCHAR(5) NOT NULL
);

create table ItemCollection(
    collectionID INTEGER PRIMARY KEY,
    collection TEXT NOT NULL
);

create table ItemType(
    typeID INTEGER PRIMARY KEY,
    type TEXT NOT NULL
);

create table User (
    userName TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    libraryCard INTEGER PRIMARY KEY,
    booksCheckedOut INTEGER NOT NULL
);

create table Book (
    BibNumber INTEGER NOT NULL,
    Title TEXT NOT NULL,
    Author TEXT,
    ISBN TEXT NOT NULL,
    Publisher TEXT,
    PublishYear TEXT,
    ItemType INTEGER NOT NULL,
    Subject TEXT,
    ItemCollection INTEGER NOT NULL,
    branchID INTEGER NOT NULL,
    ItemCount INTEGER NOT NULL,
    PRIMARY KEY (BibNumber, branchID, ItemCollection, ItemType),
    FOREIGN KEY (branchID) references Branches(branchID),
    FOREIGN KEY (ItemType) references ItemType(typeID),
    FOREIGN KEY (ItemCollection) references ItemCollection(collectionID)
);

create table LibraryReview (
    BibNumber INTEGER NOT NULL,
    rating DECIMAL(2,1) NOT NULL,
    reviewText TEXT NOT NULL,
    libraryCard INTEGER,
    PRIMARY KEY (BibNumber, libraryCard),
    FOREIGN KEY (libraryCard) references User(libraryCard),
    FOREIGN KEY (BibNumber) references Book(BibNumber)
);


create table Records(
    BibNumber INTEGER NOT NULL,
    ItemType INTEGER,
    ItemCollection INTEGER,
    CallNumber TEXT,
    CheckoutDateTime datetime NOT NULL,
    PRIMARY KEY (BibNumber, CheckoutDateTime),
    FOREIGN KEY (ItemType) references ItemType(typeID),
    FOREIGN KEY (ItemCollection) references ItemCollection(collectionID)
);

create table CheckOuts(
   libraryCard INTEGER NOT NULL,
   BibNumber INTEGER NOT NULL,
   checkoutDate datetime NOT NULL,
   checkInDate datetime,
   dueDate datetime NOT NULL,
   branchID INTEGER NOT NULL,
   status INTEGER NOT NULL,
   itemType INTEGER NOT NULL, 
   itemCollection INTEGER NOT NULL,
   primary key (libraryCard, BibNumber, checkoutDate, branchID, itemType, itemCollection),
   FOREIGN key (libraryCard) references User(libraryCard),
   FOREIGN key (branchID) references Branches(branchID),
   FOREIGN key (BibNumber, branchID, ItemCollection, ItemType) references Book(BibNumber, branchID, ItemCollection, ItemType)
)