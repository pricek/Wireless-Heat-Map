# WirelessHeatMap

Our application is meant to host a site that allows users to view a heatmap of Oregon State University's wireless network population in real time.

To install and run our project, please install python 3.8 and create a virtual environment using the command

```python3.8 -m venv <virtual_environment>```

After verifying that you have the correct version of python installed, clone our repo to your system

```git clone https://github.com/pricek/Wireless-Heat-Map.git```

In order to host a site you need to be in the virtual enviornment you created. To do this use the command

```source <virtual_enviornment>/bin/activate```

You will then need to ensure that the correct dependencies are installed. Do this by navigating to the newly cloned repo and using the command

```pip install -r dependencies.txt```

You will need to install and configure InfluxDB version 1.7.10 on the machine that you are using. After installing run the InfluxDB shell with ```influx``` and setup the data storage with the following commands.

```CREATE DATABASE airwave_data```

```USE airwave_data```

```CREATE RETENTION POLICY two_days ON airwave_data DURATION 24h DEFAULT REPLICATION 1```

```CREATE RETENTION POLICY one_year ON airwave_data DURATION 8736h REPLICATION 1```

```CREATE CONTINUOUS QUERY cq_24h ON airwave_data RESAMPLE EVERY 1d for 1d BEGIN SELECT mean(clients) AS clients, mean(bandwidth_in) AS bandwidth_in, mean(bandwidth_out) AS bandwidth_out INTO airwave_data.one_year.downsampled FROM airwave_data.two_days.ap_usage GROUP BY time(1d), * END```

You will need to modify strings_example.py to include the necessary credentials and rename it to strings.py

Then navigate to the newly cloned repo and in the same directory as manage.py, use the following commands

```python manage.py migrate```

```python manage.py createsuperuser```

```python manage.py buildDB```

```python manage.py buildDB --render```

```python manage.py buildDB --baseline```

```python manage.py runserver 0:<Port>```

Available ports on the server are 8080, 8081, 8082.
You should then be able to view the hosted site in your browser at

```<IP_Address>:<Port>/buildings```

And perform admin actions at

```<IP_Address>:<Port>/admin```
