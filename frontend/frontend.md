**FRONTEND**

Frontend is being created using Django templates, HTML, CSS, JavaScript(React.js). 

Folder frontend structure:  
frontend  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── src  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── components  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── static  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;package.json  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;webpack.config.json  

Inside components folder, there are React.js components. To add one to the project, you should create new file and then define new build script in _package.json_. After that you are able to run this script inside frontend(not root directory) and import file created by webpack in .html template file.  

If there are problems, try ```npm install```. If there are not any changes whole project should run as it is after just ```docker-compose up``` inside root directory.
