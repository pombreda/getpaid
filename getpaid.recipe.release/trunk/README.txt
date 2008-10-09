- Code repository: https://getpaid.googlecode.com/svn/
- Questions and comments to getpaid-dev AT googlegroups dot com
- Report bugs at http://code.google.com/p/getpaid/issues/list


How to use the recipe
---------------------

- we are assuming you have your own buildout created
- this is the list of code to add to your buildout

[buildout]
parts =
   getpaid
   
unzip = true

[getpaid]
recipe = getpaid.recipe.release
find-links=
    http://getpaid.googlecode.com/files/hurry.workflow-0.9.1-getpaid.tar.gz
    http://getpaid.googlecode.com/files/yoma.batching-0.2.1-getpaid.tar.gz

[instance]
eggs =
    ${getpaid:eggs}

- then you will have to run bin/buildout, start your instance and quickinstall PloneGetPaid
