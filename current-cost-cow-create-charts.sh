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

rrdtool graph /var/www/spudooli/charts/power-24h.png \
--start end-24h --width 700 --end now --slope-mode \
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

rrdtool graph /var/www/spudooli/charts/power-2hours.png \
--start end-120m --width 700 --end now --slope-mode \
--no-legend --vertical-label Watts --lower-limit 0 \
--alt-autoscale-max \
DEF:Power=current-cost-cow.rrd:Wholehouse:AVERAGE \
LINE3:Power#0000FF:"Average"
