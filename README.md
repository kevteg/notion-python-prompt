# Notion Python prompt! 


This is just a proof of concept. The idea is to render python code inside of a notion page using the new notion API. Just for fun!

<img width="800" alt="Quick demo" src="https://user-images.githubusercontent.com/5288503/160199145-b3ae51cf-f1a5-4601-8773-bb707012a8a7.gif">


## Seting up the notion page

- Create a new [notion integration](https://developers.notion.com/docs/getting-started#step-1-create-an-integration)
- Create a copy of [this page](https://keeeevin.notion.site/Python-Prompt-ed5eb08d626442f4ac7c9ae6d60d30ff) in your workspace
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
docker run -it -v $(pwd):/usr/src/app notion python pynotion.py -t INTEGRATION_TOKEN -p PAGE_ID
```

**Note**: Every time you add something to the page you need to run the command to update it with the result. Unfortunately it is not real time :(

## Available commands

### Run code: (Default)

The last text found on your page is processed as Python code and the result is appended to the page

```
... pynotion -t INTEGRATION_TOKEN -p PAGE_ID -c run
```

### Clean page: 

The page is cleaned

```
... pynotion -t INTEGRATION_TOKEN -p PAGE_ID -c clean
```

## Warning

- This is making use of the [eval](https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html) function so be careful with whom you share your notion page! They could do something like this (or worst):
![image](https://user-images.githubusercontent.com/5288503/160207635-00ae8260-2172-4b7b-8295-9857dcdb181c.png)
- This "propmpt" can't run any _complex code_ such as classes or method definitions 
