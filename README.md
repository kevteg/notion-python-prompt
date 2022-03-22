# Notion Python intepreter

This is just a proof of concept. The idea is to render python code inside of a notion page using the new notion API. Just for fun!

## Seting up the notion page

- Create a new [notion integration](https://developers.notion.com/docs/getting-started#step-1-create-an-integration)
- Create a copy of [this page](https://keeeevin.notion.site/Python-Interpreter-ed5eb08d626442f4ac7c9ae6d60d30ff) in your workspace
- Make sure to share your new page with your integration:
<img width="427" alt="Screen_Shot_2022-03-22_at_4_52_14_PM" src="https://user-images.githubusercontent.com/5288503/159582677-c1d4c2f5-2d07-44fe-92a1-34ef524f1d20.png">

- Copy the page ID: 
<img width="768" alt="Screen_Shot_2022-03-22_at_4_47_45_PM" src="https://user-images.githubusercontent.com/5288503/159581870-f62ffb8a-f6af-4e69-abcf-23c838b8c26f.png">


## Running using docker

 - Create the image and tag it:
```
docker build . -t notion 
```

- Run the command, make sure you have the integration token and the page ID 
```
docker run -it -v $(pwd):/usr/src/app notion python  pynotion.py -t INTEGRATION_TOKEN -p PAGE_ID
```

**Note**: Every time you add something to the page you need to run the command to update it with the result. Unfortunately it is not real time :(
