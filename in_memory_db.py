class InMemoryDB:
    def __init__(self):
        self.data = {}                  
        self.transaction_active = False 
        self.trans_data = {}            

    def get(self, key): #return the value associated with the key or null if the key doesn’t exist. 
        return self.data.get(key, None)

    def put(self, key, value):
        # called when a transaction is not in progress throw an exception
        if not self.transaction_active:
            raise Exception("No transaction in progress. Please start a transaction before putting data.")
        self.trans_data[key] = value

    def begin_transaction(self):
        if self.transaction_active:
            raise Exception("Transaction already in progress. Please commit or rollback the current transaction before starting a new one.")
        self.transaction_active = True
        self.trans_data = {}

    def commit(self):
        # Commits all changes made during the transaction to the main data
        if not self.transaction_active:
            raise Exception("No transaction to commit.")
        self.data.update(self.trans_data)
        self.trans_data = {}
        self.transaction_active = False

    def rollback(self):
        #  abort all the changes
        if not self.transaction_active:
            raise Exception("No transaction to rollback.")
        self.trans_data = {}
        self.transaction_active = False

if __name__ == "__main__":
    db = InMemoryDB()
    print(db.get("A"))  # None, as A doesn’t exist
    try:
        db.put("A", 5)
    except Exception as e:
        print(e)  # Error because no transaction is in progress
    db.begin_transaction()
    db.put("A", 5)
    print(db.get("A"))  # None, change not visible yet
    db.put("A", 6)
    db.commit()
    print(db.get("A"))  # 6, change now visible after commit
    try:
        db.commit()
    except Exception as e:
        print(e)  # Error, no transaction to commit
    try:
        db.rollback()
    except Exception as e:
        print(e)  # Error, no transaction to rollback
    print(db.get("B"))  # None, B does not exist
    db.begin_transaction()
    db.put("B", 10)
    db.rollback()
    print(db.get("B"))  # None, rollback does not show changes
