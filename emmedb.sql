use emmedb;

INSERT INTO users (name, email, image, admin, username, password) values
    ('name1', 'email1@g.com', 'image1', 1, 'user1', '123'),
    ('name2', 'email2@g.com', 'image2', 0, 'user2', '123'),
    ('name3', 'email3@g.com', 'image3', 1, 'user3', '123'),
    ('name4', 'email4@g.com', 'image4', 0, 'user4', '123'),
    ('name5', 'email5@g.com', 'image5', 1, 'user5', '123'),
    ('name6', 'email6@g.com', 'image6', 0, 'user6', '123');

INSERT INTO projects (name_project, category, description, image, user_id) values
    ('pro1', 'cat1', 'desc1', 'image1', 1),
    ('pro2', 'cat2', 'desc2', 'image2', 2),
    ('pro3', 'cat3', 'desc3', 'image3', 3),
    ('pro4', 'cat4', 'desc4', 'image4', 4),
    ('pro5', 'cat5', 'desc5', 'image5', 5),
    ('pro6', 'cat6', 'desc6', 'image6', 6);




