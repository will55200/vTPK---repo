# Vector Tile Package Automation
This code will automate the creation of vector tile packages from an esri aprx for custom extents (AOIs) at user defined scales. This is accomplished using the CIM Module. Parameters are built into both scripts that step the user through the different inputs needed. There are not parameters set up for summary or tags. You can hard code this in at around lines 119,120. Do not use any " " or , when putting in the file paths or cache scales. The two scripts are very similar, the main difference is that one uses vector tile indexs and the other does not.

The code tracks your progress, creates a text log of processing times for each AOI, has some error managment, and will continue to process if some AOIs are unsuccessful. At the end if you have any unsuccessful runs they will be listed and you can go back in the terminal to find its error.

In testing I processed 148 AOIs I created of USFS National Forest boundaries at a scale of 295828763 to 564. Using the indexed script it took ~22 hours to process. Using the no index script it took ~54 hours. The resulting vtpks were the same. Although the index script is faster it does require more file and data management. It assumes that you already have indexs generated. Overall I think the time it took me to process the indexs, QA them against my AOIs, and set them up may add up to the time it takes to use the no index script. BUT the time saver here is that I will not need to redo the indexs unless something major changes with my map like a number of layers are added or removed.  

This code was build using Python 3.11.8 and Esri ArcGIS Pro 3.3.

## Indexed Script
To run this script you need to make sure that the name of your AOI and your AOIs index are EXACTLY the same. 

## No Index Script
This script does not requre the user to have vector tile indexs for their AOI(s). A index will be generated on the fly for each AOI. This does add processing time but reduces the ammount of data that you need to manage. 

# Known Issues
Your vtpk output may have labels that extend outside of your AOI. This is because of the way the vtpk geoprocessing tool splits the tiles and the style of the data. As you zoom into your vtpk you will see that only the data inside your AOI will show. I have spoken to esri about this and they have put in a enhancement request (ENH - 000169523)
![image](https://github.com/user-attachments/assets/970e1d4b-fd61-415a-a65f-5110a6224791)
# Resources 
Python CIM access - esri documentation - https://pro.arcgis.com/en/pro-app/3.1/arcpy/mapping/python-cim-access.htm
ArcGIS Pro 3.3 API Reference CIMMap Class - https://pro.arcgis.com/en/pro-app/latest/sdk/api-reference/topic2824.html
Create Vector Tile Package - esri documentation - https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/create-vector-tile-package.htm

## Thanks
This development was aided by Kylie at Esri Support Services. Thank you for working with me to solve this.



