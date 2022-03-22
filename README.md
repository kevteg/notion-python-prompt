# notion-python-interpreter
This is an experiment to render python code inside of a notion page using the new notion API. Just for fun!

## Seting up the notion page

- Create a new notion integration
- Create a copy of this page in your workspace
- Make sure to share your new page with your integration 
- Copy the page ID

## Running using docker

 - Create the image and tag it
docker build . -t notion 

- Run the command, make sure you have the integration token and the page ID 

docker run -it -v $(pwd):/usr/src/app notion python  pynotion.py -t INTEGRATION_TOKEN -p PAGE_ID
