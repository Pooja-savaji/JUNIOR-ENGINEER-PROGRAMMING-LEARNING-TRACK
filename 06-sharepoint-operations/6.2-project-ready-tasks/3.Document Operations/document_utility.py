
documents = [
def upload_document(name, folder, document_type, department):
    document = {
        "name": name,
        "folder": folder,
        "metadata": {
            "Document Type": document_type,
            "Department": department
        }
    }

    documents.append(document)
    print("Uploaded:", name)


def retrieve_document(name):
    for document in documents:
        if document["name"] == name:
            print("Retrieved:", document)
            return document

    print("Document not found")


# Upload documents
upload_document(
    "Python_Training.pdf",
    "Training Materials",
    "Training Material",
    "IT"
)

upload_document(
    "Pooja_SQL_Certificate.pdf",
    "Certificates",
    "Certificate",
    "IT"
)


# Retrieve document
retrieve_document("Python_Training.pdf")

# Check metadata
print("\nAll Documents:")
for document in documents:
    print(document)
