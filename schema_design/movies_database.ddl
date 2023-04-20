CREATE SCHEMA IF NOT EXISTS content;

/* Tables */

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
); 

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
); 

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    CONSTRAINT genre_id FOREIGN KEY(id) REFERENCES content.genre(id),
    CONSTRAINT film_work_id FOREIGN KEY(id) REFERENCES content.film_work(id),
    created timestamp with time zone,
); 

CREATE TABLE IF NOT EXISTS content.person(
    id uuid PRIMARY KEY,
    full_name text,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work(
    id uuid PRIMARY KEY,
    CONSTRAINT person_id FOREIGN KEY(id) REFERENCES content.person(id),
    CONSTRAINT film_work_id FOREIGN KEY(id) REFERENCES content.film_work(id),
    role text,
    created timestamp with time zone
);

/* Indexes */

CREATE UNIQUE INDEX film_work_genre ON content.genre_film_work (film_work_id, genre_id)

CREATE UNIQUE INDEX film_work_person_role ON content.person_film_work (film_work_id, person_id, role);
