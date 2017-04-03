import subprocess
import datetime
import sys

grid_proc       = subprocess.Popen(["python grid.py"],stdout=subprocess.PIPE, shell=True) 
(grid_out, err) = grid_proc.communicate()


pv_proc         = subprocess.Popen(["python pvgrid.py"], stdout=subprocess.PIPE, shell=True)
(pv_out,err)    = pv_proc.communicate()


dc_proc         = subprocess.Popen(["python dcpanel.py"], stdout=subprocess.PIPE, shell=True)
(dc_out,err)    = dc_proc.communicate()


weather_proc      = subprocess.Popen(["python weather.py"], stdout=subprocess.PIPE, shell=True)
(weather_out,err) = weather_proc.communicate()



gridy    = grid_out.rstrip()
pvy      = pv_out.rstrip()
dcvy     = dc_out.rstrip()
weathery = weather_out.rstrip()

current  = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())


data_string = gridy + ',' + pvy + ',' + dcvy  + ',' + weathery + ',' + current

print data_string

with open('march.csv', "a") as myfile:
    myfile.write(data_string+"\n")

sys.exit()
