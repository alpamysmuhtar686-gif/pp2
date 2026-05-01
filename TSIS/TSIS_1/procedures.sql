-- Procedure 1: Single insertion of an user
create or replace procedure insert_user(
    first_name varchar(255),
    last_name varchar(255),
    cnumber varchar(15),
    email varchar(511),
    extra_info varchar(255),
    birthday date,
    phone_type varchar(10)
)
language plpgsql as $$
declare
    existing_id int;
begin

    -- 1. check contact
    select contact_id into existing_id
    from contacts
    where contact_first_name = first_name
    and contact_last_name = last_name;

    -- 2. insert or update contact
    if found then
        update contacts
        set contact_email = email,
            contact_extra_info = extra_info
        where contact_id = existing_id;
    else
        insert into contacts(
            contact_first_name,
            contact_last_name,
            contact_number,
            contact_email,
            contact_extra_info,
            birthday
        )
        values (
            first_name,
            last_name,
            cnumber,
            email,
            extra_info,
            birthday
        )
        returning contact_id into existing_id;
    end if;

    -- 3. UPSERT phone (replace if same type exists)
    insert into phones(contact_id, phone_number, phone_type)
    values (existing_id, cnumber, phone_type)
    on conflict (contact_id, phone_type)
    do update set phone_number = excluded.phone_number;

end;
$$;

/* Procedure 2: multiple insertion through an array*/

-- DROP TYPE IF EXISTS user_type CASCADE;

-- CREATE TYPE user_type AS (
--     first_name varchar(255),
--     last_name varchar(255),
--     phone_number varchar(15),
--     email varchar(511),
--     extra_info varchar(255),
--     birthday date,
--     phone_type varchar(10)
-- );

create or replace procedure multiple_insertion(users user_type[])
language plpgsql as $$
declare
    u user_type;
    contact_id_result int;
    invalid_users user_type[] := '{}';
begin

    foreach u in array users loop

        -- validation
        if u.phone_number !~ '^[0-9]{5,15}$' then
            invalid_users := array_append(invalid_users, u);
            continue;
        end if;

        -- check if contact exists
        select contact_id into contact_id_result
        from contacts
        where contact_first_name = u.first_name
        and contact_last_name = u.last_name;

        -- insert if not exists
        if not found then
            insert into contacts(
                contact_first_name,
                contact_last_name,
                contact_number,
                contact_email,
                contact_extra_info,
                birthday
            )
            values (
                u.first_name,
                u.last_name,
                u.phone_number,
                u.email,
                u.extra_info,
                u.birthday
            )
            returning contact_id into contact_id_result;
        end if;

        -- always insert into phones
        insert into phones(contact_id, phone_number, phone_type)
        values (
            contact_id_result,
            u.phone_number,
            COALESCE(u.phone_type, 'mobile')
        );

    end loop;

    -- report invalid users
    if array_length(invalid_users, 1) > 0 then
        raise notice '[Warning] Invalid users: %', invalid_users;
    end if;

end;
$$;


-- Procedure 3: Delete user by user_name or phone_number
create or replace procedure delete_user(first_name varchar(255), last_name varchar(255), phone_number varchar(15))
language plpgsql as $$
begin
    -- check if the user exists
    if exists (select 1 from contacts where (contact_first_name=first_name and contact_last_name=last_name) or (contact_number=phone_number)) then
        delete from contacts where (contact_first_name=first_name and contact_last_name=last_name) or (contact_number=phone_number);
    else
        raise notice '[Error] The contact with first_name %, last_name % and phone_number % not found', first_name, last_name, phone_number;
    end if;

end;
$$;

/* Procedure 4: add phone */
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
BEGIN

    -- 1. find contact
    SELECT contact_id
    INTO v_contact_id
    FROM contacts
    WHERE contact_first_name = p_contact_name
      AND contact_last_name = p_last_name;

    IF NOT FOUND THEN
        RAISE NOTICE '[Error] Contact not found';
        RETURN;
    END IF;

    -- 2. insert phone
    INSERT INTO phones(contact_id, phone_number, phone_type)
    VALUES (v_contact_id, p_phone, p_type);

    RAISE NOTICE '[Success] Phone added';

END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_last_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
    v_group_id INT;
BEGIN

    -- 1. find contact
    SELECT contact_id
    INTO v_contact_id
    FROM contacts
    WHERE contact_first_name = p_contact_name
      AND contact_last_name = p_last_name;

    IF NOT FOUND THEN
        RAISE NOTICE '[Error] Contact not found';
        RETURN;
    END IF;

    -- 2. get or create group
    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    IF NOT FOUND THEN
        INSERT INTO groups(name)
        VALUES (p_group_name)
        RETURNING id INTO v_group_id;
    END IF;

    -- 3. update contact
    UPDATE contacts
    SET group_id = v_group_id
    WHERE contact_id = v_contact_id;

    RAISE NOTICE '[Success] Contact moved to group';
END;
$$;