drop table if exists student;
drop table if exists teacher;
drop table if exists classroom;
drop table if exists batch;
drop table if exists time_slot;
drop table if exists batch_timeslot;
drop table if exists joins;
drop table if exists comment;
drop table if exists attendance;
drop table if exists fee;
drop table if exists admin;

create table student(student_id int not null auto_increment primary key, name char(100) not null, mobile char(10) not null, dateofbirth date not null, address char(100) not null, father_name char(100) not null, mother_name char(100) not null, standard int not null, school char(100) not null);
create table teacher(teacher_id int not null auto_increment primary key, password char(130) not null, name char(100) not null, mobile char(10) not null, dateofbirth date not null, address char(100) not null);
create table classroom(room_id int not null auto_increment primary key, hall_name char(100) not null, capacity int not null);
create table batch(batch_id int not null auto_increment primary key, standard int not null, subject char(100) not null, teacher_id int not null, foreign key (teacher_id) references teacher(teacher_id) on delete cascade, room_id int not null, foreign key(room_id) references classroom(room_id) on delete cascade, fee int not null);
create table time_slot(timeslot_id int not null auto_increment primary key, day char(10) not null, start_time float not null, end_time float not null);
create table batch_timeslot(batch_id int not null, foreign key (batch_id) references batch(batch_id) on delete cascade, timeslot_id int not null, foreign key (timeslot_id) references time_slot(timeslot_id) on delete cascade, primary key(batch_id,timeslot_id));
create table joins(student_id int not null, foreign key (student_id) references student(student_id) on delete cascade, batch_id int not null, foreign key (batch_id) references batch(batch_id) on delete cascade, primary key(student_id,batch_id));
create table comment(comment_id int not null auto_increment primary key, batch_id int not null, foreign key (batch_id) references batch(batch_id) on delete cascade, statement text not null, name char(100) not null, timedate datetime not null);
create table attendance(student_id int not null, batch_id int not null, foreign key (student_id,batch_id) references joins(student_id,batch_id) on delete cascade, dateofclass date not null, record char(1) not null, primary key(student_id, batch_id, dateofclass));
create table fee(receipt_id int not null auto_increment primary key, amount int not null, dateofdeposit date not null, student_id int not null, batch_id int not null, foreign key (student_id,batch_id) references joins(student_id,batch_id) on delete cascade);
create table admin(username char(100) not null, password char(130) not null);

insert into student(name,mobile,dateofbirth,address,father_name,mother_name,standard,school) values('Saurabh Rathi','9657965513','1997-08-24','Shivaji Colony','Bhagirath','Sarla',10,'Saint Paul');
insert into teacher(password, name, mobile, dateofbirth, address) values('6cb52b86f3a58e82aa9a79ef12267e422e20513693783265ff080445f73e6b2c2c04f402ba025240a4437270dee64347af73a264e6b8708509dad69296421cd0', 'Bhagirath', '1234', '1963-11-19', 'shivaji');
insert into classroom(hall_name,capacity) values('GF Hall 1', 120);
insert into batch(standard, subject, teacher_id, room_id, fee) values(10, 'Maths', 1, 1, 1000);
insert into joins(student_id, batch_id) values(1,1);
insert into time_slot(day, start_time, end_time) values('MON',8,9);
insert into batch_timeslot(batch_id,timeslot_id) values(1,1);
insert into attendance(student_id, batch_id, dateofclass, record) values (1,1,'2017-07-25','A');
insert into fee(amount,dateofdeposit,student_id,batch_id) values(200, '2017-07-01',1,1);
insert into comment(batch_id, statement, name, timedate) values(1,'Why speed of light is 3*10^8 m/s', 'Saurabh Rathi' , now());
insert into admin values('admin','b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86');

insert into time_slot(day, start_time, end_time) values('TUE',8,9);
insert into time_slot(day, start_time, end_time) values('WED',8,9);
insert into time_slot(day, start_time, end_time) values('THUR',8,9);
insert into time_slot(day, start_time, end_time) values('FRI',8,9);
insert into time_slot(day, start_time, end_time) values('SAT',8,9);
insert into batch_timeslot(batch_id,timeslot_id) values(1,3);
insert into batch_timeslot(batch_id,timeslot_id) values(1,5);
insert into attendance(student_id, batch_id, dateofclass, record) values (1,1,'2017-07-26','P');
insert into attendance(student_id, batch_id, dateofclass, record) values (1,1,'2017-07-27','P');
insert into attendance(student_id, batch_id, dateofclass, record) values (1,1,'2017-08-01','P');
insert into attendance(student_id, batch_id, dateofclass, record) values (1,1,'2017-08-02','P');
insert into fee(amount,dateofdeposit,student_id,batch_id) values(200, '2017-08-01',1,1);

