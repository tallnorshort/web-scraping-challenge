from flask import Flask, render_template, redirect

from flask_pymongo import PyMongo

import scrape_mars



app = Flask(__name__)



# MongoDB connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"

mongo = PyMongo(app)



@app.route("/")

def index():



    mars_info_dict = mongo.db.mars_facts.find_one()



    # Return template and data

    return render_template("index.html", mars=mars_info_dict)



@app.route("/scrape")

def scrape():

    mars_info_dict = scrape_mars.scrape()



    mongo.db.mars_info_dict.update({}, mars_info_dict, upsert=True)



    return redirect("/", code=302)



if __name__ == "__main__":

    app.run(debug=True)
