class SharePointRecords:

    def __init__(self):
        self.records = []
        self.documents = {}

    # CREATE
    def create(self, record):
        record["ID"] = len(self.records) + 1
        self.records.append(record)
        return record

    # READ
    def get(self, record_id):
        for record in self.records:
            if record["ID"] == record_id:
                return record
        return None

    # UPDATE
    def update(self, record_id, data):
        record = self.get(record_id)

        if record is None:
            return None

        record.update(data)
        return record

    # DELETE
    def delete(self, record_id):
        record = self.get(record_id)

        if record is None:
            return False

        self.records.remove(record)
        return True

    # DOCUMENT UPLOAD
    def upload_document(self, name, content):
        self.documents[name] = content

    # DOCUMENT RETRIEVAL
    def get_document(self, name):
        return self.documents.get(name)


# Example
app = SharePointRecords()

employee = app.create({
    "Name": "Pooja",
    "Department": "IT",
    "Training": "Python"
})

print("Created:", employee)
print("Read:", app.get(1))

app.update(1, {"Training": "SharePoint"})
print("Updated:", app.get(1))

app.upload_document("certificate.pdf", "Python Certificate")
print("Document:", app.get_document("certificate.pdf"))

app.delete(1)
print("After Delete:", app.get(1))
