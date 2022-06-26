from unittest import result
from django.shortcuts import render , redirect
from django.contrib import messages
from login_register_app .models import User 
from .models import Book


#1
def index(request):
    # TO MAKE SURRE USER IS LOGGED
    if not ('userId' in request.session):
        messages.error(request, "Need to login first", 'alert alert-danger')
        return render(request,'loginError.html')

    # RETURNING THE LOGGED USER AND ALL BOOKS FROM DB
    
    userId = request.session['userId']
    curr_user = User.objects.filter(id=userId).last()
    context = {
        'curr_user': curr_user ,
        'books' : Book.objects.all(),
        'allBooks': allBooks(request),
    }
    try:
        if (request.session['userTryToPost']):
            #to not lost the user inputs, if user try to add a book and an error occured.
            context['book_title'] = request.session['book_title']
            context['book_desc'] = request.session['book_desc']
            request.session['userTryToPost'] = False
            #empty session, so if user try to refresh the page to empty the form.
            del request.session['book_title']
            del request.session['book_desc']
    except:
        print('--'*80,'no post saved')

    return render(request,'books.html',context)


#2
def allBooks(request):
    books = Book.objects.all()
    userId = request.session['userId']
    user = User.objects.get(id=userId)
    userBooks = user.liked_books.all()
    books = Book.objects.all()
    allBooks = []
    if (len(userBooks) == 0):
        for book in books:
            result = 1
            dict = {
                'book' : book,
                'result':result}
            allBooks.append(dict)
    else:      
        for book in books:
            for userBook in userBooks:
                if(userBook == book):
                    result = 0
                    dict = {
                        'book' : book,
                        'result':result}
                    allBooks.append(dict)
                    break
                elif userBook == userBooks.last():
                    result = 1
                    dict = {
                        'book' : book,
                        'result':result}
                    allBooks.append(dict)
    print('--'*50,allBooks)
    return allBooks

#3
# 'addBook'
def addBook (request):
    if request.method != 'POST':
        return redirect ('/books')
    
    # TO ENSURE THAT USER INSERT A VALID INPUTS.
    errors = Book.objects.validBook(request.POST)
    if(len(errors)>0):
        for key, value in errors.items():
            messages.error(request, value, 'alert alert-danger')
        # saving user inputs if error occured, so user don't have to write eveything again
        savingUserAttempt(request,request.POST)
        return redirect ('/books')

    # RETURNING THE USER FROM DB, to link the BOOK to USER who uploaded the BOOK.
    userId = request.session['userId']
    user = User.objects.filter(id=userId).last()

    # RETURN USER INPUTS
    title = request.POST['title']
    desc = request.POST['desc']

    # CREATING A NEW BOOK
    book = Book.objects.create(title=title,desc=desc,uploaded_by=user)

    # AUTOMATICALLY FAVORITE the new BOOK by THE USER who uploaded the BOOK.
    favorite(request,book.id)
    return redirect ('/books')


#4
def savingUserAttempt(request,post,bookId=None):
    #if USER try to UPDATE existing BOOK
    if bookId:
    # saving user inputs in session
        try:
            book = Book.objects.get(id=id)
            request.session['book_title'] = post['title'] if post['title'] else book.title
            request.session['book_desc'] = post['desc'] if post['desc'] else book.desc
            request.session['userTryToPost'] = True
        except:
            # no post.
            request.session['book_title'] = ''
            request.session['book_desc'] = ''
            request.session['userTryToPost'] = False
    else:
        # if its ADD NEW BOOK

        print('--'*50,'in add new book')
        request.session['book_title'] = post['title'] if post['title'] else ""
        request.session['book_desc'] = post['desc'] if post['desc'] else ""
        request.session['userTryToPost'] = True

#5
# favorite/<int:bookId>
def favorite(request,bookId):
    userId = request.session['userId']
    user = User.objects.filter(id=userId).last()
    book = Book.objects.get(id=bookId)
    book.liked_by.add(user)
    book.save()
    return redirect ('/books')

#6
# <int:bookId>
def showBook(request,bookId):
    # RETURNING CURRENT USER & the chosen BOOK from DB
    userId = request.session['userId']
    curr_user = User.objects.filter(id=userId).last()
    book = Book.objects.get(id=bookId)

    # CHECKING IF CURRENT USER didnt upload this book
    likedBook = False
    if book.uploaded_by.id != curr_user.id:
        # CHECKING IF CURRENT USER liked this book
        for user in book.liked_by.all():
            if user.id == curr_user.id:
                likedBook = True
                break
            
        print('--'*50,likedBook )    
        context = {
        'curr_user': curr_user,
        'book':book,
        'likedBook':likedBook,
        }
        return render (request,'otherBooks.html',context)

    # IF CURRENT USER uploaded this book
    context = {
        'curr_user': curr_user,
        'book':book,
        'book_title': book.title,
        'book_desc': book.desc,
    }
    try:
        # if user try to update a book and falied, then restore the inputs to try again without typing again.
        if (request.session['userTryToPost']):
            context['book_title'] = request.session['book_title']
            context['book_desc'] = request.session['book_desc']
            request.session['userTryToPost'] = False #if user try to refresh the page to reset the original book info.
    except:
        print('--'*80,'no post saved')

    return render (request,'userbooks.html',context)

#7
# handlingBook/<int:bookId>
def handlingBook(request,bookId):
    # to specify which route to take based on the clicked button.
    if request.method != 'POST':
        return redirect(f'/favorite/{bookId}')

    if(request.POST['action']=='delete'):
        return delete(request,bookId)
    else:
        return update(request,bookId)

#8
def delete(request,bookId):
    book = Book.objects.get(id=bookId)
    book.delete()
    return redirect('/books')

#9
def update(request,bookId):
    print('--'*50,'in update')
    # RETURN the BOOK
    book = Book.objects.get(id=bookId)

    # CHECKING if the INPUTS are VALID
    errors = Book.objects.validBook(request.POST)
    if(len(errors)>0):
        for key, value in errors.items():
            messages.error(request, value, 'alert alert-danger')
        # saving user inputs, if user try to update a book and falied,so he/she can restore the inputs to try again without typing again.
        savingUserAttempt(request,request.POST)
        return redirect (f'/books/{bookId}')

    # SAVE THE UPDATED INFO.
    book.title = request.POST['title']
    book.desc = request.POST['desc']
    book.save()

    # UPDATE SUCCESS.
    messages.success(request, f"SUCCESFULY UPDATE THE BOOK: {book.title}", 'alert alert-success')
    request.session['userTryToPost'] = False
    return redirect('/books')


#10
# un_favorite/<int:bookId>
def un_favorite(request,bookId):
    userId = request.session['userId']
    curr_user = User.objects.get(id=userId)
    book = Book.objects.get(id=bookId)
    book.liked_by.remove(curr_user)
    return redirect(f'/books/{bookId}')