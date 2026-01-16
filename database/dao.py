from database.DB_connect import DBConnect
from model.prodotto import Prodotto

class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def get_category():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT id,category_name
                    FROM category 
                    ORDER BY category_name asc """
        cursor.execute(query)

        for row in cursor:
            results.append((row["id"],row["category_name"]))


        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_prodotti_per_categoria(id_categoria):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                    FROM product 
                    WHERE category_id=%s
                    ORDER BY product_name"""

        cursor.execute(query, (id_categoria,))

        for row in cursor:
            results.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_connessioni(data_inizio,data_fine):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT oi.product_id as id, count(*) as peso
                    FROM `order` o, order_item oi
                    WHERE oi.order_id=o.id and DATE(order_date) between %s and %s
                    GROUP BY oi.product_id 
                    HAVING count(*)>=1"""

        cursor.execute(query, (data_inizio,data_fine,))

        for row in cursor:
            results.append((int(row["id"]),row["peso"]))

        cursor.close()
        conn.close()
        return results






