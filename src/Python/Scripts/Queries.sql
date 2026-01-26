create database Scrapper
collate Cyrillic_General_100_CI_AI
GO

use Scrapper
go

create table dbo.Shops
(
    Id       int          not null
        constraint PK_dbo_Shops
            primary key,
    ShopName varchar(100) not null
        constraint UQ_dbo_Shops__ShopName
            unique
)
go

insert into dbo.Shops
    (Id, ShopName)
values
    (1, 'DNS'),
    (2, 'Sitilink'),
    (3, 'Regard')
GO

create table dbo.GPUs
(
    Id                bigint identity
        constraint PK_dbo_GPUs
            primary key,
    Name              varchar(255)            not null,
    GraphicsProcessor varchar(100)            not null,
    Cores             int                     not null,
    TMUS              int                     not null,
    ROPS              int                     not null,
    MemorySize        varchar(100)            not null,
    MemoryType        varchar(100)            not null,
    BusWidth          varchar(100)            not null,
    ImagePath         varchar(100) default '' not null
)
go

create table dbo.RawData
(
    Id          bigint identity
        constraint PK_dbo_RawData
            primary key,
    ProductName varchar(255)                                        not null,
    Price       int                                                 not null,
    ShopId      int                                                 not null
        constraint FK_dbo_RawData__dbo_Shops
            references Shops,
    InsertDate  datetime2(3)
        constraint DF_dbo_RawData__InsertDate default sysdatetime() not null,
    CategoryId  bigint
        constraint FK_dbo_RawData__dbo_GPUs
            references GPUs
)
go

create index IX_dbo_RawData__InsertDate
    on dbo.RawData (InsertDate)
go