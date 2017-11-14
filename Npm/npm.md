# npm

### Basics 

npm install 

Installs packages specified in package.json at root.

npm link 

		/local/node_module_A/ npm link
		/local/node_module_B/ npm link node_module_A

Now node_module_B will reference the local version of node_module_A instead of fetching from npm registry.

npm list node_module 

Displays installed node_module name and version

npm bump 

Auto-increments current node package version