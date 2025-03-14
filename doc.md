# JS files documentation :

[appUtils.js](/app/static/appUtils.md)  -  Contain the utility class to provide various functionalities, including dynamic CSS rules management, event handling, and caching via localStorage. Implements the Singleton design pattern.  
[confetti.js](/app/static/confetti.md) - Contain a class that manages confetti animations on the page.  
[script.js](/app/static/script.md) -  Main script, manage game, interactions, ...   

# How to update this documentation  :

Install Node.JS on your computer and paste the following commands into the shell:

- npm install -g jsdoc-to-markdown
- cd app/static
- jsdoc2md appUtils.js > appUtils.md
- jsdoc2md confetti.js > confetti.md
- jsdoc2md script.js > script.md