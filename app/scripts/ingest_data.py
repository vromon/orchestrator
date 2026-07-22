import time
from app.ai.vectorstore import get_vectorstore
from app.ai.loader import get_csv_loader

loader = get_csv_loader("./app/data/raw/Indian_Tour_dataset.csv", ["state"])
docs = loader.load()

total_docs = len(docs)
batch_size = 20

try:
    vectorstore = get_vectorstore()
    
    for i in range(0, total_docs, batch_size):
        batch = docs[i : i + batch_size]
        
        uploaded = False
        while not uploaded:
            try:
                print(f"Uploading documents {i} to {i + len(batch)}...")
                vectorstore.add_documents(documents=batch)
                uploaded = True  # Success! Break the while loop
                
            
                time.sleep(2.5) 
                
            except Exception as e:
            
                if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                    print("Quota hit! Sleeping for 22 seconds to let the API cool down...")
                    time.sleep(22) 
                    print("Retrying the batch now...")
                else:
                    raise e

except Exception as e:
    print(f"An error occurred: {e}")
else:
    print("Data ingestion successful!")
