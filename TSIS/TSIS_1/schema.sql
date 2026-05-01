CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

ALTER TABLE contacts
    ADD COLUMN birthday DATE,
    ADD COLUMN group_id INTEGER REFERENCES groups(id);

CREATE TABLE phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(contact_id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);

-- to update phone_number if there is another number in the same phone_type
ALTER TABLE phones
ADD CONSTRAINT unique_contact_phone_type
UNIQUE (contact_id, phone_type);


INSERT INTO groups(name) VALUES
('work'),
('family'),
('friend'),
('other');