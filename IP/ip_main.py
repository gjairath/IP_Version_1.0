# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 21:58:35 2021

@author: garvit
"""

import sys
import gui as gui
from project import Project


# Existing projects -> Big Tasks [Quaterly Review] -> Tasks [Do something] -> People

if __name__ == "__main__":
    print ("Hi!\n")
    
    new_project = Project()    
    print ("-" * 20)
    print(new_project.name)
    print ("-" * 20)
    print(new_project.is_active, "[Is Active?]")    
    print ("-" * 20)
    
    print ("\n\nSub-Tasks:")
    
    print(new_project.sub_tasks[0].name)
    print ("-" * 20)
    print(new_project.sub_tasks[0].eta, "Minutes (Time Left)")
    print ("-" * 20)
    print(new_project.sub_tasks[0].finish_date)
    print ("-" * 20)
    print(new_project.sub_tasks[0].members)

    
    app = gui.QApplication(sys.argv)
    ex = gui.App()
    sys.exit(app.exec_())
    