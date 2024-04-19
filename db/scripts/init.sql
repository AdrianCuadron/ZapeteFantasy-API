CREATE TABLE users (
    username VARCHAR(255) PRIMARY KEY,
    hashed_password VARCHAR(255),
    name VARCHAR(255),
    last_name VARCHAR(255),
    points INTEGER,
    money DOUBLE PRECISION,
    profile_image TEXT NOT NULL DEFAULT '/app/images/placeholder.png'
);

CREATE TABLE player (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    user_id VARCHAR(255),
    team VARCHAR(255),
    position VARCHAR(255),
    line_up BOOLEAN,
    points INTEGER,
    price DOUBLE PRECISION,
    state VARCHAR(255)
);

CREATE TABLE post (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(255),
    user_id VARCHAR(255),
    texto TEXT
);

INSERT INTO users (username, hashed_password, name, last_name, points, money)
VALUES 
    ('admin', '$2b$12$3VwSck4F9.VRwvn.6rWF0OXFGOBqASf3I3OpwnuuH.IyyBWn5sW4S', 'Admin', 'Admin', 0, 200.0),
    ('test', '$2b$12$3VwSck4F9.VRwvn.6rWF0OXFGOBqASf3I3OpwnuuH.IyyBWn5sW4S', 'Test', 'Test', 0, 200.0),
    ('aketza16', '$2b$12$3VwSck4F9.VRwvn.6rWF0OXFGOBqASf3I3OpwnuuH.IyyBWn5sW4S', 'Aketza', 'Calle', 0, 200.0),
    ('alexdi', '$2b$12$3VwSck4F9.VRwvn.6rWF0OXFGOBqASf3I3OpwnuuH.IyyBWn5sW4S', 'Alex', 'Diez', 0, 200.0),
    ('ikersobron', '$2b$12$3VwSck4F9.VRwvn.6rWF0OXFGOBqASf3I3OpwnuuH.IyyBWn5sW4S', 'Iker', 'Sobron', 0, 200.0),
    ('cuadron11', '$2b$12$3VwSck4F9.VRwvn.6rWF0OXFGOBqASf3I3OpwnuuH.IyyBWn5sW4S', 'Adrian', 'Cuadron', 0, 200.0);

INSERT INTO player (name, user_id, team, position, line_up, points, price, state) VALUES

('Joselu', NULL, 'Alaves', 'DL', false, 50, 10.0, 'Disponible'),
('Rodrigo Ely', NULL, 'Alaves', 'MC', false, 40, 8.5, 'Lesionado'),
('Ximo Navarro', NULL, 'Alaves', 'DF', false, 60, 12.0, 'Duda'),
('Luis Rioja', NULL, 'Alaves', 'PT', false, 30, 7.0, 'Roja'),
('Borja Sainz', NULL, 'Alaves', 'DF', false, 45, 9.5, 'Disponible'),

('Ager Aketxe', NULL, 'Almeria', 'DL', false, 45, 9.5, 'Lesionado'),
('Fran Villalba', NULL, 'Almeria', 'MC', false, 55, 11.0, 'Duda'),
('Ivan Balliu', NULL, 'Almeria', 'DF', false, 42, 8.8, 'Roja'),
('Largie Ramazani', NULL, 'Almeria', 'PT', false, 48, 10.2, 'Disponible'),
('Juan Villar', NULL, 'Almeria', 'DL', false, 38, 8.0, 'Disponible'),

('Adrián Cuadrón', NULL, 'Athletic Club', 'MC', false, 60, 12.0, 'Disponible'),
('Iñigo Martínez', NULL, 'Athletic Club', 'DL', false, 60, 12.0, 'Lesionado'),
('Unai Vencedor', NULL, 'Athletic Club', 'MC', false, 30, 7.0, 'Duda'),
('Yuri Berchiche', NULL, 'Athletic Club', 'DF', false, 45, 9.5, 'Roja'),
('Raúl García', NULL, 'Athletic Club', 'PT', false, 55, 11.0, 'Disponible'),
('Iker Muniain', NULL, 'Athletic Club', 'DL', false, 60, 12.0, 'Disponible'),

('João Félix', NULL, 'Atletico de Madrid', 'DL', false, 38, 8.0, 'Disponible'),
('Koke', NULL, 'Atletico de Madrid', 'MC', false, 47, 9.7, 'Disponible'),
('Stefan Savic', NULL, 'Atletico de Madrid', 'DF', false, 50, 10.0, 'Lesionado'),
('Luis Suárez', NULL, 'Atletico de Madrid', 'PT', false, 40, 8.5, 'Duda'),
('Marcos Llorente', NULL, 'Atletico de Madrid', 'DL', false, 45, 9.5, 'Roja'),

