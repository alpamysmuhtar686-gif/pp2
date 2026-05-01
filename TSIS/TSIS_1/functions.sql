-- Function 1: Get the rows by pattern

create or replace function get_by_pattern(pattern_type text, pattern text)
returns table(
    first_name varchar(255),
    last_name varchar(255),
    phone_number varchar(15),
    extra_info varchar(255)
)
language plpgsql as $$
begin
    if pattern_type = 'first_name' then
        return query
        select contact_first_name, contact_last_name, contact_number, contact_extra_info
        from contacts
        where contact_first_name ilike '%' || pattern || '%';

    elsif pattern_type = 'last_name' then
        return query
        select contact_first_name, contact_last_name, contact_number, contact_extra_info
        from contacts
        where contact_last_name ilike '%' || pattern || '%';

    elsif pattern_type = 'number' then
        return query
        select contact_first_name, contact_last_name, contact_number, contact_extra_info
        from contacts
        where contact_number ilike '%' || pattern || '%';
    
    elsif pattern_type = 'email' then
        return query
        select contact_first_name, contact_last_name, contact_number, contact_extra_info
        from contacts
        where contact_email ilike '%' || pattern || '%';

    else
        raise notice '[Error]: Invalid attribute_type!';
    end if;
end;
$$;

-- Function 2: Paginate the rows
create or replace function query_pagination(rows_per_page int, page_number int)
returns table(first_name varchar(255), last_name varchar(255), phone_number varchar(15), email varchar(511), extra_info varchar(255))
language plpgsql as $$
begin
    return query
    select contact_first_name, contact_last_name, contact_number, contact_email, contact_extra_info from contacts limit rows_per_page offset (page_number - 1) * rows_per_page;
end;
$$;



CREATE OR REPLACE FUNCTION get_contacts_by_group(group_name text)
RETURNS TABLE(
    contact_id int,
    contact_first_name varchar,
    contact_last_name varchar,
    contact_email varchar,
    birthday date
)
LANGUAGE sql
AS $$
    SELECT c.contact_id,
           c.contact_first_name,
           c.contact_last_name,
           c.contact_email,
           c.birthday
    FROM contacts c
    JOIN groups g ON c.group_id = g.id
    WHERE g.name = group_name;
$$;

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    contact_id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    phone_number VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN

    RETURN QUERY

    SELECT
        c.contact_id,
        c.contact_first_name,
        c.contact_last_name,
        c.contact_email,
        p.phone_number,
        p.phone_type
    FROM contacts c
    LEFT JOIN phones p ON c.contact_id = p.contact_id
    WHERE
        c.contact_first_name ILIKE '%' || p_query || '%'
        OR c.contact_last_name ILIKE '%' || p_query || '%'
        OR c.contact_email ILIKE '%' || p_query || '%'
        OR p.phone_number ILIKE '%' || p_query || '%';

END;
$$;