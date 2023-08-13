CREATE TABLE IF NOT EXISTS sigma_gawsalya_schema.dim_truck (
    truck_id BIGINT GENERATED ALWAYS AS IDENTITY,
    t_name TEXT,
    t_desc TEXT,
    card_reader TEXT,
    fsa_rating SMALLINT,
    PRIMARY KEY (truck_id)
);


CREATE TABLE IF NOT EXISTS sigma_gawsalya_schema.dim_type (
    type_id BIGINT GENERATED ALWAYS AS IDENTITY,
    payment_type TEXT,
    PRIMARY KEY (type_id)
);


CREATE TABLE IF NOT EXISTS sigma_gawsalya_schema.dim_date (
    date_id BIGINT GENERATED ALWAYS AS IDENTITY,
    d_date DATE,
    d_day TEXT,
    PRIMARY KEY (date_id)
);


CREATE TABLE IF NOT EXISTS sigma_gawsalya_schema.fact_truck_transaction (
    truck_id BIGINT,
    type_id BIGINT,
    date_id BIGINT,
    cost FLOAT,
    f_time TIMESTAMP,
    FOREIGN KEY (truck_id) REFERENCES sigma_gawsalya_schema.dim_truck(truck_id),
    FOREIGN KEY (type_id) REFERENCES sigma_gawsalya_schema.dim_type(type_id),
    FOREIGN KEY (date_id) REFERENCES sigma_gawsalya_schema.dim_date(date_id)
);


INSERT INTO sigma_gawsalya_schema.dim_type (payment_type) VALUES ('card'),
                                            ('cash');
                                            


INSERT INTO sigma_gawsalya_schema.dim_truck(t_name, t_desc, card_reader, fsa_rating)
VALUES ('Burrito Madness','An authentic taste of Mexico.','YES', 4),
        ('Kings of Kebabs','Locally-sourced meat cooked over a charcoal grill.','YES', 2),
        ('Cupcakes by Michelle', 'Handcrafted cupcakes made with high-quality, organic ingredients.', 'YES', 5),
        ('Hartmanns Jellied Eels', 'A taste of history with this classic English dish.', 'YES', 4),
        ('Yoghurt Heaven', 'All the great tastes, but only some of the calories!', 'YES', 4),
        ('SuperSmoothie', 'Pick any fruit or vegetable, and we will make you a delicious, healthy, multi-vitamin shake. Live well, live wild.', 'NO', 3);