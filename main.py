'''
Main file to start the web server
'''

from web_app import create_app
# flask app creation
# hello
# hi
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
