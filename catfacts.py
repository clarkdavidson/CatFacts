from flask import Flask,jsonify,request
import requests
import boto3
from botocore.exceptions import ClientError

client = boto3.client(
   service_name='ses',
   region_name='us-east-1',
   aws_access_key_id='AKIA5ORGZAXP3NXJPJSR',
   aws_secret_access_key="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"
)

app = Flask(__name__)


@app.route("/send", methods=["POST"])
def get_fact():
   if request.json.get("address") == None:
      return jsonify(error = "Missing email field"),400
   if '@' in request.json.get("address"):
      email = request.json.get("address")
   else:
      return jsonify(error="Please enter valid email"),400

   ## Get fact from Cat-Facts API ##
   x = requests.get('https://cat-fact.herokuapp.com/facts/random')
   response = x.json()
   fact = response["text"]

   ##Send fact to the client API ##
   try:

      email=client.send_email(
         Source='catfacts@csci390.com',
         Destination={
            'ToAddresses':[email]
         },
         Message={
            'Subject':{
               'Charset': 'UTF-8',
               'Data': 'Daily Cat Fact!'
            },
            'Body':{
               'Text':{
                  'Charset': 'UTF-8',
                  'Data': fact
               }
            }
         }
      )
   except ClientError as e:
      return jsonify(error=e.response['Error'])
   else:
      print("Email Sent Successfuly")
      return jsonify({}),200




if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)