('Lionel Messi', NULL, 'FC Barcelona', 'DL', false, 45, 9.5, 'Disponible'),
('Frenkie de Jong', NULL, 'FC Barcelona', 'MC', false, 55, 11.0, 'Disponible'),
('Gerard Piqué', NULL, 'FC Barcelona', 'DF', false, 42, 8.8, 'Lesionado'),
('Antoine Griezmann', NULL, 'FC Barcelona', 'PT', false, 48, 10.2, 'Duda'),
('Pedri', NULL, 'FC Barcelona', 'DL', false, 60, 12.0, 'Roja'),

('Nabil Fekir', NULL, 'Real Betis', 'DL', false, 50, 10.0, 'Duda'),
('Guido Rodríguez', NULL, 'Real Betis', 'MC', false, 40, 8.5, 'Disponible'),
('Mandi', NULL, 'Real Betis', 'DF', false, 60, 12.0, 'Lesionado'),
('Joaquín', NULL, 'Real Betis', 'PT', false, 30, 7.0, 'Roja'),
('Emerson Royal', NULL, 'Real Betis', 'DF', false, 45, 9.5, 'Disponible'),

('Álvaro Negredo', NULL, 'Cadiz', 'DL', false, 45, 9.5, 'Disponible'),
('Jon Ander Garrido', NULL, 'Cadiz', 'MC', false, 55, 11.0, 'Disponible'),
('Isaac Carcelén', NULL, 'Cadiz', 'DF', false, 42, 8.8, 'Duda'),
('Salvi Sánchez', NULL, 'Cadiz', 'PT', false, 48, 10.2, 'Lesionado'),
('Anthony Lozano', NULL, 'Cadiz', 'DL', false, 38, 8.0, 'Roja'),

('Iago Aspas', NULL, 'Celta de Vigo', 'DL', false, 60, 12.0, 'Disponible'),
('Nolito', NULL, 'Celta de Vigo', 'MC', false, 30, 7.0, 'Duda'),
('Joseph Aidoo', NULL, 'Celta de Vigo', 'DF', false, 45, 9.5, 'Lesionado'),
('Denis Suárez', NULL, 'Celta de Vigo', 'PT', false, 55, 11.0, 'Roja'),
('Santi Mina', NULL, 'Celta de Vigo', 'DL', false, 60, 12.0, 'Disponible'),

('Ángel Rodríguez', NULL, 'Getafe', 'DL', false, 45, 9.5, 'Roja'),
('Mauro Arambarri', NULL, 'Getafe', 'MC', false, 55, 11.0, 'Disponible'),
('Djené Dakonam', NULL, 'Getafe', 'DF', false, 42, 8.8, 'Lesionado'),
('Enes Ünal', NULL, 'Getafe', 'PT', false, 48, 10.2, 'Duda'),
('Carles Aleñá', NULL, 'Getafe', 'DL', false, 60, 12.0, 'Disponible'),

('Stuani', NULL, 'Girona', 'DL', false, 38, 8.0, 'Disponible'),
('Samuel Sáiz', NULL, 'Girona', 'MC', false, 47, 9.7, 'Roja'),
('Bernardo Espinosa', NULL, 'Girona', 'DF', false, 50, 10.0, 'Lesionado'),
('Jordi Calavera', NULL, 'Girona', 'PT', false, 40, 8.5, 'Duda'),
('Franquesa', NULL, 'Girona', 'DL', false, 45, 9.5, 'Disponible'),

('Roberto Soldado', NULL, 'Granada', 'DL', false, 45, 9.5, 'Duda'),
('Yangel Herrera', NULL, 'Granada', 'MC', false, 55, 11.0, 'Disponible'),
('Domingos Duarte', NULL, 'Granada', 'DF', false, 42, 8.8, 'Lesionado'),
('Luis Milla', NULL, 'Granada', 'PT', false, 48, 10.2, 'Roja'),
('Ángel Montoro', NULL, 'Granada', 'DL', false, 60, 12.0, 'Disponible'),

('Sergio Araujo', NULL, 'Las Palmas', 'DL', false, 60, 12.0, 'Disponible'),
('Maikel Mesa', NULL, 'Las Palmas', 'MC', false, 30, 7.0, 'Duda'),
('Álvaro Lemos', NULL, 'Las Palmas', 'DF', false, 45, 9.5, 'Lesionado'),
('Rober', NULL, 'Las Palmas', 'PT', false, 55, 11.0, 'Roja'),
('Jesús Fortes', NULL, 'Las Palmas', 'DL', false, 45, 9.5, 'Disponible'),

