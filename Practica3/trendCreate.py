import rrdtool
ret = rrdtool.create("trend.rrd",
                     "--start",'N',
                     "--step",'60',
                     "DS:CPUload:GAUGE:60:0:100",
                     "DS:RAM:GAUGE:60:0:100",
                     "DS:Red:GAUGE:60:0:100",
                     "RRA:AVERAGE:0.5:1:60")
if ret:
    print (rrdtool.error())
