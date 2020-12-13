Student: Corey Vorsanger
Class: Comp 3006
Assignment: Large Project

This project is a scatch the surface analysis of Aviation in the United States and impacts of COOVID-19

Included:
    Aviation_Analysis.py : The main program. Can be called from the command line.Depending on the inputs will look
        at general trends or covid analysis.
        syntax Aviation_Analysis.py [-h] [-a <airport> | -s <state> | -r <region>] [-o <outfile>] <anaylsis>
        type Aviation_Analysis.py -h for more information

    Covid.py: module that helps the Covid analysis in Aviation_Analysis.py

    Test scripts for both Aviation_Analysis and Covid modules

    Falon_Field.ipynb: Jupyter notebook that investigates wher I work; Falcon Field Airport. Intended to 
        illustrate functionality of above modules

    3 csv files: Airport_Info, Covid_Data, Yearly_Data: Public data from FAA used in the program

    Project_env.yml: Yaml file contain used packages. Packages of note needed(excluding Python and what comes with it):
        matplotlib
        pandas
        numpy
        folium(Only needed if you plan on running the Jupyter notebook)