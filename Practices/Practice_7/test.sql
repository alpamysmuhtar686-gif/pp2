-- copy kostroma_users(email, username, last_activity, register_date, user_state, message_count, receive_admin_email, is_banned, is_staff, user_group_id)
-- from '/data.csv'
-- delimiter ','
-- csv header;

select * from kostroma_users;
CREATE TABLE if not exists contacts (
    contact_id SERIAL PRIMARY KEY,
    contact_first_name varchar(255) not null,
    contact_last_name varchar(255),
    contact_number varchar(15) not null unique,
    contact_email varchar(511),
    contact_extra_info varchar(255)
)