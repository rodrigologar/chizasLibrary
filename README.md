# CHIZA'S LIBRARY
#### Video Demo:  https://youtu.be/jkvLZEJSsLM
#### Description:
Chiza's Library is a Python-Flask web application in which you can access
my personal selection of books. In this app you can select the books you are
reading, and you can update your progress until you finish them. This app has
different pages that I will describe below:

- login.html is pretty self-explanatory, since its only function is to let
the user login. It goes through chiza.db, which is the database used in
this web app, and it looks in the users table for the username that the user
typed in the username prompt. If it is found, it checks if the entered
password is correct and it logs you in. If your username doesn't exist, you
need to register.

- register.html also explains itself. It let's the user create an account. It
prompts the user for an username and a password. After the user clicks on
register, the username and hashed password is saved on the database. After this
you are able to login.

- index.html shows you the books that you are currently reading and the books
you've finished. It also let's you update your progress on the books you're
reading and shows the percentage of the book you've read. So basically, this
page checks the library table of the database, which has every book added by
every user to each one's library. By a for loop it goes through this table
in the database looking for all the books added by the active user and shows
them as a Bootstrap card, showing the cover of the book in the top, and a
progress bar in the bottom that shows you the percentage of the book you have
read. Under these, you can update your progress by entering the page you are in
and clicking on the update button. If you enter the last page's number, which
means you've finished the book, the book will go to the already read section
of the page, by changing its read value on the database from False to True.

- Everytime you finish a book, the app will take you to finished.html, which
simply congratulates you and tells you how many books from the collection
you've finished reading.

- When you finish all the books from the collection, the app will take you to
final.html, where you will be congratulated on finishing the entire selection
of books.

- Finally, collection.html shows the entire selection of books you can read in
the app. This page shows you the books' covers and information like author,
pages, language, etc. In this page you can add any book you like to your
library. This page also uses a for loop going through the books table on the
database, which has all the books from the collection. collection.html also
displays the book, like index.html, in a Bootstrap card, which at the top shows
the book cover, and in the bottom it shows the books' name and author. Below these
it has a collapsed section where you have the books' number of pages, ISBN, the
year the book was originally published and the language this specific edition is
printed in.

- All of the pages in the app follow the layout.html desing. A the top of every
page is the title of the page "Chiza's Library" in different pastel colors. This
was inspired by CS50 Finance's title. Beside the title there is a navbar with the
Home page, which is index.html, and the Collection page, which is collection.html.
On the far right of the top of the page is the logout button. The footer of every
page has a small text that encourages the users to shop at local libraries to
support them. And finally, on the bottom of the page, you can see a message
that says that this page was dedicated to my girlfriend, who's nickname is Chiza,
for supporting me in every part of my life.