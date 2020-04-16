from api import create_app


# imports and start the app so that app is modular
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)