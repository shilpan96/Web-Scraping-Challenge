# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# create home route and define home function
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_info = mongo.db.mars_collection.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_info)

# create scrape route 
@app.route("/scrape")
def scrape():
    # run the scrape function
    mars_data = scrape_mars.scrape()

    # insert the mars data in to the collection
    mongo.db.mars_collection.update({}, mars_data, upsert=True)

    # go back to the home page
    return redirect("/")

# run the app
if __name__ == "__main__":
    app.run(debug=False)