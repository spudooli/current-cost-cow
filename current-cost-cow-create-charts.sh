cd /var/www/scripts/current-cost-cow
rrdtool graph /var/www/spudooli/charts/power-week.png \
--start end-7d --width 700 --end now --slope-mode \
--no-legend --vertical-label Watts --lower-limit 0 \
--alt-autoscale-max \
DEF:Power=current-cost-cow.rrd:Wholehouse:AVERAGE \
DEF:PowerMin=current-cost-cow.rrd:Wholehouse:MIN \
DEF:PowerMax=current-cost-cow.rrd:Wholehouse:MAX \
CDEF:PowerRange=PowerMax,PowerMin,- \
LINE1:PowerMin: \
AREA:PowerRange#0000FF11:"Error Range":STACK \
LINE1:PowerMin#0000FF33:"Min" \
LINE1:PowerMax#0000FF33:"Max" \
LINE1:Power#0000FF:"Average"

rrdtool graph /var/www/spudooli/charts/hotwater-week.png \
--start end-7d --width 700 --end now --slope-mode \
--no-legend --vertical-label Watts --lower-limit 0 \
--alt-autoscale-max \
DEF:Power=current-cost-cow.rrd:Hotwater:AVERAGE \
DEF:PowerMin=current-cost-cow.rrd:Hotwater:MIN \
DEF:PowerMax=current-cost-cow.rrd:Hotwater:MAX \
CDEF:PowerRange=PowerMax,PowerMin,- \
LINE1:PowerMin: \
AREA:PowerRange#FF000011:"Error Range":STACK \
LINE1:PowerMin#FF000033:"Min" \
LINE1:PowerMax#FF000033:"Max" \
LINE1:Power#FF0000:"Average"

rrdtool graph /var/www/spudooli/charts/power-24h.png \
--start end-24h --width 700 --end now --slope-mode \
--no-legend --vertical-label Watts --lower-limit 0 \
--alt-autoscale-max \
DEF:Hotwater=current-cost-cow.rrd:Hotwater:AVERAGE \
DEF:HotwaterMin=current-cost-cow.rrd:Hotwater:MIN \
DEF:HotwaterMax=current-cost-cow.rrd:Hotwater:MAX \
CDEF:HotwaterRange=HotwaterMax,HotwaterMin,- \
LINE1:HotwaterMin: \
AREA:HotwaterRange#FF000011:"Error Range":STACK \
LINE1:HotwaterMin#FF000033:"Min" \
LINE1:HotwaterMax#FF000033:"Max" \
LINE1:Hotwater#FF0000:"Average" \
DEF:Wholehouse=current-cost-cow.rrd:Wholehouse:AVERAGE \
DEF:WholehouseMin=current-cost-cow.rrd:Wholehouse:MIN \
DEF:WholehouseMax=current-cost-cow.rrd:Wholehouse:MAX \
CDEF:WholehouseRange=WholehouseMax,WholehouseMin,- \
LINE1:WholehouseMin: \
AREA:WholehouseRange#0000FF11:"Error Range":STACK \
LINE1:WholehouseMin#0000FF33:"Min" \
LINE1:WholehouseMax#0000FF33:"Max" \
LINE1:Wholehouse#0000FF:"Average"

rrdtool graph /var/www/spudooli/charts/power-2hours.png \
--start end-120m --width 700 --end now --slope-mode \
--no-legend --vertical-label Watts --lower-limit 0 \
--alt-autoscale-max \
DEF:Hotwater=current-cost-cow.rrd:Hotwater:AVERAGE \
DEF:Wholehouse=current-cost-cow.rrd:Wholehouse:AVERAGE \
LINE3:Wholehouse#0000FF:"Average" \
LINE3:Hotwater#FF0000:"Average"
