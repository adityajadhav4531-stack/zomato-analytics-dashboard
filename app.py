from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

@app.route("/")
def home():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ROOT",
        database="zomato"
    )

    cursor = conn.cursor()

    # KPI
    cursor.execute("""
        SELECT
            SUM(Revenue),
            SUM(Total_Orders),
            COUNT(DISTINCT Restaurant_ID),
            AVG(Rating)
        FROM zomato_cleaned_data13
    """)

    result = cursor.fetchone()

    # TOP 10 RESTAURANTS
    cursor.execute("""
        SELECT
            Restaurant_Name,
            Revenue
        FROM zomato_cleaned_data13
        ORDER BY Revenue DESC
        LIMIT 10
    """)

    top_restaurants = cursor.fetchall()

    # CITY-WISE REVENUE
    cursor.execute("""
        SELECT
            City,
            SUM(Revenue)
        FROM zomato_cleaned_data13
        GROUP BY City
        ORDER BY SUM(Revenue) DESC
    """)

    city_revenue = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "index.html",
        total_revenue=result[0],
        total_orders=result[1],
        total_restaurants=result[2],
        avg_rating=result[3],
        top_restaurants=top_restaurants,
        city_revenue=city_revenue
    )

if __name__ == "__main__":
    app.run(debug=True)