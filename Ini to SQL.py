import sqlite3
import sys
import traceback
import glob, os, os.path


def main():

    os.chdir("Input")
    txtfilenames = glob.glob("*.txt")
    inifilenames = glob.glob("*.ini")
    
    filenames = txtfilenames + inifilenames
    for x in xrange(len(filenames)):

        with open(filenames[x]) as f:
            filedata = f.readlines()
            
        create_table(filenames[x], filedata)

    
def create_table(name, data):

    sys.stdout.write("\nCreating SQLite table for " + name + "...\n")

    if ".txt" in name:
        slimname = name.strip(".txt")
    elif ".ini" in name:
        slimname = name.strip(".ini")

    os.chdir("..")
    os.chdir("Output")

    if os.path.isfile(slimname + ".db"):
        sys.stdout.write("\n\nError: File named " + slimname + ".db already exists, please remove or rename the file and rerun this application.\n\n")
        os.chdir("..")
        os.chdir("Input")
        return
    
    datanames = []
    datacount = 0
    
    for x in xrange(len(data)):
        data[x] = data[x].strip("\n")

    datanames.append("ID")

    for x in xrange(len(data)):
        if "=" in data[x]:
            values = data[x].split("=")
            if values[0] not in datanames:
                datanames.append(values[0])
        elif "[" in data[x] and data[x][0] == "[":
            datacount +=1
 
    db = sqlite3.connect(slimname + ".db")
    db.text_factory = str
    cursor = db.cursor() 
    cursor.execute(' CREATE TABLE IF NOT EXISTS ' + slimname + ' ( "' + '" , "'.join(datanames) + '" ); ')
    sys.stdout.write("Created " + slimname + ".db.")
    sys.stdout.write("\nAdding data from " + name + " to SQLite table...\n")


    datalist = [{} for _ in xrange(datacount)]
    
    for x in xrange(datacount):
         for y in xrange(len(datanames)):
            datalist[x][datanames[y]] = ""
    curdata = -1
    
    for x in xrange(len(data)):
        if "[" in data[x] and data[x][0] == "[":
            curdata += 1
            datalist[curdata]["ID"] = data[x].strip()[1:-1]
        elif "=" in data[x]:          
            values = data[x].split("=")
            datalist[curdata][values[0]] = values[1]
    valuestr = ""

    for x in xrange(len(datanames)):
        if x == 0:
            valuestr += "?"
        else:
            valuestr += ",?"

    
            
    for x in xrange(datacount):
        datavalues = []
        for y in xrange(len(datanames)):
            datavalues.append(datalist[x][datanames[y]])
            
        cursor.execute(' INSERT INTO ' + slimname + ' ( "' + '" , "'.join(datanames) + '" ) VALUES ( ' + valuestr + ')', datavalues)
        db.commit()

    os.chdir("..")
    os.chdir("Input")
    sys.stdout.write("\n\nConversion of " + name + " complete!\n")


if __name__ == "__main__":
    try:
        main()
    except:
        print sys.exc_info()[0]
        print traceback.format_exc()
    finally:
        print "\nPress Enter to continue..."
        raw_input()
