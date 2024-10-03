# Hosting on Google Cloud

Most of the legwork for understanding google cloud is complete.

To submit a docker image now, we must run the following command:
``` gcloud builds submit --region=europe-west1 --tag europe-west1-docker.pkg.dev/borders-buses-scrape-437521/buses-docker-repo/borders-test-basic:1.0.4 ```

Alter the final portion of the path to represent the local docker image name. 

The major issue that I am facing right now is that the requests to borders-buses are being flagged by antibot systems are returning "Just a moment..." html responses.

As of right now, I am looking for a way around this, otherwise GCP may not be the solution