('Abdon Prats', NULL, 'Mallorca', 'DL', false, 45, 9.5, 'Duda'),
('Luis García', NULL, 'Mallorca', 'MC', false, 55, 11.0, 'Disponible'),
('Fran Gámez', NULL, 'Mallorca', 'DF', false, 42, 8.8, 'Lesionado'),
('Amath Ndiaye', NULL, 'Mallorca', 'PT', false, 48, 10.2, 'Roja'),
('Jordi Mboula', NULL, 'Mallorca', 'DL', false, 60, 12.0, 'Disponible'),

('Rubén García', NULL, 'Osasuna', 'DL', false, 45, 9.5, 'Roja'),
('Oier Sanjurjo', NULL, 'Osasuna', 'MC', false, 55, 11.0, 'Disponible'),
('Unai García', NULL, 'Osasuna', 'DF', false, 42, 8.8, 'Lesionado'),
('Ante Budimir', NULL, 'Osasuna', 'PT', false, 48, 10.2, 'Duda'),
('Javi Martínez', NULL, 'Osasuna', 'DL', false, 60, 12.0, 'Disponible'),

('Alexander Isak', NULL, 'Real Sociedad', 'DL', false, 45, 9.5, 'Duda'),
('Mikel Merino', NULL, 'Real Sociedad', 'MC', false, 55, 11.0, 'Disponible'),
('Diego Llorente', NULL, 'Real Sociedad', 'DF', false, 42, 8.8, 'Lesionado'),
('Adnan Januzaj', NULL, 'Real Sociedad', 'PT', false, 48, 10.2, 'Roja'),
('Portu', NULL, 'Real Sociedad', 'DL', false, 60, 12.0, 'Disponible'),

('Óscar Trejo', NULL, 'Rayo Vallecano', 'DL', false, 45, 9.5, 'Duda'),
('Santi Comesaña', NULL, 'Rayo Vallecano', 'MC', false, 55, 11.0, 'Disponible'),
('Saveljich', NULL, 'Rayo Vallecano', 'DF', false, 42, 8.8, 'Lesionado'),
('Álvaro García', NULL, 'Rayo Vallecano', 'PT', false, 48, 10.2, 'Roja'),
('Bebe', NULL, 'Rayo Vallecano', 'DL', false, 60, 12.0, 'Disponible'),

('Karim Benzema', NULL, 'Real Madrid', 'DL', false, 50, 10.0, 'Disponible'),
('Luka Modric', NULL, 'Real Madrid', 'MC', false, 40, 8.5, 'Duda'),
('Sergio Ramos', NULL, 'Real Madrid', 'DF', false, 60, 12.0, 'Lesionado'),
('Thibaut Courtois', NULL, 'Real Madrid', 'PT', false, 30, 7.0, 'Roja'),
('Lucas Vázquez', NULL, 'Real Madrid', 'DL', false, 45, 9.5, 'Disponible'),

('Youssef En-Nesyri', NULL, 'Sevilla', 'DL', false, 45, 9.5, 'Duda'),
('Joan Jordán', NULL, 'Sevilla', 'MC', false, 55, 11.0, 'Disponible'),
('Diego Carlos', NULL, 'Sevilla', 'DF', false, 42, 8.8, 'Lesionado'),
('Luuk de Jong', NULL, 'Sevilla', 'PT', false, 48, 10.2, 'Roja'),
('Jesús Navas', NULL, 'Sevilla', 'DL', false, 60, 12.0, 'Disponible'),

('Maxi Gómez', NULL, 'Valencia', 'DL', false, 45, 9.5, 'Duda'),
('Carlos Soler', NULL, 'Valencia', 'MC', false, 55, 11.0, 'Disponible'),
('José Gayà', NULL, 'Valencia', 'DF', false, 42, 8.8, 'Lesionado'),
('Gonçalo Guedes', NULL, 'Valencia', 'PT', false, 48, 10.2, 'Roja'),
('Manu Vallejo', NULL, 'Valencia', 'DL', false, 60, 12.0, 'Disponible'),

('Gerard Moreno', NULL, 'Villarreal', 'DL', false, 45, 9.5, 'Duda'),
('Dani Parejo', NULL, 'Villarreal', 'MC', false, 55, 11.0, 'Disponible'),
('Pau Torres', NULL, 'Villarreal', 'DF', false, 42, 8.8, 'Lesionado'),
('Paco Alcácer', NULL, 'Villarreal', 'PT', false, 48, 10.2, 'Disponible'),
('Yeremy Pino', NULL, 'Villarreal', 'DL', false, 60, 12.0, 'Disponible');

INSERT INTO post (tipo, user_id, texto) VALUES

('compra', 'admin','ha comprado a Joselu Mato'),
('venta', 'admin','ha vendido a Maxi Gómez'),
('publicacion', 'admin', 'hola que tal');