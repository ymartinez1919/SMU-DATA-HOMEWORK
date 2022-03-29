from flask import Flask, render_template, redirect
from mongoHelper import MongoHelper
from scrape_mars import ScrapingHelper

# Create an instance of Flask
app = Flask(__name__)

# init helper classes
mongo = MongoHelper()
scraper = ScrapingHelper()

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    marshmk_data = list(mongo.db.mars.find())[0]

    # Return template and data
    return render_template("index.html", mars=marshmk_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to a variable
    # DO SCRAPING WORK
    data = scraper.getData()


    # Update the Mongo database using update and upsert=True
    mongo.insertData(data)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
