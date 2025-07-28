# How to Config a telethon bot in telegram

1- Update Ubuntu Distro
  a- <pre><code> sudo apt update -y && sudo apt upgrade -y </code></pre>
2- Installed Python and dependencies
  <pre><code> sudo apt install -y python3 python3.8-venv python3-pip </code></pre>
  
3- Create python environment
   <pre><code> python3 -m venv my-venv-name </code></pre> (if the activaton does not work with the next command on step 4 come back and re run same commnand from here again)

4- <pre><code>source my-env-name/bin/activate </code></pre> (You will see the name of your enviroment in the left of your name that is how your will know the environment is working)

5- Install telethon
  a- Move to the environment directory and run the next commadn to install telethon
    b- <pre><code>pip install telethon</code></pre>

6- After that everything should be working and run your telethon python file to test with the next command 
    a- python3 telethon.py or if it does not work try python instead python3


# Create a Service
Modify the next document with the path of your py files as it is shown in the telethon.service file
  

