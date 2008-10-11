Starting a project based on this project
========================================
   git clone git://github.com/dokterbob/django-project-base.git <my_app>
   git checkout -b <my_app>

Updating your project from the base
-----------------------------------
   git pull
   git merge master

Using this base project within another app
==========================================
   git clone <my_app_url> <my_app>

   git remote add -f django-project-base git://github.com/dokterbob/django-project-base.git
   
   git merge -s ours --no-commit django-project-base/master
   
   git read-tree --prefix=demo/ -u django-project-base/master
   
   git commit -m "Merge django-project-base project as demo"

(This is the 'subtree merge strategy, see: 
http://www.kernel.org/pub/software/scm/git/docs/howto/using-merge-subtree.html )

Updating your project from the base
-----------------------------------
   git pull -s subtree django-project-base master
