create table dbo.Shops
(
    Id          int             not null,
    ShopName    varchar(100)    not null,

    constraint PK_dbo_Shops primary key (Id),
    constraint UQ_dbo_Shops__ShopName unique nonclustered (ShopName)
)
GO

insert into dbo.Shops
    (Id, ShopName)
values
    (1, 'DNS'),
    (2, 'Sitilink'),
    (3, 'Regard')
GO

create table dbo.RawData
(
    Id          bigint          not null    identity (1, 1),
    ProductName varchar(255)    not null,
    Price       int             not null,
    ShopId      int             not null,
    InsertDate  datetime2(3)    not null    constraint DF_dbo_RawData__InsertDate default (sysdatetime()),

    constraint PK_dbo_RawData primary key (Id),
    constraint FK_dbo_RawData__dbo_Shops foreign key (ShopId) references dbo.Shops (Id),
)
GO

create nonclustered index IX_dbo_RawData__InsertDate
on dbo.RawData
(
    InsertDate
)
GO

create table dbo.GPUs
(
    Id                  bigint          not null    identity (1, 1),
    [Name]              varchar(255)    not null,
    GraphicsProcessor   varchar(100)    not null,
    Cores               int             not null,
    TMUS                int             not null,
    ROPS                int             not null,
    MemorySize          varchar(100)    not null,
    MemoryType          varchar(100)    not null,
    BusWidth            varchar(100)    not null,
    ImagePath           varchar(100)    not null,

    constraint PK_dbo_GPUs primary key (Id)
)
GO