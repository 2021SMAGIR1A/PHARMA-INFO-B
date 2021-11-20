/*==============================================================*/
/* Table : commune                                              */
/*==============================================================*/
create table commune
(
   com_id               int not null auto_increment,
   com_lib              varchar(100),
   primary key (com_id)
);

/*==============================================================*/
/* Table : pharmacie                                            */
/*==============================================================*/
create table pharmacie
(
   ph_id                int not null auto_increment,
   com_id               int not null,
   ph_nom               char(50),
   ph_adresse           varchar(200),
   ph_date              date,
   ph_long              float,
   ph_lat               float,
   primary key (ph_id),
   constraint fk_reference_1 foreign key (com_id)
      references commune (com_id) on delete restrict on update restrict
);
