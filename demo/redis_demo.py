import db


def connect():
    pool = db.ConnectionPool(host='127.0.0.1', port=6379)
    r = db.Redis(connection_pool=pool)
    # r = db.Redis(host='127.0.0.1', port=6379, db=0)
    r.set("foo", "bar")
    print(r.get("foo"))

    # pool = db.ConnectionPool(host='192.168.0.110', port=6379)
    # r = db.Redis(connection_pool=pool)

if __name__ == '__main__':
    connect()
