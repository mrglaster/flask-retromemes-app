# Retromemes.net - small flask based website 

this site was created as a study assignment for Irkutsk State University (ISU). On assignment, we had to create a website with memes. It should support uploading new memes, viewing those already uploaded as a feed, authorizing and registering new users, and also allow users to rate posts with "like" or "dislike" 

```THIS VERSION IS WINDOWS ONLY```

## How to run this application?

1) Install ```Python 3.x```
2) Download the project
3) type in terminal/console  ```pip install -r requirements.txt``` 

or 

```
pip install Flask==1.1.4
pip install Werkzeug==1.0.1
pip install bcrypt
```
4) Change dir to the project's directory 
5) Run project with ```flask run```
6) Profit!


## Database structure 

![alt text](https://github.com/mrglaster/flask-retromemes-app/blob/windows-edition/readme_images/db_info.jpg)


## Pages of the site

### Authorizarion and Registration 

![alt text](https://github.com/mrglaster/flask-retromemes-app/blob/windows-edition/readme_images/login.png)



![alt text](https://github.com/mrglaster/flask-retromemes-app/blob/windows-edition/readme_images/register.png)


### Memes upload page

![alt text](https://github.com/mrglaster/flask-retromemes-app/blob/windows-edition/readme_images/upload_meme.png)

### Feed

![alt text](https://github.com/mrglaster/flask-retromemes-app/blob/windows-edition/readme_images/feed.png)

### And if there are too many memes

![alt text](https://github.com/mrglaster/flask-retromemes-app/blob/windows-edition/readme_images/too_many_memes.png)

### User's page

User's page is the page for account's owner. There the user can look at memes uploaded by his/her hands or do some activities, if the user is an administrator

![alt text](https://github.com/mrglaster/flask-retromemes-app/blob/windows-edition/readme_images/users_page.png)

### About roles

User roles can be divided into 3 groups. The first and most numerous are ordinary users. They can upload memes and delete uploaded by them ones. The second group is moderators, they can remove any memes from the site. And the third and last group, administrators. They have the same powers to delete posts as moderators, and they can also promote / demote other users, including moderators.

![alt text](https://github.com/mrglaster/flask-retromemes-app/blob/windows-edition/readme_images/default_user.png)

![alt text](https://github.com/mrglaster/flask-retromemes-app/blob/windows-edition/readme_images/just_moder.png)

![alt text](https://github.com/mrglaster/flask-retromemes-app/blob/windows-edition/readme_images/admin.png)


## Custom pages for errors (500, 404, etc)

### Error 500

![alt text](https://github.com/mrglaster/flask-retromemes-app/blob/windows-edition/static/images/error_images/500-image.png)

### Error 404 

![alt text](https://github.com/mrglaster/flask-retromemes-app/blob/windows-edition/static/images/error_images/404-image.png)

### Error 400 

![alt text](https://github.com/mrglaster/flask-retromemes-app/blob/windows-edition/static/images/error_images/400-image.png)

### Error 403

![alt image](https://github.com/mrglaster/flask-retromemes-app/blob/windows-edition/static/images/error_images/notadmin-image.png)

![alt image](https://github.com/mrglaster/flask-retromemes-app/blob/windows-edition/static/images/error_images/403-image.png)


### Developed by

1) [Vadim Nechaev](https://github.com/nech14)
2) [Vladislav Novikov](https://github.com/vladnov138)
3) [Egor Pristavka](https://github.com/mrglaster/)

### Links

1) https://flask.palletsprojects.com/en/2.2.x/
2) https://vk.com/whenangelsrise (https://vk.com/whenangelsrise?z=photo-162910245_456239052%2Fwall-162910245_34)
3) https://images7.memedroid.com/images/UPLOADED903/6056582719c9c.jpeg
