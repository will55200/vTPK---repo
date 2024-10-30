# This script will loop through an AOI gdb and create a vector tile package of the AOI at a user defined scale. 
# This script does not require a vector tile index, this will be processed on the fly. It takes longer to process the vtpk 
# but requires less data management. A text document is used to track and log the processing time for each AOI. 
# For the paramater inputs DO NOT USE any " " or ,
# Developed in 2024 by Jenna Williams using Python 3.11.8 and Esri ArcGIS Pro 3.3


import arcpy
import os
import time
from datetime import datetime

def main():
    arcpy.env.overwriteOutput = True

    # Prompt user for input parameters
    aprx_path = input("Enter the path to the ArcGIS Pro aprx: ")
    temp_aprx_path = input("Enter the path for temporary ArcGIS Pro project file: ")
    vtpk_Output = input("Enter the output directory for Vector Tile Packages: ")
    AOI_gdb_path = input("Enter the path to the geodatabase containing feature class AOIs for the vtpks: ")
    map_name = input("Enter the name of the map in the ArcGIS Pro project: ")
    min_cached_scale = float(input("Enter the minimum cached scale (e.g., 295828763): "))
    max_cached_scale = float(input("Enter the maximum cached scale (e.g., 564): "))
    
    # Start timing the entire process
    start_time = time.time()

    print(f"Loading ArcGIS Pro project from: {aprx_path}")
    aprx = arcpy.mp.ArcGISProject(aprx_path)
    m = aprx.listMaps(map_name)[0]

    print(f"Setting workspace to: {AOI_gdb_path}")
    arcpy.env.workspace = AOI_gdb_path

    # List feature classes in AOI_gdb_path
    feature_classes = sorted(arcpy.ListFeatureClasses())
    total_features = len(feature_classes)

    print(f"Total feature classes to process: {total_features}")

    # Print the names of the feature classes
    print("Feature classes in the geodatabase:")
    for fc in feature_classes:
        print(f"- {fc}")

    # Create a list to store unsuccessful runs
    unsuccessful_runs = []

    # Create a list to store feature class names and their VTPK creation times
    fc_times = []

    # Loop through each feature class
    for index, fc in enumerate(feature_classes, start=1):
        print(f"\nProcessing feature class {index} of {total_features}: {fc}")
        
        # Construct the full path to the feature class
        fc_path = os.path.join(AOI_gdb_path, fc)
        
        print(f"Adding layer to map: {fc}")
        # Add the feature class as a layer to the map
        layer = m.addDataFromPath(fc_path)
        
        # Unselect the layer
        layer.visible = False

        # layer that is defining extent as a polygon
        refLyr = m.listLayers(fc)[0]

        print("Setting map extent...")
        # Get the layer's extent as a polygon
        newExtent = arcpy.Describe(refLyr).extent.polygon

        # Get the map's CIM definition
        m_cim = m.getDefinition('V3')

        # Set the property
        m_cim.customFullExtent = newExtent

        # Apply the modified definition back to the map
        m.setDefinition(m_cim)

        aprx.saveACopy(temp_aprx_path)
        print(f"Temporary project saved to: {temp_aprx_path}")

        print(f"Creating VTPK for {fc} started at {time.ctime()}...")
        vtpk_start_time = time.time()
        
        output = os.path.join(vtpk_Output, f"{fc}.vtpk")
        
        try:
            # Create vector tile package
            arcpy.management.CreateVectorTilePackage(
                in_map=m,
                output_file=output,
                service_type="ONLINE",
                tiling_scheme=None,
                tile_structure="INDEXED",
                min_cached_scale=min_cached_scale,
                max_cached_scale=max_cached_scale,
                index_polygons=None,
                summary="",
                tags=""
            )
        except arcpy.ExecuteError as e:
            print(f"ArcPy error occurred while creating VTPK for {fc}: {e}")
            unsuccessful_runs.append(fc)
        except Exception as e:
            print(f"An unexpected error occurred while creating VTPK for {fc}: {e}")
            unsuccessful_runs.append(fc)
        else:
            vtpk_end_time = time.time()
            vtpk_duration = vtpk_end_time - vtpk_start_time
            minutes, seconds = divmod(vtpk_duration, 60)
            print(f"VTPK for {fc} created in {int(minutes)} minutes and {int(seconds)} seconds")
            current_date = datetime.now().strftime("%Y-%m-%d")
            fc_times.append((fc, f"{int(minutes)}m {int(seconds)}s", current_date))
        finally:
            # Write the feature class names and their VTPK creation times to a text file
            output_txt = os.path.join(vtpk_Output, "VTPK_Creation_Times.txt")
            with open(output_txt, "w") as f:
                f.write("Feature Class\tCreation Time\tCreation Date\n")
                for fc, time_taken, current_date in fc_times:
                    f.write(f"{fc}\t{time_taken}\t{current_date}\n")

            print(f"\nVTPK creation times saved to: {output_txt}")

        # Remove the layer from the map
        print(f"Removing layer: {fc}")
        m.removeLayer(layer)

        print(f"Progress: {index}/{total_features} ({index/total_features*100:.2f}%)")

    end_time = time.time()
    total_duration = end_time - start_time
    hours, remainder = divmod(total_duration, 3600)
    total_minutes, total_seconds = divmod(remainder, 60)

    print(f"\nScript completed in {int(hours)} hours, {int(total_minutes)} minutes and {int(total_seconds)} seconds")
    print(f"Total feature classes processed: {total_features}")

    # Print the list of unsuccessful runs
    if unsuccessful_runs:
        print("\nUnsuccessful runs:")
        for run in unsuccessful_runs:
            print(f"- {run}")
    else:
        print("\nAll feature classes processed successfully.")

if __name__ == "__main__":
    main()