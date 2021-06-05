from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Scrape through functions
    mars_info = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Scrape through functions
    mars_info = mongo.db.mars_info

    # Run the scrape function
    mars_data = scrape_mars.scrape_mars_news()
    mars_f = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_images()
    mars_data = scrape_mars.scrape_mars_hemi()

    # Update the Mongo database using update and upsert=True
    mars_info.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
