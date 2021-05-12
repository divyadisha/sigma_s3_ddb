import boto3
ddb = boto3.client("dynamodb")
import pandas as pd
s3 = boto3.client("s3")

def read_file(event, context):
    try:
        data = s3.get_object(
            Bucket="awssigmabocket",
            Key="testdata.csv"
        )
        books_df = pd.read_csv(data.get("Body"))
        print(books_df)
        
        for i in range(len(books_df)):
            try:
                dy_db = ddb.put_item(
                    TableName="emptable",
                    Item={
                        'id': {
                            'N': str(books_df['id'][i])
                        },
                        'name': {
                            'S': books_df['name'][i]
                        }
                    }
                )
            except BaseException as e:
                print(e)
                raise(e)
            
    except BaseException as e:
        print(e)
        raise(e)
    
    return {"message": "Successfully read file from S3 and inserted to DDB"}
